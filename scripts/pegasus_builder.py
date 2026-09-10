import os
import json
import subprocess
from scripts.config_rules import PATHS

def get_github_base_url():
    """Détecte dynamiquement l'URL raw GitHub du dépôt courant via les commandes git."""
    try:
        # Récupère l'URL remote origin (supporte les formats HTTPS et SSH)
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True
        )
        url = result.stdout.strip()
        
        # Conversion du format SSH (git@github.com:user/repo.git) en HTTPS
        if url.startswith("git@github.com:"):
            url = url.replace("git@github.com:", "https://github.com/")
            
        # Nettoyage de l'extension .git de fin
        if url.endswith(".git"):
            url = url[:-4]
            
        if "github.com" in url:
            # Retourne l'URL raw pointant vers la branche main/master et le dossier assets
            return f"{url}/raw/main/assets"
    except Exception:
        pass
        
    # Fallback par défaut si git n'est pas initialisé ou accessible
    return "https://raw.githubusercontent.com/nexgen999/evoX-CoreOS/main/assets"

def generate_pegasus_catalog(pkg_flat, ffpfsc_flat):
    print("🎯 Génération du catalogue JSON pour Pegasus-DL...")
    
    output_dir = os.path.join(PATHS.get("json_dir", "json"), "pegasus-dl")
    os.makedirs(output_dir, exist_ok=True)
    
    catalog_path = os.path.join(output_dir, "catalog.json")
    
    # Récupération dynamique de l'URL des assets
    base_url = get_github_base_url()
    print(f"    🔗 URL des assets détectée : {base_url}")
    
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
