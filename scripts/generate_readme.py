# scripts/generate_readme.py
import os
from scripts.config_rules import PATHS, BASE_URL

def generate_readme(credits_list, data_store_by_cat=None):
    readme_path = "README.md"
    
    clean_url = BASE_URL.replace("https://", "").replace("http://", "")
    url_parts = clean_url.split("/")
    owner = url_parts[0].split(".")[0]
    repo = url_parts[1] if len(url_parts) > 1 else "evoX-CoreOS"
    
    github_releases_base = f"https://github.com/{owner}/{repo}/releases/download/latest"
    json_base_url = f"{BASE_URL}/json"

    sorted_credits = sorted(list(set(credits_list)))
    credits_content = "\n".join(sorted_credits) if sorted_credits else "_Aucun crédit répertorié._"

    content = f"""<p align="center"><h1>evoX-CoreOS</h1></p>

<p align="center">
  <img src="assets/evoX-CoreOS.png" alt="evoX-CoreOS Banner" width="800">
</p>

---

## 🌟 À Propos du Projet

**evoX-CoreOS** est un écosystème automatisé et intelligent pour PlayStation 5. Il centralise, structure et synchronise en continu les payloads, packages (PKG), fichiers FFPFSC et applications utilitaires de la scène homebrew. Le système intègre une génération dynamique de flux RSS et OPML pour la veille technologique, ainsi qu'une compilation automatisée des packages et des archives AIO (All-In-One).

---

## 🌐 Page Web du Store

Accédez à l'interface web interactive générée automatiquement pour explorer le catalogue :
- **Interface Web Principale (index.html)** : [{BASE_URL}/index.html]({BASE_URL}/index.html)

---

## 🔗 Liste des URLs JSON Globales

Retrouvez l'ensemble des points d'accès aux données JSON du store :
- **Payloads Global** : `{json_base_url}/payloads.json`
- **Packages (PKG) Global** : `{json_base_url}/pkg.json`
- **Fichiers FFPFSC Global** : `{json_base_url}/ffpfsc.json`
- **Applications Global** : `{json_base_url}/apps.json`

---

## 📡 Flux RSS & Veille Technologique

Les flux RSS et fichiers OPML générés automatiquement permettent de suivre en temps réel les mises à jour des dépôts, des outils et des binaires de la scène PS5 :
- **Flux RSS Payloads** : `{BASE_URL}/rss/payloads_rss.xml`
- **Flux RSS Packages (PKG)** : `{BASE_URL}/rss/pkg_rss.xml`
- **Flux RSS Fichiers FFPFSC** : `{BASE_URL}/rss/ffpfsc_rss.xml`
- **Flux RSS Applications** : `{BASE_URL}/rss/apps_rss.xml`
- **Fichier Source OPML Global** : `{BASE_URL}/rss/source_aio.opml`

---

## 📦 Packs Latest à Télécharger (AIO)

- **Pack Payloads AIO** : [{github_releases_base}/PS5_payloads_aio_latest.zip]({github_releases_base}/PS5_payloads_aio_latest.zip)
- **Pack PKG AIO** : [{github_releases_base}/PS5_pkg_aio_latest.zip]({github_releases_base}/PS5_pkg_aio_latest.zip)
- **Pack FFPFSC AIO** : [{github_releases_base}/PS5_ffpfsc_aio_latest.zip]({github_releases_base}/PS5_ffpfsc_aio_latest.zip)
- **Pack Apps AIO** : [{github_releases_base}/PS5_apps_aio_latest.zip]({github_releases_base}/PS5_apps_aio_latest.zip)
- **Ultimate Pack AIO** : [{github_releases_base}/PS5_ultimate_pack_latest.zip]({github_releases_base}/PS5_ultimate_pack_latest.zip)

---
"""

    category_titles = {
        "payloads": "⚡ Payloads (.elf / .bin) Disponibles par Catégorie",
        "pkg": "🎮 Packages PS5 (.pkg) Disponibles",
        "ffpfsc": "📄 Fichiers FFPFSC Disponibles",
        "apps": "🛠️ Applications Utilitaires Disponibles"
    }

    if data_store_by_cat:
        for cat_key, cat_data in data_store_by_cat.items():
            if not cat_data:
                continue
            
            section_title = category_titles.get(cat_key, f"📦 {cat_key.upper()}")
            content += f"## {section_title}\n\n"
            
            for sub_cat_name, items in cat_data.items():
                if not items:
                    continue
                
                content += f"### 📂 {sub_cat_name}\n\n"
                json_filename = f"{sub_cat_name.replace(' ', '_').replace('/', '_')}.json"
                content += f"> **JSON Catégorie** : `{json_base_url}/{cat_key}/{json_filename}`\n\n"
                
                table_lines = []
                if cat_key == "pkg":
                    table_lines.append("| Package | Auteur | Version | Description |")
                    table_lines.append("| :--- | :--- | :--- | :--- |\n") # Ajout d'un saut de ligne ici pour séparer l'en-tête du corps
                    for item in items:
                        if isinstance(item, dict):
                            name = item.get('name', item.get('filename', 'Inconnu'))
                            url = item.get('url', '#')
                            author = item.get('author', 'Inconnu')
                            version = item.get('version', 'v1.0.0')
                            desc = item.get('description', '') or 'Aucune description.'
                            
                            display_name = f"[{name}]({url})" if url and url != '#' else name
                            table_lines.append(f"| {display_name} | {author} | {version} | {desc} |")
                else:
                    table_lines.append("| Application | Version | Empreinte SHA-256 | Description |")
                    table_lines.append("| :--- | :--- | :--- | :--- |\n") # Ajout d'un saut de ligne ici aussi
                    for item in items:
                        if isinstance(item, dict):
                            name = item.get('name', item.get('filename', 'Inconnu'))
                            url = item.get('url', '#')
                            version = item.get('version', 'v1.0.0')
                            sha = item.get('sha256', 'N/A')
                            if sha and len(sha) > 12:
                                sha_short = f"`{sha[:12]}...`"
                            else:
                                sha_short = f"`{sha}`" if sha else "N/A"
                            desc = item.get('description', '') or 'Aucune description.'
                            
                            display_name = f"[{name}]({url})" if url and url != '#' else name
                            table_lines.append(f"| {display_name} | {version} | {sha_short} | {desc} |")
                
                content += "\n".join(table_lines) + "\n\n"
            content += "---\n\n"

    content += f"""## ☕ Crédits & Sources

Ce projet agrège et structure le travail des développeurs de la scène PS5 :

{credits_content}

---
*Mise à jour automatique assurée par GitHub Actions.*
"""

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Génération du README.md terminée avec succès.")

build_readme = generate_readme
