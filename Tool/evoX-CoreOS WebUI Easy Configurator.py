import json
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Configuration de la charte graphique evoX
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue") # On adaptera les boutons en rouge/accentué manuellement

class EvoXConfigurator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("evoX-CoreOS WebUI Easy Configurator")
        self.geometry("900x700")
        
        # Données de configuration en mémoire
        self.config_data = {
            "siteTitle": "evoX-CoreOS WebUI",
            "github": {"user": "", "dataRepository": "", "webuiRepository": ""},
            "sources": {"pldmgr": "", "json": [], "changelog": "", "pegasus": []},
            "webkit": [],
            "ps5_webui": [],
            "releases": {"baseUrl": "", "packs": []},
            "credits": [],
            "socials": []
        }

        # Création des onglets
        self.tabview = ctk.CTkTabview(self, width=850, height=600)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tab_general = self.tabview.add("Général")
        self.tab_store = self.tabview.add("Store & Pegasus")
        self.tab_webkit = self.tabview.add("WebKit & WebUI")
        self.tab_footer = self.tabview.add("Footer & Génération")

        self.init_general_tab()
        self.init_store_tab()
        self.init_webkit_tab()
        self.init_footer_tab()

    def init_general_tab(self):
        # Paramètres globaux
        ctk.CTkLabel(self.tab_general, text="Paramètres du Site", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        
        self.entry_title = self.create_input(self.tab_general, "Titre du site", self.config_data["siteTitle"])
        self.entry_gh_user = self.create_input(self.tab_general, "Utilisateur GitHub")
        self.entry_gh_data = self.create_input(self.tab_general, "Dépôt Data (ex: nexgen999/evoX-CoreOS)")
        self.entry_gh_webui = self.create_input(self.tab_general, "Dépôt WebUI")
        
        ctk.CTkLabel(self.tab_general, text="Sources Principales", font=("Arial", 16, "bold")).pack(pady=(20, 5))
        self.entry_pldmgr = self.create_input(self.tab_general, "URL pldmgr.json")
        self.entry_changelog = self.create_input(self.tab_general, "URL CHANGELOG.md")
        self.entry_releases = self.create_input(self.tab_general, "URL de base des Releases")

    def init_store_tab(self):
        # Générateur générique pour les listes
        self.create_list_manager(self.tab_store, "Fichiers JSON du Store", ["name", "url"], self.config_data["sources"]["json"])
        self.create_list_manager(self.tab_store, "Catalogues Pegasus", ["name", "url"], self.config_data["sources"]["pegasus"])
        self.create_list_manager(self.tab_store, "Packs AIO (Releases)", ["name", "file", "icon"], self.config_data["releases"]["packs"])

    def init_webkit_tab(self):
        self.create_list_manager(self.tab_webkit, "Hôtes WebKit", ["name", "url", "icon", "description"], self.config_data["webkit"])
        self.create_list_manager(self.tab_webkit, "Services WebUI PS5", ["name", "port", "path", "icon", "description"], self.config_data["ps5_webui"])

    def init_footer_tab(self):
        self.create_list_manager(self.tab_footer, "Réseaux Sociaux", ["platform", "url", "icon"], self.config_data["socials"])
        
        # Crédits (Liste simple de strings)
        frame = ctk.CTkFrame(self.tab_footer)
        frame.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(frame, text="Crédits (séparés par des virgules)").pack(anchor="w", padx=10, pady=5)
        self.entry_credits = ctk.CTkEntry(frame, width=800)
        self.entry_credits.pack(padx=10, pady=5)

        # Bouton de génération
        btn_generate = ctk.CTkButton(self.tab_footer, text="Générer config.json", fg_color="#E60033", hover_color="#B30027", font=("Arial", 16, "bold"), command=self.generate_json)
        btn_generate.pack(pady=40)

    # --- Utilitaires de création d'UI ---

    def create_input(self, parent, label_text, default=""):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=2)
        ctk.CTkLabel(frame, text=label_text, width=200, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(frame, width=500)
        entry.insert(0, default)
        entry.pack(side="left", padx=10)
        return entry

    def create_list_manager(self, parent, title, fields, target_array):
        """Crée dynamiquement une interface pour ajouter des éléments à un tableau JSON"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(frame, text=title, font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        input_frame = ctk.CTkFrame(frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=10)
        
        entries = {}
        for field in fields:
            # Petite astuce visuelle pour indiquer comment remplir l'icône
            placeholder = "fa-solid fa-globe ou url" if field == "icon" else field.capitalize()
            e = ctk.CTkEntry(input_frame, placeholder_text=placeholder, width=120)
            e.pack(side="left", padx=5, pady=5)
            entries[field] = e
            
        # Zone d'affichage
        display_box = ctk.CTkTextbox(frame, height=60)
        display_box.pack(fill="x", padx=10, pady=5)
        
        def add_item():
            item = {}
            for k, v in entries.items():
                val = v.get().strip()
                # Conversion du port en entier pour les WebUI
                if k == "port" and val.isdigit():
                    val = int(val)
                item[k] = val
                v.delete(0, 'end')
            
            target_array.append(item)
            display_box.insert("end", f"- {item['name']} ajouté.\n")
            
        btn_add = ctk.CTkButton(input_frame, text="Ajouter", width=80, command=add_item)
        btn_add.pack(side="left", padx=5)

    # --- Génération finale ---

    def generate_json(self):
        # Récupération des champs simples
        self.config_data["siteTitle"] = self.entry_title.get()
        self.config_data["github"]["user"] = self.entry_gh_user.get()
        self.config_data["github"]["dataRepository"] = self.entry_gh_data.get()
        self.config_data["github"]["webuiRepository"] = self.entry_gh_webui.get()
        
        self.config_data["sources"]["pldmgr"] = self.entry_pldmgr.get()
        self.config_data["sources"]["changelog"] = self.entry_changelog.get()
        self.config_data["releases"]["baseUrl"] = self.entry_releases.get()
        
        # Traitement des crédits
        raw_credits = self.entry_credits.get()
        if raw_credits:
            self.config_data["credits"] = [c.strip() for c in raw_credits.split(',')]

        # Sauvegarde
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile="config.json",
            title="Sauvegarder la configuration",
            filetypes=[("Fichiers JSON", "*.json")]
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Succès", f"Le fichier a été généré avec succès :\n{file_path}")

if __name__ == "__main__":
    app = EvoXConfigurator()
    app.mainloop()