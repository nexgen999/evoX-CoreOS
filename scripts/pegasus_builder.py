import os
import json

def apply_pegasus_metadata(items_list):
    """
    Injecte les métadonnées personnalisées (titleId, title, icône/poster) 
    configurées via l'application Manager.
    """
    # Résolution absolue du chemin vers assets/icon/pegasus_metadata.json
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.abspath(os.path.join(base_dir, "..", "assets", "icon", "pegasus_metadata.json"))
    
    metadata = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        except Exception as e:
            print(f"    ⚠️ Erreur lors de la lecture de {config_path}: {e}")

    for item in items_list:
        fname = item.get("filename")
        # Si le nom de fichier n'est pas explicite, on l'extrait de l'URL
        if not fname and item.get("url"):
            fname = os.path.basename(item["url"])
            
        if fname in metadata:
            overrides = metadata[fname]
            if overrides.get("titleId"):
                item["titleId"] = overrides["titleId"]
            if overrides.get("title"):
                item["title"] = overrides["title"]
            if overrides.get("icon"):
                icon_name = overrides['icon']
                if icon_name.strip():
                    item["posterUrl"] = f"https://cdn.jsdelivr.net/gh/nexgen999/evoX-CoreOS@main/assets/icon/{icon_name}"
                
    return items_list

def generate_pegasus_catalog(pkg_flat, ffpfsc_flat, output_path="json/pegasus_catalog.json"):
    """
    Génère le catalogue unifié Pegasus compatible avec les éléments PKG et FFPFSC,
    en y appliquant les métadonnées personnalisées.
    """
    all_items = []
    
    # Fusion et formatage des éléments PKG et FFPFSC
    for item in pkg_flat + ffpfsc_flat:
        if isinstance(item, dict):
            fname = item.get("filename")
            if not fname and item.get("url"):
                fname = os.path.basename(item["url"])
                
            if fname and not any(i.get("filename") == fname for i in all_items):
                all_items.append({
                    "filename": fname,
                    "titleId": item.get("titleId", "CUSA00000"),
                    "title": item.get("title", fname),
                    "url": item.get("url", ""),
                    "posterUrl": item.get("posterUrl", "https://cdn.jsdelivr.net/gh/nexgen999/evoX-CoreOS@main/assets/evoX-CoreOS_pkg.jpg")
                })

    # Application des surcharges du fichier pegasus_metadata.json
    final_items = apply_pegasus_metadata(all_items)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_items, f, indent=4, ensure_ascii=False)
        
    print(f"    ➔ Catalogue Pegasus généré : {output_path} ({len(final_items)} éléments)")
