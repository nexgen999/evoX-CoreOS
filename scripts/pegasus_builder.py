import os
import json

def apply_pegasus_metadata(items_list):
    """
    Injecte les métadonnées personnalisées (titleId, title, icône/poster) 
    configurées via l'application Manager avec des vérifications de diagnostic.
    """
    # Résolution absolue du chemin vers assets/icon/pegasus_metadata.json
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.abspath(os.path.join(base_dir, "..", "assets", "icon", "pegasus_metadata.json"))
    
    print(f"    🔍 [DEBUG] Recherche du fichier de métadonnées : {config_path}")
    print(f"    🔍 [DEBUG] Le fichier existe ? {os.path.exists(config_path)}")
    
    metadata = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                print(f"    🔍 [DEBUG] Clés trouvées dans le JSON de config : {list(metadata.keys())}")
        except Exception as e:
            print(f"    ⚠️ [DEBUG] Erreur de lecture du JSON: {e}")
    else:
        # Solution de repli : essayer un autre chemin au cas où le script est lancé depuis la racine
        alt_config_path = os.path.abspath("assets/icon/pegasus_metadata.json")
        if os.path.exists(alt_config_path):
            print(f"    🔍 [DEBUG] Trouvé via le chemin alternatif : {alt_config_path}")
            try:
                with open(alt_config_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                    print(f"    🔍 [DEBUG] Clés trouvées : {list(metadata.keys())}")
            except Exception as e:
                pass

    for item in items_list:
        fname = item.get("filename")
        if not fname and "downloadLinks" in item and item["downloadLinks"]:
            fname = os.path.basename(item["downloadLinks"][0].get("url", ""))
        
        if fname and fname in metadata:
            print(f"    ✅ [DEBUG] Match trouvé pour le fichier : {fname}")
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
            if not fname and "downloadLinks" in item and item["downloadLinks"]:
                fname = os.path.basename(item["downloadLinks"][0].get("url", ""))
            
            if fname:
                item["filename"] = fname
            
            # Évite les doublons
            if fname and not any(i.get("filename") == fname for i in all_items):
                if not item.get("titleId"):
                    item["titleId"] = "CUSA00000"
                if not item.get("posterUrl"):
                    item["posterUrl"] = "https://cdn.jsdelivr.net/gh/nexgen999/evoX-CoreOS@main/assets/evoX-CoreOS_pkg.jpg"
                
                all_items.append(item)

    # Application des surcharges du fichier pegasus_metadata.json
    final_items = apply_pegasus_metadata(all_items)

    # Structure finale du catalogue attendue par Pegasus
    catalog_output = {
        "name": "Evox-CoreOS Catalog",
        "packages": final_items
    }

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(catalog_output, f, indent=4, ensure_ascii=False)
        
    print(f"    ➔ Catalogue Pegasus généré : {output_path} ({len(final_items)} éléments)")
