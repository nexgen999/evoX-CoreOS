# 🚀 Dev Note: About evoX-CoreOS

Today, I'll try to explain what **evoX-CoreOS** is and everything that comes with it.

---

## ❓ What is evoX-CoreOS?

**evoX-CoreOS** was born from a test version of *PS5 Super PLDMGR Auto Updater*, which I used to run tests whenever I added repositories and repository rules.

*PS5 Super PLDMGR Auto Updater* is a repository used to automatically fetch `elf`/`bin` payload files for the PS5 via GitHub Actions. It is used with **itsPLK**'s *Payloads Manager*, and over time it became my main source repository to stay up-to-date with more and more applications.

**evoX-CoreOS** is therefore the logical continuation and evolution of *PS5 Super PLDMGR Auto Updater*. I started by rewriting the code to make it cleaner instead of keeping it in a single file, and to separate tasks for better repository rule management.

As time went on, **evoX-CoreOS** evolved to become much more than that.

Now, the repository no longer just manages `elf`/`bin` files. Between cups of coffee spent in front of the computer and new ideas, I added new features. That is when the repository development officially transitioned into **evoX-CoreOS**.

---

## 🛠️ What does evoX-CoreOS do?

* 📥 Fetching `elf`/`bin` files and importing them into the repository
* 📦 Fetching `pkg` files
* 📂 Fetching `ffpfsc` files
* 🗜️ Fetching `zip` or binary files
* 📊 Generating category-based application list JSON files
* 📡 Generating RSS/OPML feed lists for networks like Discord or news feed apps to track updates
* 🔗 Generating JSON compatible with **PLDMGR** (to retrieve `elf`/`bin` files on the PS5) and **Pegasus-FE** (for `pkg` and `ffpfsc`)
* 📝 Generating a `CHANGELOG.md` file with a differential based on JSON lists at each build
* 📖 Generating the `README.md` presentation page for the GitHub repository (containing JSON links, RSS/OPML feeds, AIO packs, a table with all available applications, and credits)
* 🎁 Generating AIO `.zip` packs published in Releases
* ⚡ Generating `latest build` zips with fixed URLs
* 📋 Generating the changelog for zip builds
* 🧹 Automatic build cleanup: only the latest pack releases are kept to avoid overloading the repository
* 🌐 Generating a static web page for GitHub Pages
* 📚 Generating Pegasus-DL catalogs
* 🎨 Metadata and icon editor for the internal Pegasus-DL catalog
* 🔄 Importing third-party JSON lists for Pegasus-DL

---

## 🖥️ evoX-CoreOS-WebUI

But that's not all! **evoX-CoreOS** then gave birth to **evoX-CoreOS-WebUI**, which aims to be a complete website rather than a simple web page (which will surely be removed soon) and groups several services together.

The goal of **evoX-CoreOS-WebUI** is to offer a nice showcase website that can run on GitHub Pages or a classic web server. This separates the **evoX-CoreOS** part (the engine) from **evoX-CoreOS-WebUI** (the storefront).

You can host multiple **evoX-CoreOS** servers (in case one repository gets taken down due to a DMCA or Sony takedown) and keep your personal site elsewhere. If one goes down, you still have the rest! Because the project is decentralized, you have greater peace of mind (in some countries rules are strict, and websites are often deleted or inaccessible).

### 🌟 What does evoX-CoreOS-WebUI do?

