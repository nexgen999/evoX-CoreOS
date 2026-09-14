# 🚀 Note de développement : À propos de evoX-CoreOS

Aujourd'hui, je vais tenter de vous expliquer ce qu'est **evoX-CoreOS** et tout ce qui l'accompagne.

---

## ❓ Qu'est-ce que evoX-CoreOS ?

**evoX-CoreOS** est né d'une version de test de *PS5 Super PLDMGR Auto Updater* dont je me servais pour effectuer des tests à chaque ajout de repository et de règles pour les dépôts.

*PS5 Super PLDMGR Auto Updater* est un repository qui sert à récupérer automatiquement, via GitHub Actions, les fichiers payloads `elf`/`bin` pour la PS5. Il s'utilise avec le *Payloads Manager* de **itsPLK**, et il est devenu au fil du temps ma principale source de dépôt pour être à jour avec toujours plus d'applications.

**evoX-CoreOS** est donc la suite logique et l'évolution de *PS5 Super PLDMGR Auto Updater*. J'ai commencé par réécrire le code pour qu'il soit plus propre au lieu de tenir dans un fichier unique, et pour séparer les tâches afin d'avoir une meilleure gestion des règles de dépôts.

Au fur et à mesure, **evoX-CoreOS** a basculé pour devenir bien plus que ça. 

À présent, le repository ne gère plus seulement les fichiers `elf`/`bin`. Entre les cafés passés devant l'ordinateur et de nouvelles idées, j'ai ajouté de nouvelles fonctions. C'est là que le développement du repository a officiellement évolué vers **evoX-CoreOS**.

---

## 🛠️ Que fait evoX-CoreOS ?

* 📥 Récupération des fichiers `elf`/`bin` et importation dans le dépôt
* 📦 Récupération des fichiers `pkg`
* 📂 Récupération des fichiers `ffpfsc`
* 🗜️ Récupération de fichiers `zip` ou binaires
* 📊 Génération de fichiers JSON de liste d'applications par catégories
* 📡 Génération de listes de flux RSS/OPML pour les réseaux tels que Discord ou applications de news feed pour suivre les mises à jour
* 🔗 Génération de JSON compatible avec **PLDMGR** (pour récupérer les `elf`/`bin` sur la PS5) et **Pegasus-FE** (pour les `pkg` et `ffpfsc`)
* 📝 Génération d'un fichier `CHANGELOG.md` avec un différentiel suivant les listes JSON à chaque build
* 📖 Génération du `README.md` de page de présentation du dépôt GitHub (contient les liens JSON, les flux RSS/OPML, les packs AIO, un tableau avec toutes les applications disponibles, et les crédits)
* 🎁 Génération des packs AIO `.zip` publiés dans les Releases
* ⚡ Génération de zips `latest build` avec URL fixe
* 📋 Génération du changelog des builds zip
* 🧹 Nettoyage automatique des builds : seules les dernières releases pack sont disponibles pour ne pas surcharger le dépôt
* 🌐 Génération d'une page statique web pour GitHub Pages
* 📚 Génération de catalogue Pegasus-DL
* 🎨 Éditeur de métadonnées et icônes pour le catalogue Pegasus-DL interne
* 🔄 Importation de listes JSON tierces pour Pegasus-DL

---

## 🖥️ evoX-CoreOS-WebUI

Mais ce n'est pas tout ! **evoX-CoreOS** a ensuite donné naissance à **evoX-CoreOS-WebUI**, qui a pour but d'être un site web complet plutôt qu'une simple page web (qui sera sûrement bientôt supprimée) et qui regroupe plusieurs services.

Le but de **evoX-CoreOS-WebUI** est d'offrir un beau site vitrine pouvant fonctionner sur GitHub Pages ou sur un serveur web classique. Cela permet de séparer la partie **evoX-CoreOS** (le moteur) et **evoX-CoreOS-WebUI** (la vitrine).

