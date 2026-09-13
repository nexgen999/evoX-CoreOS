import os
import json

def apply_pegasus_metadata(items_list, config_path="assets/icon/pegasus_metadata.json"):
    """
    Injecte les métadonnées personnalisées (titleId, title, icône/poster) 
    configurées via l'application Manager.
    """
    metadata = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        except Exception:
            pass

    for item in items_list:
        filename = item.get("filename")
        if filename in metadata:
            overrides = metadata[filename]
            if overrides.get("titleId"):
                item["titleId"] = overrides["titleId"]
            if overrides.get("title"):
                item["title"] = overrides["title"]
            if overrides.get("icon"):
                item["posterUrl"] = f"assets/icon/{overrides['icon']}"
                
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
            if fname and not any(i.get("filename") == fname for i in all_items):
                all_items.append({
                    "filename": fname,
                    "titleId": item.get("titleId", ""),
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "posterUrl": item.get("posterUrl", "")
                })

    # Application des surcharges du fichier pegasus_metadata.json
    final_items = apply_pegasus_metadata(all_items)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_items, f, indent=4, ensure_ascii=False)
        
    print(f"    ➔ Catalogue Pegasus généré : {output_path} ({len(final_items)} éléments)")
