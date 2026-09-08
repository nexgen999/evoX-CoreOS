import os
import json
from datetime import datetime

def generate_build_changelog():
    json_dir = "json"
    changelog_path = "CHANGELOG.md"
    
    # Catégories gérées
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
                # Selon la structure, on map par nom ou filename
                for item in old_data:
                    old_items_map[item.get('name')] = item.get('version')
                    
        added_or_updated = []
        for item in new_data:
            name = item.get('name')
            version = item.get('version', 'v1.0.0')
            
            if name not in old_items_map:
                added_or_updated.append(f"`{name}` ({version}) - *Nouveau*")
            elif old_items_map[name] != version:
                added_or_updated.append(f"`{name}` ({version}) - *Mise à jour (Précédent: {old_items_map[name]})*")
                
        if added_or_updated:
            current_changes[cat] = added_or_updated
            
        # Sauvegarde du nouveau fichier en tant qu'ancien pour la prochaine build
        with open(old_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=4, ensure_ascii=False)

    if not current_changes:
        return # Rien de nouveau, pas de modification du changelog

    # Formatage de l'entrée du jour
    date_str = datetime.now().strftime("%d/%m/%Y à %H:%M")
    new_section = f"## Build du {date_str}\n"
    for cat, items in current_changes.items():
        new_section += f"* **{cat.upper()}**\n"
        for entry in items:
            new_section += f"  * {entry}\n"
    new_section += "\n"

    # Lecture de l'ancien changelog s'il existe pour prepend (ajouter en haut)
    existing_content = ""
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    else:
        existing_content = "# 📜 Journal des Mises à Jour (Changelog)\n\n"

    # Insertion de la nouvelle build juste après le titre principal
    header = "# 📜 Journal des Mises à Jour (Changelog)\n\n"
    body_content = existing_content.replace(header, "")
    
    final_content = header + new_section + body_content

    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print("✅ Changelog de build généré avec succès !")
