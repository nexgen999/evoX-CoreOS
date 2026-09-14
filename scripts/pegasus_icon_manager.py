import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scripts.fetchers.pkg_fetcher import fetch_pkg_category
from scripts.fetchers.ffpfsc_fetcher import fetch_ffpfsc_category

class PegasusMetadataManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evox-CoreOS - Pegasus Metadata & Icon Manager")
        self.root.geometry("1050x700")
        
        self.config_dir = os.path.join("assets", "icon")
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_path = os.path.join(self.config_dir, "pegasus_metadata.json")
        
        self.metadata_data = self.load_config()
        self.items_list = []

        # --- TOP FRAME : Actions ---
        top_frame = ttk.LabelFrame(root, text=" 📂 Configuration & Scan ", padding=10)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        self.btn_scan = ttk.Button(top_frame, text="Scanner les sources PKG & FFPFSC", command=self.scan_feeds)
        self.btn_scan.pack(side="left", padx=5)
        
        self.btn_save = ttk.Button(top_frame, text="Sauvegarder la configuration", command=self.save_config)
        self.btn_save.pack(side="right", padx=5)

        # --- CENTER FRAME : Tableau ---
        center_frame = ttk.LabelFrame(root, text=" 🎮 Éléments détectés et métadonnées associées ", padding=10)
        center_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("type", "filename", "title_id", "title", "url", "icon")
        self.tree = ttk.Treeview(center_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("type", text="Type")
        self.tree.heading("filename", text="Nom du fichier")
        self.tree.heading("title_id", text="Title ID")
        self.tree.heading("title", text="Titre")
        self.tree.heading("url", text="URL Source")
        self.tree.heading("icon", text="Icône assignée")
        
        self.tree.column("type", width=70, anchor="center")
        self.tree.column("filename", width=180)
        self.tree.column("title_id", width=100, anchor="center")
        self.tree.column("title", width=180)
        self.tree.column("url", width=200)
        self.tree.column("icon", width=150)
        
        scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<Double-1>", self.edit_item)

        # --- BOTTOM FRAME : Édition rapide ---
        bottom_frame = ttk.LabelFrame(root, text=" ✏️ Édition de l'élément sélectionné ", padding=10)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(bottom_frame, text="Fichier :").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.lbl_selected = ttk.Label(bottom_frame, text="Aucun", font=("Arial", 9, "bold"))
        self.lbl_selected.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(bottom_frame, text="Title ID :").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.ent_title_id = ttk.Entry(bottom_frame, width=25)
        self.ent_title_id.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(bottom_frame, text="Titre :").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.ent_title = ttk.Entry(bottom_frame, width=35)
        self.ent_title.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        ttk.Label(bottom_frame, text="Icône :").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.ent_icon = ttk.Entry(bottom_frame, width=25)
        self.ent_icon.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        self.btn_browse = ttk.Button(bottom_frame, text="Parcourir...", command=self.browse_icon)
        self.btn_browse.grid(row=2, column=2, padx=5, pady=5)
        
        self.btn_apply = ttk.Button(bottom_frame, text="Appliquer", command=self.apply_changes)
        self.btn_apply.grid(row=2, column=3, sticky="e", padx=5, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def save_config(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.metadata_data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Succès", f"Configuration enregistrée dans :\n{self.config_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer : {e}")

    def scan_feeds(self):
        self.tree.delete(*self.tree.get_children())
        self.items_list = []
        credits_set = set()
        
        try:
            print("Scan des flux en cours...")
            _, pkg_flat = fetch_pkg_category(credits_set)
            _, ffpfsc_flat = fetch_ffpfsc_category(credits_set)
            
            for item in pkg_flat + ffpfsc_flat:
                fname = item.get("filename")
                if fname:
                    itype = "PKG" if item in pkg_flat else "FFPFSC"
                    saved = self.metadata_data.get(fname, {})
                    
                    title_id = saved.get("titleId", item.get("titleId", ""))
                    title = saved.get("title", item.get("title", ""))
                    icon = saved.get("icon", "")
                    url = item.get("url", "")
                    
                    self.items_list.append((itype, fname, title_id, title, url, icon))
                    
            for row in self.items_list:
                self.tree.insert("", "end", values=row)
                
            messagebox.showinfo("Scan terminé", f"{len(self.items_list)} éléments chargés.")
        except Exception as e:
            messagebox.showerror("Erreur de scan", f"Une erreur est survenue : {e}")

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item_values = self.tree.item(selected[0], "values")
            self.lbl_selected.config(text=item_values[1])
            self.ent_title_id.delete(0, tk.END)
            self.ent_title_id.insert(0, item_values[2])
            self.ent_title.delete(0, tk.END)
            self.ent_title.insert(0, item_values[3])
            self.ent_icon.delete(0, tk.END)
            self.ent_icon.insert(0, item_values[5])

    def browse_icon(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.config_dir,
            title="Sélectionner une icône",
            filetypes=[("Images JPEG/PNG", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            basename = os.path.basename(file_path)
            self.ent_icon.delete(0, tk.END)
            self.ent_icon.insert(0, basename)

    def apply_changes(self):
        selected = self.tree.selection()
        if not selected:
            return
        item_id = selected[0]
        item_values = list(self.tree.item(item_id, "values"))
        
        filename = item_values[1]
        new_title_id = self.ent_title_id.get().strip()
        new_title = self.ent_title.get().strip()
        new_icon = self.ent_icon.get().strip()
        
        item_values[2] = new_title_id
        item_values[3] = new_title
        item_values[5] = new_icon
        self.tree.item(item_id, values=item_values)
        
        self.metadata_data[filename] = {
            "titleId": new_title_id,
            "title": new_title,
            "icon": new_icon
        }

    def edit_item(self, event):
        self.apply_changes()

if __name__ == "__main__":
    root = tk.Tk()
    app = PegasusMetadataManagerApp(root)
    root.mainloop()
