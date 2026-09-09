import os
import json
from datetime import datetime
from scripts.config_rules import PATHS

def generate_release_notes(data_store_by_cat):
    print("📝 Génération des notes de version pour la Release...")
    json_dir = PATHS.get("json_dir", "json")
    notes_path = "release_notes.md"
    date_str = datetime.now().strftime("v%Y.%m.%d-%H%M")
    
    categories = ["payloads", "pkg", "ffpfsc", "apps"]
    current_changes = {}
    
    # 1. Détection automatique des nouveautés par comparaison old / new JSON
    for cat in categories:
        new_file = os.path.join(json_dir, f"{cat}.json")
        old_file = os.path.join(json_dir, f"old_{cat}.json")
        
        if not os.path.exists(new_file):
            continue
            
        with open(new_file, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
            
        old_filenames = set()
        if os.path.exists(old_file):
            with open(old_file, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
                for key, val in old_data.items():
                    if isinstance(val, list):
                        for item in val:
                            if isinstance(item, dict):
                                fname = item.get('filename')
                                if fname:
                                    old_filenames.add(fname)
                    elif isinstance(val, dict):
                        items_list = val.get('items', [])
                        for item in items_list:
                            if isinstance(item, dict):
                                fname = item.get('filename')
                                if fname:
                                    old_filenames.add(fname)
                    
        added_or_updated = []
        if isinstance(new_data, dict):
            for key, val in new_data.items():
                if key == "name":
                    continue
                items_list = []
                if isinstance(val, list):
                    items_list = val
                elif isinstance(val, dict):
                    items_list = val.get('items', [])
                    
                for item in items_list:
                    if isinstance(item, dict):
                        fname = item.get('filename')
                        if fname and fname not in old_filenames:
                            added_or_updated.append(f"`{fname}` - *Nouveau*")
                            
        if added_or_updated:
            current_changes[cat] = sorted(list(set(added_or_updated)))

    # 2. Construction du contenu Markdown global
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

    for cat_key in categories:
        json_file_path = os.path.join(json_dir, f"{cat_key}.json")
        icon = icons.get(cat_key, "📦")
        content += f"<details>\n<summary><b>{icon} Pack {cat_key.upper()}</b></summary>\n\n"
        
        has_items = False
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                json_content = json.load(f)
                
            if isinstance(json_content, dict):
                for section_key, section_val in json_content.items():
                    if section_key == "name":
                        continue
                        
                    file_entries = []
                    items_list = []
                    if isinstance(section_val, list):
                        items_list = section_val
                    elif isinstance(section_val, dict):
                        items_list = section_val.get('items', [])
                        
                    for item in items_list:
                        if isinstance(item, dict):
                            fname = item.get('filename')
                            if fname:
                                file_entries.append(fname)
                        
                    if file_entries:
                        has_items = True
                        content += f"* **{section_key}**\n"
                        seen = set()
                        for fname in file_entries:
                            if fname not in seen:
                                seen.add(fname)
                                content += f"  * `{fname}`\n"
        
        if not has_items:
            content += "*Aucun élément dans ce pack.*\n"
            
        content += "\n</details>\n\n"

    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("    ✅ Fichier release_notes.md généré avec succès !")
