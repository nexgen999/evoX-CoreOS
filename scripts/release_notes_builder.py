import os
import json
from datetime import datetime
from scripts.config_rules import PATHS

def generate_release_notes(data_store_by_cat):
    json_dir = PATHS.get("json_dir", "json")
    notes_path = "release_notes.md"
    date_str = datetime.now().strftime("v%Y.%m.%d-%H%M")
    
    categories = ["payloads", "pkg", "ffpfsc", "apps"]
    current_changes = {}
    
    # 1. Détection des nouveautés/mises à jour
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
                if isinstance(old_data, dict):
                    for sub_cat, sub_list in old_data.items():
                        if isinstance(sub_list, list):
                            for item in sub_list:
                                if isinstance(item, dict):
                                    fname = item.get('filename')
                                    if fname:
                                        old_items_map[fname] = item.get('version', '')
                    
        added_or_updated = []
        if isinstance(new_data, dict):
            for sub_cat, sub_list in new_data.items():
                if isinstance(sub_list, list):
                    for item in sub_list:
                        if isinstance(item, dict):
                            fname = item.get('filename')
                            fver = item.get('version', 'v1.0.0')
                            if not fname:
                                continue
                            
                            if fname not in old_items_map:
                                added_or_updated.append(f"`{fname}` ({fver}) - *Nouveau*")
                            elif fver and old_items_map.get(fname) != fver:
                                added_or_updated.append(f"`{fname}` ({fver}) - *Mis à jour*")
                                
        if added_or_updated:
            current_changes[cat] = sorted(list(set(added_or_updated)))

    # 2. Construction du contenu Markdown
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

    # 3. Lecture directe et stricte des JSON par catégorie
    for cat_key in categories:
        json_file_path = os.path.join(json_dir, f"{cat_key}.json")
        icon = icons.get(cat_key, "📦")
        content += f"<details>\n<summary><b>{icon} Pack {cat_key.upper()}</b></summary>\n\n"
        
        has_items = False
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                json_content = json.load(f)
                
            if isinstance(json_content, dict):
                for sub_cat_name, sub_list in json_content.items():
                    if isinstance(sub_list, list) and sub_list:
                        valid_files = []
                        for item in sub_list:
                            if isinstance(item, dict):
                                fname = item.get('filename')
                                fver = item.get('version', '')
                                if fname:
                                    valid_files.append((fname, fver))
                        
                        if valid_files:
                            has_items = True
                            content += f"* **{sub_cat_name}**\n"
                            seen = set()
                            for fname, fver in valid_files:
                                if fname not in seen:
                                    seen.add(fname)
                                    ver_str = f" *({fver})*" if fver else ""
                                    content += f"  * `{fname}`{ver_str}\n"
        
        if not has_items:
            content += "*Aucun élément dans ce pack.*\n"
            
        content += "\n</details>\n\n"

    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("    ✅ Fichier release_notes.md généré avec succès !")
