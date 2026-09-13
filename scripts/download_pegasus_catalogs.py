import os
import urllib.request

def download_catalogs():
    """
    Télécharge les catalogues Pegasus distants dans le dossier json/pegasus-dl/
    en écrasant les anciens fichiers à chaque mise à jour.
    """
    urls = {
        "dlps.json": "https://pegasus-catalog.fly.dev/catalogs/dlps.json",
        "pippo.json": "https://pegasus-catalog.fly.dev/catalogs/pippo.json",
        "pfs.json": "https://pegasus-catalog.fly.dev/catalogs/pfs.json"
    }

    output_dir = os.path.join("json", "pegasus-dl")
    os.makedirs(output_dir, exist_ok=True)

    for filename, url in urls.items():
        dest_path = os.path.join(output_dir, filename)
        try:
            print(f"Téléchargement de {filename}...")
            urllib.request.urlretrieve(url, dest_path)
            print(f"Succès : {dest_path}")
        except Exception as e:
            print(f"Erreur pour {filename} : {e}")

if __name__ == "__main__":
    download_catalogs()
