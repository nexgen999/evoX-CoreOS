import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

FEED_DIR = "feed"

class OPMLManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PS5 Store - OPML Feed Manager")
        self.geometry("1100 x 720")

        self.current_file_path = None
        self.entries_data = []
        self.editing_index = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Gauche) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=260, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.lbl_files = ctk.CTkLabel(self.sidebar_frame, text="📁 Catégories (OPML)", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_files.pack(padx=10, pady=(10, 5))

        self.btn_refresh = ctk.CTkButton(self.sidebar_frame, text="🔄 Rafraîchir la liste", command=self.load_opml_files)
        self.btn_refresh.pack(padx=10, pady=5, fill="x")

        self.btn_new_file = ctk.CTkButton(self.sidebar_frame, text="➕ Nouveau fichier .opml", fg_color="#00ba7c", hover_color="#008f5f", command=self.create_new_opml)
        self.btn_new_file.pack(padx=10, pady=5, fill="x")

        self.files_scrollable = ctk.CTkScrollableFrame(self.sidebar_frame, label_text="Fichiers disponibles")
        self.files_scrollable.pack(padx=10, pady=10, fill="both", expand=True)

        # --- Content Area (Droite) ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.lbl_active_file = ctk.CTkLabel(self.main_frame, text="Sélectionnez un fichier .opml", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_active_file.grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")

        # Formulaire
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="ew")
        self.form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.form_frame, text="Nom / Titre :").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_title = ctk.CTkEntry(self.form_frame, placeholder_text="ex: kstuff_EchoStretch")
        self.entry_title.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Auteur :").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_author = ctk.CTkEntry(self.form_frame, placeholder_text="ex: EchoStretch")
        self.entry_author.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="URL Dépôt / Feed :").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_url = ctk.CTkEntry(self.form_frame, placeholder_text="ex: https://github.com/EchoStretch/kstuff")
        self.entry_url.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Description :").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_desc = ctk.CTkEntry(self.form_frame, placeholder_text="ex: Fnd Kstuff payload for PS5.")
        self.entry_desc.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.btn_action = ctk.CTkButton(self.form_frame, text="➕ Ajouter au fichier", command=self.add_or_update_entry)
        self.btn_action.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        # Liste des éléments
        self.entries_scrollable = ctk.CTkScrollableFrame(self.main_frame, label_text="Dépôts inclus")
        self.entries_scrollable.grid(row=2, column=0, columnspan=2, padx=15, pady=10, sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Enregistrer
        self.btn_save = ctk.CTkButton(self.main_frame, text="💾 Enregistrer au bon format OPML", fg_color="#1da1f2", hover_color="#1a91da", font=ctk.CTkFont(weight="bold"), command=self.save_opml)
        self.btn_save.grid(row=3, column=0, columnspan=2, padx=15, pady=10, sticky="ew")

        self.load_opml_files()

    def load_opml_files(self):
        for widget in self.files_scrollable.winfo_children():
            widget.destroy()

        if not os.path.exists(FEED_DIR):
            os.makedirs(FEED_DIR)

        files = [f for f in os.listdir(FEED_DIR) if f.endswith('.opml')]
        for f in sorted(files):
            btn = ctk.CTkButton(self.files_scrollable, text=f, fg_color="transparent", border_width=1, anchor="w", command=lambda filename=f: self.open_opml_file(filename))
            btn.pack(padx=5, pady=3, fill="x")

    def create_new_opml(self):
        dialog = ctk.CTkInputDialog(text="Nom du fichier (ex: ps5_test.opml) :", title="Nouveau fichier OPML")
        name = dialog.get_input()
        if name:
            if not name.endswith(".opml"):
                name += ".opml"
            file_path = os.path.join(FEED_DIR, name)
            if not os.path.exists(file_path):
                file_title = name.replace(".opml", "")
                
                root = ET.Element("opml", version="2.0")
                head = ET.SubElement(root, "head")
                ET.SubElement(head, "title").text = file_title
                ET.SubElement(root, "body")
                
                xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
                lines = [line for line in xml_str.split("\n") if line.strip()]
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines) + "\n")
                
                self.load_opml_files()
                self.open_opml_file(name)

    def open_opml_file(self, filename):
        self.current_file_path = os.path.join(FEED_DIR, filename)
        self.entries_data.clear()
        self.reset_form()

        try:
            tree = ET.parse(self.current_file_path)
            root = tree.getroot()
            body = root.find("body")

            if body is not None:
                for outline in body.iter("outline"):
                    title = outline.attrib.get("text") or outline.attrib.get("title", "")
                    url = outline.attrib.get("xmlUrl", "")
                    author = outline.attrib.get("author", "")
                    desc = outline.attrib.get("description", "")
                    
                    if url or title:
                        self.entries_data.append({
                            "title": title,
                            "url": url,
                            "author": author,
                            "description": desc
                        })

            self.lbl_active_file.configure(text=f"Édition : {filename} ({len(self.entries_data)} dépôts)")
            self.render_entries()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier OPML : {e}")

    def render_entries(self):
        for widget in self.entries_scrollable.winfo_children():
            widget.destroy()

        for idx, item in enumerate(self.entries_data):
            card = ctk.CTkFrame(self.entries_scrollable)
            card.pack(padx=5, pady=5, fill="x")
            card.grid_columnconfigure(0, weight=1)

            title_str = item['title'] or "Sans Titre"
            author_str = f"👤 {item['author']} | " if item['author'] else ""
            url_str = item['url'] or "Pas d'URL"
            desc_str = f"\n📝 {item['description']}" if item['description'] else ""

            info_text = f"🔹 {title_str}\n{author_str}🔗 {url_str}{desc_str}"
            lbl = ctk.CTkLabel(card, text=info_text, justify="left", anchor="w", wraplength=650)
            lbl.grid(row=0, column=0, padx=10, pady=8, sticky="w")

            actions_frame = ctk.CTkFrame(card, fg_color="transparent")
            actions_frame.grid(row=0, column=1, padx=10, pady=8, sticky="e")

            btn_edit = ctk.CTkButton(actions_frame, text="✏️", width=35, command=lambda i=idx: self.edit_entry(i))
            btn_edit.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(actions_frame, text="🗑️", width=35, fg_color="#d32f2f", hover_color="#9a0007", command=lambda i=idx: self.delete_entry(i))
            btn_del.pack(side="left", padx=2)

    def add_or_update_entry(self):
        if not self.current_file_path:
            messagebox.showwarning("Attention", "Veuillez d'abord sélectionner un fichier .opml.")
            return

        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        url = self.entry_url.get().strip()
        desc = self.entry_desc.get().strip()

        if not title or not url:
            messagebox.showwarning("Attention", "Le Titre et l'URL du dépôt sont obligatoires.")
            return

        entry_dict = {
            "title": title,
            "author": author,
            "url": url,
            "description": desc
        }

        if self.editing_index is not None:
            self.entries_data[self.editing_index] = entry_dict
        else:
            self.entries_data.append(entry_dict)

        filename = os.path.basename(self.current_file_path)
        self.lbl_active_file.configure(text=f"Édition : {filename} ({len(self.entries_data)} dépôts)")
        
        self.reset_form()
        self.render_entries()

    def edit_entry(self, index):
        self.editing_index = index
        item = self.entries_data[index]

        self.entry_title.delete(0, 'end')
        self.entry_title.insert(0, item['title'])

        self.entry_author.delete(0, 'end')
        self.entry_author.insert(0, item['author'])

        self.entry_url.delete(0, 'end')
        self.entry_url.insert(0, item['url'])

        self.entry_desc.delete(0, 'end')
        self.entry_desc.insert(0, item['description'])

        self.btn_action.configure(text="🔄 Mettre à jour", fg_color="#e67e22", hover_color="#d35400")

    def reset_form(self):
        self.editing_index = None
        self.entry_title.delete(0, 'end')
        self.entry_author.delete(0, 'end')
        self.entry_url.delete(0, 'end')
        self.entry_desc.delete(0, 'end')
        self.btn_action.configure(text="➕ Ajouter au fichier", fg_color="#1f538d", hover_color="#14375e")

    def delete_entry(self, index):
        del self.entries_data[index]
        filename = os.path.basename(self.current_file_path)
        self.lbl_active_file.configure(text=f"Édition : {filename} ({len(self.entries_data)} dépôts)")
        self.reset_form()
        self.render_entries()

    def save_opml(self):
        if not self.current_file_path:
            return

        try:
            filename = os.path.basename(self.current_file_path)
            title_head = filename.replace(".opml", "")

            root = ET.Element("opml", version="2.0")
            head = ET.SubElement(root, "head")
            ET.SubElement(head, "title").text = title_head

            body = ET.SubElement(root, "body")
            for item in self.entries_data:
                ET.SubElement(body, "outline", {
                    "text": item["title"],
                    "title": item["title"],
                    "type": "rss",
                    "xmlUrl": item["url"],
                    "author": item["author"],
                    "description": item["description"]
                })

            raw_xml = ET.tostring(root, encoding="utf-8")
            parsed_xml = minidom.parseString(raw_xml)
            pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

            # Nettoyage des lignes vides générées par minidom
            cleaned_lines = [line for line in pretty_xml.split("\n") if line.strip()]

            with open(self.current_file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(cleaned_lines) + "\n")

            messagebox.showinfo("Succès", f"{filename} enregistré au format conforme !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement : {e}")

if __name__ == "__main__":
    app = OPMLManagerApp()
    app.mainloop()