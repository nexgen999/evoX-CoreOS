import os
from datetime import datetime
from scripts.config_rules import PATHS

def generate_release_notes(data_store_by_cat):
    notes_path = "release_notes.md"
    changelog_path = "CHANGELOG.md"
    date_str = datetime.now().strftime("v%Y.%m.%d-%H%M")
    
    categories = ["payloads", "pkg", "ffpfsc", "apps"]
    
    # Extraction automatique des nouveautés directement depuis le CHANGELOG.md fraîchement généré
    recent_changes_html = ""
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            changelog_content = f.read()
            
        # On extrait la première section de build du changelog
        parts = changelog_content.split("## Build du ")
        if len(parts) > 1:
            latest_build_block = parts[1].split("## Build du ")[0]
            lines = latest_build_block.strip().split('\n')
            # Ignore la première ligne (la date du build)
            build_lines = lines[1:] if len(lines) > 1 else []
            
            if build_lines:
                current_cat = None
                cat_items = {}
                for line in build_lines:
                    if line.startswith("- "):
                        cat_name = line.replace("- ", "").strip()
                        current_cat = cat_name
                        cat_items[current_cat] = []
                    elif line.startswith("  - ") or line.startswith("   - ") or line.startswith("    - "):
                        item_text = line.strip().lstrip("- ").strip()
                        if current_cat:
                            cat_items[current_cat].append(item_text)
                
                for cat, items in cat_items.items():
                    recent_changes_html += f"<details>\n<summary><b>{cat}</b> ({len(items)} changements)</summary>\n\n"
                    for entry in items:
                        recent_changes_html += f"- {entry}\n"
                    recent_changes_html += "\n</details>\n\n"

    # Construction du contenu Markdown global
    content = f"### 🚀 Synthèse de la mise à jour ({date_str})\n\n"
    content += "Le store PlayStation 5 a été mis à jour avec succès.\n\n"
    
    content += "#### 📦 Archives AIO Disponibles :\n"
    content += "- `PS5_payloads_aio_latest.zip`\n"
    content += "- `PS5_pkg_aio_latest.zip`\n"
    content += "- `PS5_ffpfsc_aio_latest.zip`\n"
    content += "- `PS5_apps_aio_latest.zip`\n"
    content += "- `PS5_ultimate_pack_latest.zip`\n\n"
    
    content += "#### 📂 Fichiers inclus / mis à jour :\n"
    if recent_changes_html:
        content += recent_changes_html
    else:
        content += "*Aucun nouveau fichier ou changement détecté sur cette build.*\n\n"

    content += "#### 🛠️ Détail des Packs & Contenu des Archives\n"
    
    icons = {
        "payloads": "⚡",
        "pkg": "🎮",
        "ffpfsc": "📄",
        "apps": "🛠️"
    }

    json_dir = PATHS.get("json_dir", "json")
    for cat_key in categories:
        json_file_path = os.path.join(json_dir, f"{cat_key}.json")
        icon = icons.get(cat_key, "📦")
        content += f"<details>\n<summary><b>{icon} Pack {cat_key.upper()}</b></summary>\n\n"
        
        has_items = False
        import json
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                json_content = json.load(f)
                
            if isinstance(json_content, dict):
                for section_key, section_val in json_content.items():
                    if section_key == "name":
                        continue
                        
                    file_entries = []
                    if isinstance(section_val, list):
                        for item in section_val:
                            if isinstance(item, dict):
                                fname = item.get('filename')
                                if fname:
                                    file_entries.append(fname)
                    elif isinstance(section_val, dict):
                        sub_items = section_val.get('items', [])
                        if isinstance(sub_items, list):
                            for item in sub_items:
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
    print("    ✅ Fichier release_notes.md généré avec succès à partir du Changelog !")
