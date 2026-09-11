import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import re

class OPMLBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EvoX OPML Feed Builder")
        self.root.geometry("950x700")

        # --- Style & Thème ---
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        BG_COLOR = "#2d2d2d"
        FG_COLOR = "#ffffff"
        FRAME_BG = "#383838"
        ACCENT_COLOR = "#007acc"
        ENTRY_BG = "#1e1e1e"
        
        self.root.configure(bg=BG_COLOR)
        
        self.style.configure(".", background=BG_COLOR, foreground=FG_COLOR, font=("Segoe UI", 9))
        self.style.configure("TLabelframe", background=FRAME_BG, foreground=FG_COLOR, borderwidth=1, relief="solid")
        self.style.configure("TLabelframe.Label", background=FRAME_BG, foreground="#00d2ff", font=("Segoe UI", 10, "bold"))
        self.style.configure("TLabel", background=FRAME_BG, foreground=FG_COLOR)
        self.style.configure("TButton", background="#4a4a4a", foreground=FG_COLOR, borderwidth=0, padding=5)
        self.style.map("TButton", background=[("active", ACCENT_COLOR)])
        
        # Correction explicite des couleurs de saisie (Entry) pour éviter le texte blanc sur fond blanc
        self.style.configure("TEntry", fieldbackground=ENTRY_BG, foreground=FG_COLOR, insertcolor=FG_COLOR)
        self.style.configure("TCombobox", fieldbackground=ENTRY_BG, foreground=FG_COLOR, darkcolor=FRAME_BG, lightcolor=FRAME_BG)
        self.style.map("TCombobox", fieldbackground=[("readonly", ENTRY_BG)], foreground=[("readonly", FG_COLOR)])

        self.style.configure("Treeview", background=ENTRY_BG, foreground=FG_COLOR, fieldbackground=ENTRY_BG, rowheight=25)
        self.style.configure("Treeview.Heading", background="#333333", foreground="#00d2ff", font=("Segoe UI", 9, "bold"))
        self.style.map("Treeview", background=[("selected", ACCENT_COLOR)])

        self.current_filepath = None
        self.outlines = []

        # Menu contextuel Clic Droit (Coller)
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Coller", command=self.paste_from_clipboard)

        # --- En-tête / Métadonnées OPML ---
        header_frame = ttk.LabelFrame(self.root, text=" Configuration du Fichier OPML ", padding=10)
        header_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(header_frame, text="Titre de l'OPML (<title>) :").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_var = tk.StringVar(value="demo")
        self.title_entry = ttk.Entry(header_frame, textvariable=self.title_var, width=40)
        self.title_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.bind_context_menu(self.title_entry)

        # --- Formulaire d'entrée ---
        input_frame = ttk.LabelFrame(self.root, text=" Ajouter / Modifier un Flux ou Fichier Direct ", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Ligne 0 : Nom, Type, Auteur
        ttk.Label(input_frame, text="Nom / Titre (text) :").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.item_text_var = tk.StringVar()
        entry_text = ttk.Entry(input_frame, textvariable=self.item_text_var, width=30)
        entry_text.grid(row=0, column=1, sticky="w", padx=5, pady=3)
        self.bind_context_menu(entry_text)

        ttk.Label(input_frame, text="Type :").grid(row=0, column=2, sticky="w", padx=5, pady=3)
        self.item_type_var = tk.StringVar(value="rss")
        type_cb = ttk.Combobox(input_frame, textvariable=self.item_type_var, values=["rss", "file", "atom"], state="readonly", width=10)
        type_cb.grid(row=0, column=3, sticky="w", padx=5, pady=3)

        ttk.Label(input_frame, text="Auteur (author) :").grid(row=0, column=4, sticky="w", padx=5, pady=3)
        self.item_author_var = tk.StringVar()
        entry_author = ttk.Entry(input_frame, textvariable=self.item_author_var, width=25)
        entry_author.grid(row=0, column=5, sticky="w", padx=5, pady=3)
        self.bind_context_menu(entry_author)

        # Ligne 1 : xmlUrl (Détection auto au changement)
        ttk.Label(input_frame, text="URL Flux / Fichier (xmlUrl) :").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.item_xml_var = tk.StringVar()
        self.item_xml_var.trace_add("write", self.auto_fill_from_url)
        entry_xml = ttk.Entry(input_frame, textvariable=self.item_xml_var, width=70)
        entry_xml.grid(row=1, column=1, columnspan=5, sticky="w", padx=5, pady=3)
        self.bind_context_menu(entry_xml)

        # Ligne 2 : htmlUrl
        ttk.Label(input_frame, text="URL Site / Source (htmlUrl) :").grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.item_html_var = tk.StringVar()
        entry_html = ttk.Entry(input_frame, textvariable=self.item_html_var, width=70)
        entry_html.grid(row=2, column=1, columnspan=5, sticky="w", padx=5, pady=3)
        self.bind_context_menu(entry_html)

        # Ligne 3 : Description
        ttk.Label(input_frame, text="Description :").grid(row=3, column=0, sticky="w", padx=5, pady=3)
        self.item_desc_var = tk.StringVar()
        entry_desc = ttk.Entry(input_frame, textvariable=self.item_desc_var, width=70)
        entry_desc.grid(row=3, column=1, columnspan=5, sticky="w", padx=5, pady=3)
        self.bind_context_menu(entry_desc)

        # Boutons Formulaire
        btn_box = ttk.Frame(input_frame)
        btn_box.grid(row=4, column=0, columnspan=6, pady=10)

        ttk.Button(btn_box, text="➕ Ajouter l'élément", command=self.add_item).pack(side="left", padx=5)
        ttk.Button(btn_box, text="🔄 Mettre à jour", command=self.update_item).pack(side="left", padx=5)
        ttk.Button(btn_box, text="🧹 Vider les champs", command=self.clear_fields).pack(side="left", padx=5)

        # --- Tableau des Entrées ---
        list_frame = ttk.LabelFrame(self.root, text=" Entrées du Fichier OPML ", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("text", "type", "xmlUrl", "author", "description")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("text", text="Nom (text)")
        self.tree.heading("type", text="Type")
        self.tree.heading("xmlUrl", text="URL (xmlUrl)")
        self.tree.heading("author", text="Auteur")
        self.tree.heading("description", text="Description")

        self.tree.column("text", width=150)
        self.tree.column("type", width=60, anchor="center")
        self.tree.column("xmlUrl", width=280)
        self.tree.column("author", width=120)
        self.tree.column("description", width=220)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # --- Barre d'actions bas ---
        action_frame = ttk.Frame(self.root, padding=10)
        action_frame.pack(fill="x", padx=10)

        ttk.Button(action_frame, text="❌ Supprimer sélection", command=self.delete_item).pack(side="left", padx=5)
        ttk.Button(action_frame, text="📄 Nouveau OPML", command=self.new_file).pack(side="right", padx=5)
        ttk.Button(action_frame, text="📂 Ouvrir un OPML", command=self.open_file).pack(side="right", padx=5)
        ttk.Button(action_frame, text="💾 Enregistrer l'OPML", command=self.save_file).pack(side="right", padx=5)

    def auto_fill_from_url(self, *args):
        url = self.item_xml_var.get().strip()
        if not url:
            return

        # Pattern pour intercepter GitHub, GitLab, Codeberg, Bitbucket, etc.
        repo_pattern = r"https?://[^/]+/([^/]+)/([^/#?]+)"
        match = re.match(repo_pattern, url)

        if match:
            author, repo_name = match.group(1), match.group(2)
            # Nettoyage des extensions éventuelles (.git, .zip, etc.)
            repo_name = re.sub(r"\.git$", "", repo_name)
            
            # Auto-remplissage si les champs sont vides
            if not self.item_author_var.get():
                self.item_author_var.set(author)
            if not self.item_text_var.get():
                self.item_text_var.set(repo_name)

    def bind_context_menu(self, widget):
        widget.bind("<Button-3>", lambda event: self.show_context_menu(event, widget))

    def show_context_menu(self, event, widget):
        self.focused_widget = widget
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def paste_from_clipboard(self):
        try:
            clipboard_text = self.root.clipboard_get()
            if hasattr(self, "focused_widget") and self.focused_widget:
                self.focused_widget.insert(tk.INSERT, clipboard_text)
        except tk.TclError:
            pass

    def add_item(self):
        text = self.item_text_var.get().strip()
        xml_url = self.item_xml_var.get().strip()
        if not text or not xml_url:
            messagebox.showwarning("Attention", "Les champs Nom et URL (xmlUrl) sont requis.")
            return

        item = {
            "text": text,
            "title": text,
            "type": self.item_type_var.get(),
            "xmlUrl": xml_url,
            "htmlUrl": self.item_html_var.get().strip(),
            "author": self.item_author_var.get().strip(),
            "description": self.item_desc_var.get().strip()
        }
        self.outlines.append(item)
        self.refresh_tree()
        self.clear_fields()

    def update_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un élément à modifier.")
            return
        
        idx = self.tree.index(selected[0])
        text = self.item_text_var.get().strip()
        xml_url = self.item_xml_var.get().strip()

        if not text or not xml_url:
            messagebox.showwarning("Attention", "Les champs Nom et URL (xmlUrl) sont requis.")
            return

        self.outlines[idx] = {
            "text": text,
            "title": text,
            "type": self.item_type_var.get(),
            "xmlUrl": xml_url,
            "htmlUrl": self.item_html_var.get().strip(),
            "author": self.item_author_var.get().strip(),
            "description": self.item_desc_var.get().strip()
        }
        self.refresh_tree()
        self.clear_fields()

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            return
        idx = self.tree.index(selected[0])
        del self.outlines[idx]
        self.refresh_tree()
        self.clear_fields()

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        idx = self.tree.index(selected[0])
        item = self.outlines[idx]

        self.item_text_var.set(item.get("text", ""))
        self.item_type_var.set(item.get("type", "rss"))
        self.item_xml_var.set(item.get("xmlUrl", ""))
        self.item_html_var.set(item.get("htmlUrl", ""))
        self.item_author_var.set(item.get("author", ""))
        self.item_desc_var.set(item.get("description", ""))

    def clear_fields(self):
        self.item_text_var.set("")
        self.item_type_var.set("rss")
        self.item_xml_var.set("")
        self.item_html_var.set("")
        self.item_author_var.set("")
        self.item_desc_var.set("")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.outlines:
            self.tree.insert("", "end", values=(
                entry["text"],
                entry["type"],
                entry["xmlUrl"],
                entry.get("author", ""),
                entry.get("description", "")
            ))

    def new_file(self):
        self.current_filepath = None
        self.title_var.set("demo")
        self.outlines = []
        self.refresh_tree()
        self.clear_fields()

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Fichiers OPML", "*.opml"), ("Fichiers XML", "*.xml"), ("Tous les fichiers", "*.*")])
        if not filepath:
            return

        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            title_node = root.find("./head/title")
            if title_node is not None and title_node.text:
                self.title_var.set(title_node.text)

            self.outlines = []
            for outline in root.findall(".//body/outline"):
                attribs = outline.attrib
                if "xmlUrl" in attribs or "text" in attribs:
                    self.outlines.append({
                        "text": attribs.get("text", attribs.get("title", "")),
                        "title": attribs.get("title", attribs.get("text", "")),
                        "type": attribs.get("type", "rss"),
                        "xmlUrl": attribs.get("xmlUrl", ""),
                        "htmlUrl": attribs.get("htmlUrl", ""),
                        "author": attribs.get("author", ""),
                        "description": attribs.get("description", "")
                    })

            self.current_filepath = filepath
            self.refresh_tree()
            self.clear_fields()
            messagebox.showinfo("Succès", f"Fichier chargé : {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier OPML :\n{str(e)}")

    def save_file(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Attention", "Le titre (<title>) de l'OPML est obligatoire.")
            return

        opml = ET.Element("opml", version="2.0")
        head = ET.SubElement(opml, "head")
        title_elem = ET.SubElement(head, "title")
        title_elem.text = title

        body = ET.SubElement(opml, "body")
        for entry in self.outlines:
            attribs = {
                "text": entry["text"],
                "title": entry["title"],
                "type": entry["type"],
                "xmlUrl": entry["xmlUrl"],
                "author": entry.get("author", ""),
                "description": entry.get("description", "")
            }
            if entry.get("htmlUrl"):
                attribs["htmlUrl"] = entry["htmlUrl"]
            
            ET.SubElement(body, "outline", **attribs)

        raw_string = ET.tostring(opml, encoding="utf-8")
        parsed = minidom.parseString(raw_string)
        pretty_xml = parsed.toprettyxml(indent="  ", encoding="UTF-8").decode("utf-8")

        default_filename = f"{title}.opml"
        
        filepath = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".opml",
            filetypes=[("Fichiers OPML", "*.opml"), ("Tous les fichiers", "*.*")]
        )

        if not filepath:
            return

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(pretty_xml)
            self.current_filepath = filepath
            messagebox.showinfo("Succès", f"Fichier enregistré sous :\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer le fichier :\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OPMLBuilderApp(root)
    root.mainloop()