Vous pouvez héberger plusieurs serveurs **evoX-CoreOS** (si jamais un dépôt saute à cause d'une réclamation DMCA ou Sony) et garder votre site personnel ailleurs. Si l'un tombe, il vous reste les autres ! Le projet étant décentralisé, vous êtes plus serein (dans certains pays, les règles sont strictes et les sites web sont souvent effacés ou inaccessibles).

### 🌟 Que fait evoX-CoreOS-WebUI ?

* **🏠 Site vitrine :** Présentation élégante de votre dépôt **evoX-CoreOS**.
* **📰 Onglet News :** Lit le fichier généré `CHANGELOG.md` et vous permet d'afficher les updates tel un site web publiant les mises à jour.
* **📦 Onglet Pack AIO :** Accès aux packs complets *All-In-One* de vos releases (via l'URL fixe *latest*), vous permettant de télécharger toujours le dernier pack à jour contenant tout, pour le partager facilement à vos amis ou à votre communauté.
* **🛒 Onglet Store JSON :** Permet de télécharger depuis votre PC, mobile ou tablette les derniers fichiers directement depuis l'interface web.
* **🎮 Onglet Pegasus :** Contient les listes JSON de divers teams et serveurs. Vous pouvez ajouter votre propre liste, celle de vos amis ou de votre communauté.
* **🌐 Onglet Webkit :** Permet d'ajouter des webkit exploits pour la PS5 et d'accéder ainsi à divers hosts. Depuis votre PS5, allez sur votre site et lancez n'importe quel exploit webkit que vous avez ajouté ; une iframe permet d'injecter facilement l'exploit depuis le navigateur de la console.
* **⚡ Onglet WebUI :** Permet d'ajouter votre liste de services d'accès WebUI en utilisant `ps5_ip:port`, idéal pour regrouper l'accès à toutes les WebUIs de la PS5 sans avoir à retenir le port spécifique de chacune des applications.
* **📖 Onglet Wiki :** Permet d'ajouter des fichiers `.md` et de créer une documentation (pratique pour vos amis ou votre communauté) pour rédiger des tutoriels ou partager des notes.
* **📺 YouTube Creator :** Permet d'ajouter la liste des créateurs web qui partagent des news sur la scène ou des sites spécifiques (pratique pour suivre l'actualité ou trouver un tuto).
  * *Note pour YouTube Creator :* À la base, le lecteur interne permettait d'afficher les vidéos directement depuis le site, mais les limitations trop contraignantes de GitHub et YouTube m'ont contraint à enlever cette fonction.

---

## ⚙️ evoX-CoreOS Manager

Une fois **evoX-CoreOS** et **evoX-CoreOS-WebUI** créés, est né **evoX-CoreOS Manager**, une application pour PC qui permet de gérer l'ensemble de la suite.

### 1️⃣ evoX-CoreOS Options
* Permet de créer la liste de fichiers OPML Feed avec la liste des dépôts.
* Permet la configuration du fichier de métadonnées pour votre flux Pegasus et ses apps.

### 2️⃣ evoX-CoreOS-WebUI
* Permet la configuration du fichier `/web/data/config.json` qui contient l'ensemble des options.
* Gestion de configuration des dépôts maîtres de votre **evoX-CoreOS** et **evoX-CoreOS-WebUI**.
* Gestion de votre `CHANGELOG.md`.
* Gestion des packs AIO (possibilité d'ajouter des fichiers d'URL directe).
* Gestion des listes JSON pour le Store JSON de votre dépôt et ajout d'autres listes d'utilisateurs utilisant **evoX-CoreOS**.
* Gestion des URLs Webkit.
* Gestion des accès WebUI.
* Gestion des pages YouTube Creators.
* Gestion des remerciements.
* Gestion du footer avec vos réseaux sociaux et liens personnels.

### 3️⃣ GitHub Deploy
* Permet de déployer les templates de **evoX-CoreOS** et **evoX-CoreOS-WebUI** facilement (ajoutez simplement votre token GitHub et l'application déploie les deux templates en créant vos propres repositories, que vous pourrez ensuite configurer via le Manager).

### 4️⃣ HTML Bonus "evoX-CoreOS Pegasus Store"
* Cette page, en cours de développement, regroupe vos listes de catalogues JSON ainsi que les listes qui s'auto-mettent à jour depuis **evoX-CoreOS** importées d'autres serveurs.
* Elle vous permet d'avoir tous les jeux et applications sous la main, de les télécharger depuis votre PC/smartphone/tablette et ainsi de profiter du débit maximum de votre connexion internet.
* Tout comme **evoX-CoreOS-WebUI**, cette page étant décentralisée, vous pouvez la mettre sur n'importe quel dépôt de votre choix : elle est déployée en 5 secondes !

---

## ⏱️ GitHub Actions & Pages

* **🔄 Automatisation :** **evoX-CoreOS** s'auto-met à jour via GitHub Actions et Pages toutes les 6 heures pour ne pas surcharger et éviter tout risque de ban sur GitHub (vous pouvez modifier cette fréquence via le fichier `.github/workflows/update.yml` à travers le cron job).
* **🔗 Décentralisation :** La page web **evoX-CoreOS-WebUI** et la page HTML Pegasus, étant décentralisées, lisent toujours leur version la plus à jour à travers les fichiers **evoX-CoreOS** qui sont auto-mis à jour.

---

## 📌 Ce qu'il reste à faire

* [ ] Finir les templates et l'auto-déploiement dans **evoX-CoreOS Manager**.
* [ ] Finir la page web Pegasus Store.
* [☕] Boire du café et avoir d'autres idées.
* [🧪] Des tests, et encore des tests !

---

## ⚠️ Special Note

Je ne suis pas un grand développeur de talent, je prends mon temps pour développer l'ensemble d'**evoX-CoreOS** et cela demande beaucoup d'investissement. 

J'ai des obligations familiales qui m'obligent à m'occuper de ma mère malade, ce qui me prend énormément de temps. De plus, j'ai un vieux PC de plus de 13 ans, ce qui ne me permet pas d'aller aussi vite que si j'avais une configuration moderne.

Je ne demande **aucun don**. Vous pouvez forker à tout moment mes dépôts, les améliorer et les customiser à votre guise.

> 💡 **La règle d'or est simple :** Le partage est gratuit.

---

## 🙏 Remerciements

* Toute la scène PS5
* **itsPLK** qui m'a donné envie de créer ce projet grâce à *PLDMGR*
* La **Team Pegasus** pour son support
* Les amis du web : **master, mustafa, nazky, seregonwar, stonemodder, pippo, la team dlpsteam, phoenixx, vox don** et tant d'autres.
