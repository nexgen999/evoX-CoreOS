import os
import json
import urllib.request

def apply_pegasus_metadata(items_list, config_path="assets/icon/pegasus_metadata.json"):
    """
    Injects custom metadata (titleId, title, icon/poster) configured via the Manager app 
    into the generated Pegasus list items.
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

def build_pegasus_feeds(repo_url, output_path="pegasus_feed_output.json"):
    """
    Scans the GitHub repository feeds for PKG and FFPFSC items, applies custom metadata,
    and builds the final Pegasus-compatible structure.
    """
    clean_url = repo_url.rstrip("/").removesuffix(".git")
    parts = clean_url.split("/")
    if len(parts) < 5:
        print("Erreur : URL GitHub invalide.")
        return
    
    user, repo = parts[-2], parts[-1]
    all_extracted_items = []
    
    success = False
    for branch in ["main", "master"]:
        try:
            tree_url = f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"
            req = urllib.request.Request(tree_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                tree_data = json.loads(response.read().decode())
                
                for item in tree_data.get("tree", []):
                    path = item.get("path", "")
                    path_lower = path.lower()
                    
                    is_target = ("pkg" in path_lower or "ffpfsc" in path_lower)
                    is_excluded = ("payload" in path_lower or "app" in path_lower or "pegasus" in path_lower)
                    
                    if path.endswith(".json") and is_target and not is_excluded:
                        raw_file_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"
                        try:
                            f_req = urllib.request.Request(raw_file_url, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(f_req) as f_res:
                                content = json.loads(f_res.read().decode())
                                
                                def parse_json_data(data):
                                    if isinstance(data, list):
                                        for elem in data:
                                            parse_json_data(elem)
                                    elif isinstance(data, dict):
                                        fname = data.get("filename") or data.get("name")
                                        furl = data.get("url", "")
                                        ftitle_id = data.get("titleId", "")
                                        ftitle = data.get("title", "")
                                        fposter = data.get("posterUrl", "")
                                        
                                        if fname and isinstance(fname, str) and not fname.startswith("http"):
                                            if not any(i.get("filename") == fname for i in all_extracted_items):
                                                all_extracted_items.append({
                                                    "filename": fname,
                                                    "titleId": ftitle_id,
                                                    "title": ftitle,
                                                    "url": furl,
                                                    "posterUrl": fposter
                                                })
                                        for v in data.values():
                                            if isinstance(v, (list, dict)):
                                                parse_json_data(v)
                                                
                                parse_json_data(content)
                        except Exception:
                            continue
                success = True
                break
        except Exception:
            continue
            
    if not success or not all_extracted_items:
        print("Erreur : Aucun élément valide trouvé dans le dépôt distant.")
        return

    # Applique les surcharges locales (titleId, title, icônes)
    final_items = apply_pegasus_metadata(all_extracted_items)

    # Sauvegarde du fichier final généré
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_items, f, indent=4, ensure_ascii=False)
        
    print(f"Succès ! {len(final_items)} éléments traités et exportés vers '{output_path}'.")

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else input("Entrez l'URL du dépôt GitHub : ")
    build_pegasus_feeds(url)
