import os
import json
from datetime import datetime
from scripts.config_rules import PATHS

def generate_build_changelog():
    print("📝 [Bonus] Génération du changelog de build incrémental...")
    json_dir = PATHS.get("json_dir", "json")
    changelog_path = "CHANGELOG.md"
    
    categories = ["payloads", "pkg", "ffpfsc", "apps"]
    current_changes = {}
    
    for cat in categories:
        new_file = os.path.join(json_dir, f"{cat}.json")
        old_file = os.path.join(json_dir, f"old_{cat}.json")
        
        if not os.path.exists(new_file):
            continue
            
        with open(new_file, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
            
        # Indexation des anciens éléments (compatibilité structure plate ou imbriquée)
        old_items_map = {}
        if os.path.exists(old_file):
            with open(old_file, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
                
            def extract_items_to_map(data, target_map):
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            name = item.get('name') or item.get('filename')
                            version = item.get('version')
                            if name:
                                target_map[name] = version
                elif isinstance(data, dict):
                    for val in data.values():
                        extract_items_to_map(val, target_map)

            extract_items_to_map(old_data, old_items_map)
                
        # Extraction et comparaison des nouveaux éléments
        new_items_list = []
        def collect_new_items(data, target_list):
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        target_list.append(item)
            elif isinstance(data, dict):
                # Si c'est un dict de sous-catégories contenant des listes ou des dicts d'items
                for sub_val in data.values():
                    if isinstance(sub_val, list):
                        target_list.extend([i for i in sub_val if isinstance(i, dict)])
                    elif isinstance(sub_val, dict):
                        # Cas où les items sont dans une clé 'items' ou directement dedans
                        if 'items' in sub_val and isinstance(sub_val['items'], list):
                            target_list.extend([i for i in sub_val['items'] if isinstance(i, dict)])
                        else:
                            collect_new_items(sub_val, target_list)

        collect_new_items(new_data, new_items_list)
        
        added_or_updated = []
        for item in new_items_list:
            name = item.get('name') or item.get('filename')
            version = item.get('version', 'v1.0.0')
            
            if not name:
                continue
            
            if name not in old_items_map:
                added_or_updated.append(f"`{name}` ({version}) - *Nouveau*")
            elif old_items_map[name] != version:
                added_or_updated.append(f"`{name}` ({version}) - *Mise à jour (Précédent: {old_items_map[name]})*")
                
        if added_or_updated:
            current_changes[cat] = added_or_updated
            
        with open(old_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=4, ensure_ascii=False)

    if not current_changes:
        print("    ℹ️ Aucun nouveau fichier ou changement détecté pour ce build.")
        return

    date_str = datetime.now().strftime("%d/%m/%Y à %H:%M")
    new_section = f"## Build du {date_str}\n"
    for cat, items in current_changes.items():
        new_section += f"* **{cat.upper()}**\n"
        for entry in items:
            new_section += f"  * {entry}\n"
    new_section += "\n"

    existing_content = ""
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    else:
        existing_content = "# 📜 Journal des Mises à Jour (Changelog)\n\n"

    header = "# 📜 Journal des Mises à Jour (Changelog)\n\n"
    body_content = existing_content.replace(header, "")
    
    final_content = header + new_section + body_content

    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print("    ✅ Fichier CHANGELOG.md mis à jour avec succès !")
