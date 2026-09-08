# update_store.py
import os
import json
import zipfile
from datetime import datetime
from scripts.config_rules import PATHS
from scripts.fetchers.payloads_fetcher import fetch_payloads_category
from scripts.fetchers.pkg_fetcher import fetch_pkg_category
from scripts.fetchers.ffpfsc_fetcher import fetch_ffpfsc_category
from scripts.fetchers.apps_fetcher import fetch_apps_category
from scripts.generate_json import build_all
from scripts.generate_rss import build_rss_feed
from scripts.generate_readme import build_readme
from scripts.generate_web import build_index_html
from scripts.changelog_builder import generate_build_changelog

def generate_release_notes(data_store_by_cat):
    print("📝 Génération des notes de version pour la Release...")
    json_dir = PATHS.get("json_dir", "json")
    notes_path = "release_notes.md"
    date_str = datetime.now().strftime("v%Y.%m.%d-%H%M")
    
    categories = ["payloads", "pkg", "ffpfsc", "apps"]
    current_changes = {}
    
    for cat in categories:
        new_file = os.path.join(json_dir, f"{cat}.json")
        old_file = os.path.join(json_dir, f"old_{cat}.json")
        
        if not os.path.exists(new_file):
            continue
            
        with open(new_file, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
            
        old_items_map = {}
        if os.path.exists(old_file):
            with open(old_file, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
                for item in old_data:
                    if isinstance(item, dict):
                        old_items_map[item.get('name')] = item.get('version')
                    elif isinstance(item, str):
                        old_items_map[item] = ""
                    
        added_or_updated = []
        for item in new_data:
            if isinstance(item, dict):
                name = item.get('name')
                version = item.get('version', 'v1.0.0')
            elif isinstance(item, str):
                name = item
                version = ""
            else:
                continue
                
            if not name:
                continue
            
            if name not in old_items_map:
                added_or_updated.append(f"`{name}` ({version}) - *Nouveau*".strip())
            elif version and old_items_map.get(name) != version:
                added_or_updated.append(f"`{name}` ({version}) - *Mis à jour*".strip())
                
        if added_or_updated:
            current_changes[cat] = added_or_updated

    content = f"### 🚀 Synthèse de la mise à jour ({date_str})\n\n"
    content += "Le store PlayStation 5 a été mis à jour avec succès.\n\n"
    
    content += "#### 📦 Archives AIO Disponibles :\n"
    content += "- `PS5_payloads_aio_latest.zip`\n"
    content += "- `PS5_pkg_aio_latest.zip`\n"
    content += "- `PS5_ffpfsc_aio_latest.zip`\n"
    content += "- `PS5_apps_aio_latest.zip`\n"
    content += "- `PS5_ultimate_pack_latest.zip`\n\n"
    
    content += "#### 📂 Fichiers inclus / mis à jour :\n"
    if current_changes:
        for cat, items in current_changes.items():
            content += f"<details>\n<summary><b>{cat.upper()}</b> ({len(items)} changements)</summary>\n\n"
            for entry in items:
                content += f"- {entry}\n"
            content += "\n</details>\n\n"
    else:
        content += "*Aucun nouveau fichier ou changement détecté sur cette build.*\n\n"

    content += "#### 🛠️ Détail des Packs & Contenu des Archives\n"
    
    icons = {
        "payloads": "⚡",
        "pkg": "🎮",
        "ffpfsc": "📄",
        "apps": "🛠️"
    }

    for cat_key, cat_dict in data_store_by_cat.items():
        icon = icons.get(cat_key, "📦")
        content += f"<details>\n<summary><b>{icon} Pack {cat_key.upper()}</b></summary>\n\n"
        
        has_items = False
        for sub_cat, items in cat_dict.items():
            if items:
                has_items = True
                content += f"* **{sub_cat}**\n"
                for item in items:
                    if isinstance(item, dict):
                        filename = item.get('filename', item.get('name', ''))
                        version = item.get('version', '')
                        ver_str = f" *({version})*" if version else ""
                        content += f"  * `{filename}`{ver_str}\n"
                    elif isinstance(item, str):
                        content += f"  * `{item}`\n"
        
        if not has_items:
            content += "*Aucun élément dans ce pack.*\n"
            
        content += "\n</details>\n\n"

    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("    ✅ Fichier release_notes.md généré avec succès !")

def build_aio_archives(payloads_flat, pkg_flat, ffpfsc_flat, apps_flat):
    print("📦 [Bonus] Génération des archives AIO ZIP...")
    archives_dir = PATHS.get("archives_dir", "archives")
    os.makedirs(archives_dir, exist_ok=True)

    def create_zip(zip_name, items):
        zip_path = os.path.join(archives_dir, zip_name)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for item in items:
                file_path = item.get("local_path") if isinstance(item, dict) else None
                if file_path and os.path.exists(file_path):
                    zf.write(file_path, arcname=os.path.basename(file_path))
        size_bytes = os.path.getsize(zip_path) if os.path.exists(zip_path) else 0
        print(f"    ➔ Archive générée : {zip_path} ({size_bytes} octets)")

    create_zip("PS5_payloads_aio_latest.zip", payloads_flat)
    create_zip("PS5_pkg_aio_latest.zip", pkg_flat)
    create_zip("PS5_ffpfsc_aio_latest.zip", ffpfsc_flat)
    create_zip("PS5_apps_aio_latest.zip", apps_flat)
    create_zip("PS5_ultimate_pack_latest.zip", payloads_flat + pkg_flat + ffpfsc_flat + apps_flat)

def main():
    print("🚀 Démarrage de la mise à jour globale du store PS5...")
    credits_set = set()
    
    os.makedirs(PATHS["archives_dir"], exist_ok=True)
    os.makedirs(PATHS["json_dir"], exist_ok=True)
    os.makedirs(PATHS["payloads_dir"], exist_ok=True)

    print("🔍 [1/5] Scraping des sources OPML et téléchargement des binaires...")
    payloads_by_cat, payloads_flat = fetch_payloads_category(credits_set)
    pkg_by_cat, pkg_flat = fetch_pkg_category(credits_set)
    ffpfsc_by_cat, ffpfsc_flat = fetch_ffpfsc_category(credits_set)
    apps_by_cat, apps_flat = fetch_apps_category(credits_set)

    data_store = {
        "payloads": (payloads_by_cat, payloads_flat),
        "pkg": (pkg_by_cat, pkg_flat),
        "ffpfsc": (ffpfsc_by_cat, ffpfsc_flat),
        "apps": (apps_by_cat, apps_flat)
    }

    data_store_by_cat = {
        "payloads": payloads_by_cat,
        "pkg": pkg_by_cat,
        "ffpfsc": ffpfsc_by_cat,
        "apps": apps_by_cat
    }

    data_store_flat = {
        "payloads": {"name": "Payloads", "items": payloads_flat},
        "pkg": {"name": "Packages PKG", "items": pkg_flat},
        "ffpfsc": {"name": "Fichiers FFPFSC", "items": ffpfsc_flat},
        "apps": {"name": "Applications", "items": apps_flat}
    }

    print("📦 [2/5] Génération de l'arborescence JSON complète...")
    build_all(data_store)

    print("📡 [3/5] Génération des flux RSS et OPML...")
    build_rss_feed(data_store_flat)

    print("🌐 [4/5] Génération de la page index.html...")
    build_index_html(data_store_by_cat)

    print("📝 [5/5] Mise à jour du README.md, des Crédits, du Changelog et des Notes de Release...")
    build_readme(credits_set, data_store_by_cat)
    generate_build_changelog()
    generate_release_notes(data_store_by_cat)

    build_aio_archives(payloads_flat, pkg_flat, ffpfsc_flat, apps_flat)

    print("✅ Mise à jour du store et des packages terminée avec succès !")

if __name__ == "__main__":
    main()
