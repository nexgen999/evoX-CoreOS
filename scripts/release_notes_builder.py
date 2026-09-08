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
                def extract_old_items(data):
                    items = []
                    if isinstance(data, list):
                        for item in data:
                            items.extend(extract_old_items(item))
                    elif isinstance(data, dict):
                        if "name" in data or "filename" in data:
                            items.append(data)
                        for v in data.values():
                            items.extend(extract_old_items(v))
                    return items
                    
                for item in extract_old_items(old_data):
                    if isinstance(item, dict):
                        name = item.get('filename') or item.get('name')
                        if name and name not in ["name", "items"]:
                            old_items_map[name] = item.get('version', '')
                    elif isinstance(item, str):
                        old_items_map[item] = ""
                    
        added_or_updated = []
        def extract_new_items(data):
            items = []
            if isinstance(data, list):
                for item in data:
                    items.extend(extract_new_items(item))
            elif isinstance(data, dict):
                if "name" in data or "filename" in data:
                    items.append(data)
                for v in data.values():
                    items.extend(extract_new_items(v))
            return items

        for item in extract_new_items(new_data):
            if isinstance(item, dict):
                name = item.get('filename') or item.get('name')
                version = item.get('version', 'v1.0.0')
            elif isinstance(item, str):
                name = item
                version = ""
            else:
                continue
                
            if not name or name in ["name", "items"]:
                continue
            
            if name not in old_items_map:
                added_or_updated.append(f"`{name}` ({version}) - *Nouveau*".strip())
            elif version and old_items_map.get(name) != version:
                added_or_updated.append(f"`{name}` ({version}) - *Mis à jour*".strip())
                
        if added_or_updated:
            current_changes[cat] = sorted(list(set(added_or_updated)))

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

    # 3. Lecture directe des fichiers JSON générés pour l'affichage propre
    for cat_key in categories:
        json_file_path = os.path.join(json_dir, f"{cat_key}.json")
        icon = icons.get(cat_key, "📦")
        content += f"<details>\n<summary><b>{icon} Pack {cat_key.upper()}</b></summary>\n\n"
        
        has_items = False
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                json_content = json.load(f)
                
            if isinstance(json_content, list):
                for element in json_content:
                    if isinstance(element, dict):
                        sub_name = element.get('name') or element.get('category') or "Éléments"
                        sub_items = element.get('items', [element])
                        
                        if isinstance(sub_items, list) and sub_items:
                            valid_sub_items = []
                            for sub_item in sub_items:
                                if isinstance(sub_item, dict):
                                    fname = sub_item.get('filename') or sub_item.get('name', '')
                                    fver = sub_item.get('version', '')
                                    if fname and fname not in ["name", "items"]:
                                        valid_sub_items.append((fname, fver))
                                elif isinstance(sub_item, str):
                                    valid_sub_items.append((sub_item, ''))
                                    
                            if valid_sub_items:
                                has_items = True
                                content += f"* **{sub_name}**\n"
                                seen_files = set()
                                for fname, fver in valid_sub_items:
                                    if fname not in seen_files:
                                        seen_files.add(fname)
                                        ver_str = f" *({fver})*" if fver else ""
                                        content += f"  * `{fname}`{ver_str}\n"
            elif isinstance(json_content, dict):
                for sub_name, sub_items in json_content.items():
                    if sub_items:
                        has_items = True
                        content += f"* **{sub_name}**\n"
                        if isinstance(sub_items, list):
                            seen_files = set()
                            for sub_item in sub_items:
                                if isinstance(sub_item, dict):
                                    fname = sub_item.get('filename') or sub_item.get('name', '')
                                    fver = sub_item.get('version', '')
                                    if fname and fname not in ["name", "items"] and fname not in seen_files:
                                        seen_files.add(fname)
                                        ver_str = f" *({fver})*" if fver else ""
                                        content += f"  * `{fname}`{ver_str}\n"
                                elif isinstance(sub_item, str) and sub_item not in seen_files:
                                    seen_files.add(sub_item)
                                    content += f"  * `{sub_item}`\n"
        
        if not has_items:
            content += "*Aucun élément dans ce pack.*\n"
            
        content += "\n</details>\n\n"

    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("    ✅ Fichier release_notes.md généré avec succès !")
