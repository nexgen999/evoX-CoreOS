import os
import json
from datetime import datetime
from scripts.config_rules import PATHS

def generate_release_notes(data_store_by_cat):
    json_dir = PATHS.get("json_dir", "json")
    notes_path = "release_notes.md"
    date_str = datetime.now().strftime("v%Y.%m.%d-%H%M")
    
    # 1. Détection des nouveautés/mises à jour (comparaison old_*.json vs *.json)
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

    for cat_key, cat_dict in data_store_by_cat.items():
        icon = icons.get(cat_key, "📦")
        content += f"<details>\n<summary><b>{icon} Pack {cat_key.upper()}</b></summary>\n\n"
        
        has_items = False
        for sub_cat_name, sub_cat_data in cat_dict.items():
            items_list = []
            if isinstance(sub_cat_data, dict):
                items_list = sub_cat_data.get('items', [])
            elif isinstance(sub_cat_data, list):
                items_list = sub_cat_data
                
            if items_list:
                has_items = True
                content += f"* **{sub_cat_name}**\n"
                for item in items_list:
                    if isinstance(item, dict):
                        filename = item.get('filename', item.get('name', ''))
                        version = item.get('version', '')
                        ver_str = f" *({version})*" if version else ""
                        if filename:
                            content += f"  * `{filename}`{ver_str}\n"
                    elif isinstance(item, str):
                        content += f"  * `{item}`\n"
        
        if not has_items:
            content += "*Aucun élément dans ce pack.*\n"
            
        content += "\n</details>\n\n"

    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("    ✅ Fichier release_notes.md généré avec succès !")
