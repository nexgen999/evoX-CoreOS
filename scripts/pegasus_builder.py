import os
import json
import subprocess
from scripts.config_rules import PATHS

def get_jsdelivr_base_url():
    """Détecte dynamiquement l'URL CDN jsDelivr du dépôt courant via git."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True
        )
        url = result.stdout.strip()
        if url.startswith("git@github.com:"):
            url = url.replace("git@github.com:", "https://github.com/")
        if url.endswith(".git"):
            url = url[:-4]
            
        if "github.com" in url:
            parts = url.split("github.com/")
            if len(parts) > 1:
                user_repo = parts[1]
                return f"https://cdn.jsdelivr.net/gh/{user_repo}@main"
    except Exception:
        pass
        
    return "https://cdn.jsdelivr.net/gh/nexgen999/evoX-CoreOS@main"

def generate_pegasus_catalog(pkg_flat, ffpfsc_flat):
    print("🎯 Génération du catalogue JSON pour Pegasus-DL via CDN...")
    
    output_dir = os.path.join(PATHS.get("json_dir", "json"), "pegasus-dl")
    os.makedirs(output_dir, exist_ok=True)
    
    catalog_path = os.path.join(output_dir, "catalog.json")
    base_url = get_jsdelivr_base_url()
    print(f"    🔗 URL CDN de base détectée : {base_url}")
    
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
                "icon": f"{base_url}/assets/evoX-CoreOS_pkg.jpg",
                "downloadLinks": [
                    {
                        "name": "Direct PKG",
                        "url": url  # Tu peux aussi remplacer par le CDN si le fichier est versionné dans le repo
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
                "icon": f"{base_url}/assets/evoX-CoreOS_ffpfsc.jpg",
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