* **🏠 Showcase Site:** Elegant presentation of your **evoX-CoreOS** repository.
* **📰 News Tab:** Reads the generated `CHANGELOG.md` file and allows you to display updates like a website publishing patch notes.
* **📦 Pack AIO Tab:** Access to the complete *All-In-One* packs of your releases (via the fixed *latest* URL), allowing you to always download the latest up-to-date pack containing everything, for easy sharing with friends or your community.
* **🛒 Store JSON Tab:** Allows you to download the latest files directly from the web interface using your PC, mobile device, or tablet.
* **🎮 Pegasus Tab:** Contains JSON lists from various teams and servers. You can add your own list, or lists from friends and your community.
* **🌐 Webkit Tab:** Allows you to add PS5 webkit exploits and access various hosts. From your PS5, go to your site and launch any added webkit exploit; an iframe makes it easy to inject payloads from the console's browser.
* **⚡ WebUI Tab:** Allows you to add your list of WebUI access services using `ps5_ip:port`, making it easy to group access to all PS5 WebUIs without having to remember the specific port for each application.
* **📖 Wiki Tab:** Allows you to add `.md` files to build documentation (handy for friends or your community) to write tutorials or share notes.
* **📺 YouTube Creator:** Allows you to add a list of web creators who share scene news or specific sites (handy for following news or finding tutorials).
  * *Note for YouTube Creator:* Originally, the internal player allowed playing videos directly from the site, but strict limitations from GitHub and YouTube forced me to remove this feature.

---

## ⚙️ evoX-CoreOS Manager

Once **evoX-CoreOS** and **evoX-CoreOS-WebUI** were created, **evoX-CoreOS Manager** was born—a PC application to manage the entire **evoX-CoreOS** and **evoX-CoreOS-WebUI** suite.

### 1️⃣ evoX-CoreOS Options
* Creates the OPML feed file list containing repository links.
* Configures metadata files for your Pegasus feed and its apps.

### 2️⃣ evoX-CoreOS-WebUI
* Configures the `/web/data/config.json` file which contains all options.
* Manages configuration for your master **evoX-CoreOS** and **evoX-CoreOS-WebUI** repositories.
* Manages your `CHANGELOG.md`.
* Manages AIO packs (with options to add direct URL files).
* Manages JSON lists for your repository's JSON Store and adds other lists from users running **evoX-CoreOS**.
* Manages Webkit URLs.
* Manages WebUI access links.
* Manages YouTube Creator pages.
* Manages acknowledgments.
* Manages the footer with social media links and personal URLs.

### 3️⃣ GitHub Deploy
* Deploys **evoX-CoreOS** and **evoX-CoreOS-WebUI** templates easily (just add your GitHub token and the app deploys both templates, creating your own repositories which you can then configure via the Manager).

### 4️⃣ HTML Bonus "evoX-CoreOS Pegasus Store"
* This page, currently under development, groups your catalog JSON lists alongside self-updating lists imported from other **evoX-CoreOS** servers.
* It lets you access all games and apps in one place, download them from your PC/smartphone/tablet, and make the most of your internet connection's maximum bandwidth.
* Just like **evoX-CoreOS-WebUI**, this page is decentralized, meaning you can put it on any repository of your choice and have it deployed in 5 seconds!

---

## ⏱️ GitHub Actions & Pages

* **🔄 Automation:** **evoX-CoreOS** auto-updates via GitHub Actions and Pages every 6 hours to prevent overloading and avoid ban risks on GitHub (you can change this frequency via the `.github/workflows/update.yml` cron job).
* **🔗 Decentralization:** The **evoX-CoreOS-WebUI** web page and Pegasus HTML page are decentralized, always reading their most up-to-date versions directly from the auto-updating **evoX-CoreOS** files.

---

## 📌 What's Left to Do

* [ ] Finish templates and auto-deployment in **evoX-CoreOS Manager**.
* [ ] Finish the Pegasus Store web page.
* [☕] Drink coffee and come up with more ideas.
* [🧪] Testing, and more testing!

---

## ⚠️ Special Note

I am not a master developer; I take my time developing **evoX-CoreOS**, and it takes a lot of dedication and time.

I have family obligations that require me to take care of my sick mother, which takes up a huge amount of my time. Additionally, I use an old 13+ year-old PC, which prevents me from moving as fast as I would with a modern setup.

I don't ask for **any donations**. You are free to fork my repositories at any time, improve them, and customize them however you like.

> 💡 **The golden rule is simple:** Sharing is free.

---

## 🙏 Acknowledgments

* The entire PS5 scene
* **itsPLK** for inspiring me to create this project through *PLDMGR*
* The **Pegasus Team** for their support
* Web friends: **master, mustafa, nazky, seregonwar, stonemodder, pippo, the dlpsteam team, phoenixx, vox don**, and many others.
