import os
import json
from scripts.config_rules import PATHS

def generate_pegasus_catalog(pkg_flat, ffpfsc_flat):
    print("🎯 Génération du catalogue JSON pour Pegasus-DL...")
    
    output_dir = os.path.join(PATHS.get("json_dir", "json"), "pegasus-dl")
    os.makedirs(output_dir, exist_ok=True)
    
    catalog_path = os.path.join(output_dir, "catalog.json")
    
    # URL de base brute GitHub pour pointer directement sur les assets du dépôt
    base_url = "https://raw.githubusercontent.com/nexgen999/evox-w2jb/main/assets"
    
    packages = []
    
    # Traitement des PKG
    if pkg_flat:
        for item in pkg_flat:
            title = item.get("filename", "Unknown PKG")
            title_id = item.get("titleId", "CUSA00000")
            version = item.get("version", "1.00")
            url = item.get("url", "")
            
            if not url:
                continue
                
            pkg_entry = {
                "titleId": title_id,
                "title": title,
                "version": version,
                "icon": f"{base_url}/evoX-CoreOS_pkg.jpg",
                "downloadLinks": [
                    {
                        "name": "Direct PKG",
                        "url": url
                    }
                ]
            }
            packages.append(pkg_entry)

    # Traitement des FFPFSC
    if ffpfsc_flat:
        for item in ffpfsc_flat:
            title = item.get("filename", "Unknown FFPFSC")
            title_id = item.get("titleId", "FFPFSC001")
            version = item.get("version", "1.00")
            url = item.get("url", "")
            
            if not url:
                continue
                
            ff_entry = {
                "titleId": title_id,
                "title": title,
                "version": version,
                "icon": f"{base_url}/evoX-CoreOS_ffpfsc.jpg",
                "downloadLinks": [
                    {
                        "name": "Direct FFPFSC",
                        "url": url
                    }
                ]
            }
            packages.append(ff_entry)

    catalog_data = {
        "name": "Evox-CoreOS Catalog",
        "packages": packages
    }

    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=4, ensure_ascii=False)
        
    print(f"    ✅ Catalogue Pegasus-DL généré avec succès : {catalog_path} ({len(packages)} éléments)")
