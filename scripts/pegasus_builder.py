import os
import json
import subprocess
from scripts.config_rules import PATHS

def get_github_repo_info():
    """Détecte dynamiquement l'URL du dépôt et l'URL CDN jsDelivr universelle."""
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

def load_icon_mapping():
    """Charge le fichier de configuration des icônes personnalisées s'il existe."""
    config_path = os.path.join("assets", "icon", "pegasus_icons.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def generate_pegasus_catalog(pkg_flat, ffpfsc_flat):
    print("🎯 Génération du catalogue JSON pour Pegasus-DL (avec gestion d'icônes dynamiques)...")
    
    output_dir = os.path.join(PATHS.get("json_dir", "json"), "pegasus-dl")
    os.makedirs(output_dir, exist_ok=True)
    
    catalog_path = os.path.join(output_dir, "catalog.json")
    repo_url, jsdelivr_url = get_github_repo_info()
    
    # Chargement du dictionnaire des icônes personnalisées
    icon_mapping = load_icon_mapping()
    
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
            
            # Recherche d'une icône personnalisée pour ce fichier, sinon icône par défaut du type
            custom_icon = icon_mapping.get(title)
            if custom_icon:
                # Si le chemin est relatif dans assets/icon, on construit l'URL CDN complète
                if custom_icon.startswith("http"):
                    poster_url = custom_icon
                else:
                    poster_url = f"{jsdelivr_url}/assets/icon/{custom_icon}"
            else:
                poster_url = f"{jsdelivr_url}/assets/evoX-CoreOS_pkg.jpg"
                
            pkg_entry = {
                "titleId": title_id,
                "title": title,
                "version": version,
                "category": "game",
                "description": description,
                "posterUrl": poster_url,
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
                
            custom_icon = icon_mapping.get(title)
            if custom_icon:
                if custom_icon.startswith("http"):
                    poster_url = custom_icon
                else:
                    poster_url = f"{jsdelivr_url}/assets/icon/{custom_icon}"
            else:
                poster_url = f"{jsdelivr_url}/assets/evoX-CoreOS_ffpfsc.jpg"
                
            ff_entry = {
                "titleId": title_id,
                "title": title,
                "version": version,
                "description": description,
                "posterUrl": poster_url,
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
