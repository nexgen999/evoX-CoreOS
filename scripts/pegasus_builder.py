import os
import json
import subprocess
from scripts.config_rules import PATHS

def get_github_repo_info():
    """Récupère l'URL de base et l'URL brute du dépôt courant via git."""
    repo_url = "https://github.com/nexgen999/evoX-CoreOS"
    jsdelivr_url = "https://cdn.jsdelivr.net/gh/nexgen999/evoX-CoreOS@main"
    
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
            repo_url = url
            parts = url.split("github.com/")
            if len(parts) > 1:
                user_repo = parts[1]
                jsdelivr_url = f"https://cdn.jsdelivr.net/gh/{user_repo}@main"
    except Exception:
        pass
        
    return repo_url, jsdelivr_url

def generate_pegasus_catalog(pkg_flat, ffpfsc_flat):
    print("🎯 Génération du catalogue JSON pour Pegasus-DL (avec catégorie)...")
    
    output_dir = os.path.join(PATHS.get("json_dir", "json"), "pegasus-dl")
    os.makedirs(output_dir, exist_ok=True)
    
    catalog_path = os.path.join(output_dir, "catalog.json")
    repo_url, jsdelivr_url = get_github_repo_info()
    
    packages = []
    
    # Traitement des PKG
    if pkg_flat:
        for item in pkg_flat:
            title = item.get("filename", "Unknown PKG")
            title_id = item.get("titleId", "CUSA00000")
            version = item.get("version", "v1.0.0")
            url = item.get("url", "")
            description = item.get("description", f"Package PKG : {title}")
            
            if not url:
                continue
                
            pkg_entry = {
                "titleId": title_id,
                "title": title,
                "version": version,
                "category": "game",
                "description": description,
                "posterUrl": f"{jsdelivr_url}/assets/evoX-CoreOS_pkg.jpg",
                "downloadSource": repo_url,
                "downloadLinks": [
                    {
                        "name": "Github",
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
            version = item.get("version", "v1.0.0")
            url = item.get("url", "")
            description = item.get("description", f"Fichier FFPFSC : {title}")
            
            if not url:
                continue
                
            ff_entry = {
                "titleId": title_id,
                "title": title,
                "version": version,
                "description": description,
                "posterUrl": f"{jsdelivr_url}/assets/evoX-CoreOS_ffpfsc.jpg",
                "downloadSource": repo_url,
                "downloadLinks": [
                    {
                        "name": "Github",
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
        
    print(f"    ✅ Catalogue Pegasus-DL mis à jour avec succès : {catalog_path} ({len(packages)} éléments)")
