import os
import json
from datetime import datetime
from scripts.config_rules import PATHS

def generate_release_notes(data_store_by_cat):
    json_dir = PATHS.get("json_dir", "json")
    notes_path = "release_notes.md"
    date_str = datetime.now().strftime("v%Y.%m.%d-%H%M")
    
    # 1. Détection des nouveautés/mises à jour
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

    # 2. Construction du contenu Markdown pour la Release
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

    def extract_files_recursively(data):
        found = []
        if isinstance(data, list):
            for elem in data:
                found.extend(extract_files_recursively(elem))
        elif isinstance(data, dict):
            # Si le dictionnaire représente un fichier direct (contient filename ou name et pas juste une structure de regroupement)
            if "filename" in data or ("name" in data and ("url" in data or "version" in data or "path" in data)):
                filename = data.get('filename', data.get('name', ''))
                version = data.get('version', '')
                if filename and filename not in ["name", "items"]:
                    found.append((filename, version))
            # Sinon on fouille dans toutes les valeurs du dictionnaire
            for k, v in data.items():
                if k not in ["name", "items"] or isinstance(v, list):
                    found.extend(extract_files_recursively(v))
        return found

    for cat_key, cat_dict in data_store_by_cat.items():
        icon = icons.get(cat_key, "📦")
        content += f"<details>\n<summary><b>{icon} Pack {cat_key.upper()}</b></summary>\n\n"
        
        has_items = False
        if isinstance(cat_dict, dict):
            for sub_cat_name, sub_cat_data in cat_dict.items():
                files = extract_files_recursively(sub_cat_data)
                if files:
                    has_items = True
                    content += f"* **{sub_cat_name}**\n"
                    # Dédoublonner tout en gardant l'ordre
                    seen = set()
                    for filename, version in files:
                        if filename not in seen:
                            seen.add(filename)
                            ver_str = f" *({version})*" if version else ""
                            content += f"  * `{filename}`{ver_str}\n"
        
        if not has_items:
            content += "*Aucun élément dans ce pack.*\n"
            
        content += "\n</details>\n\n"

    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("    ✅ Fichier release_notes.md généré avec succès !")
