import os
import sys
import json
import urllib.request
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class PegasusMetadataManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evox-CoreOS - Pegasus Metadata & Icon Manager")
        self.root.geometry("1050x700")
        
        self.config_dir = os.path.join(os.getcwd(), "assets", "icon")
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_path = os.path.join(self.config_dir, "pegasus_metadata.json")
        # Rétrocompatibilité avec l'ancien fichier d'icônes si présent
        self.legacy_config_path = os.path.join(self.config_dir, "pegasus_icons.json")
        
        self.metadata_data = self.load_config()
        self.items_list = []

        # --- TOP FRAME : GitHub Repository Source ---
        repo_frame = ttk.LabelFrame(root, text=" 🌐 GitHub Repository Source ", padding=10)
        repo_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(repo_frame, text="Repository URL:").pack(side="left", padx=5)
        self.ent_repo_url = ttk.Entry(repo_frame, width=40)
        self.ent_repo_url.pack(side="left", padx=5)
        self.ent_repo_url.insert(0, "")
        
        self.btn_scan = ttk.Button(repo_frame, text="🚀 Scan Feeds", command=self.scan_feeds)
        self.btn_scan.pack(side="left", padx=10)

        self.btn_save = ttk.Button(repo_frame, text="💾 Save Configuration", command=self.save_config)
        self.btn_save.pack(side="right", padx=5)

        # --- CENTER FRAME : Data Table ---
        center_frame = ttk.LabelFrame(root, text=" 🎮 Detected Elements (PKG & FFPFSC) ", padding=10)
        center_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("type", "filename", "title_id", "title", "url", "icon")
        self.tree = ttk.Treeview(center_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("type", text="Type")
        self.tree.heading("filename", text="Filename")
        self.tree.heading("title_id", text="Title ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("url", text="Source URL")
        self.tree.heading("icon", text="Icon / Poster")
        
        self.tree.column("type", width=70, anchor="center")
        self.tree.column("filename", width=180)
        self.tree.column("title_id", width=110, anchor="center")
        self.tree.column("title", width=200)
        self.tree.column("url", width=220)
        self.tree.column("icon", width=150)
        
        scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<Double-1>", self.edit_item)

        # --- BOTTOM FRAME : Quick Item Editor ---
        bottom_frame = ttk.LabelFrame(root, text=" ✏️ Edit Selected Element Metadata ", padding=10)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        
        # Grid layout for editor
        ttk.Label(bottom_frame, text="Target File:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.lbl_selected = ttk.Label(bottom_frame, text="None", font=("Arial", 9, "bold"))
        self.lbl_selected.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(bottom_frame, text="Title ID:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.ent_title_id = ttk.Entry(bottom_frame, width=25)
        self.ent_title_id.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(bottom_frame, text="Game Title:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.ent_title = ttk.Entry(bottom_frame, width=35)
        self.ent_title.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        ttk.Label(bottom_frame, text="Icon/Poster File:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.ent_icon = ttk.Entry(bottom_frame, width=25)
        self.ent_icon.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        self.btn_browse = ttk.Button(bottom_frame, text="📂 Browse...", command=self.browse_icon)
        self.btn_browse.grid(row=2, column=2, padx=5, pady=5)
        
        self.btn_apply = ttk.Button(bottom_frame, text="✔️ Apply Changes", command=self.apply_changes)
        self.btn_apply.grid(row=2, column=3, sticky="e", padx=5, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        # Fallback to legacy icon file if it exists
        elif os.path.exists(self.legacy_config_path):
            try:
                with open(self.legacy_config_path, "r", encoding="utf-8") as f:
                    legacy_data = json.load(f)
                    # Convert simple icon dict to rich metadata format
                    migrated = {}
                    for k, v in legacy_data.items():
                        migrated[k] = {"titleId": "", "title": "", "icon": v}
                    return migrated
            except Exception:
                pass
        return {}

    def save_config(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.metadata_data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Success", f"Configuration successfully saved to:\n{self.config_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")

    def scan_feeds(self):
        repo_url = self.ent_repo_url.get().strip()
        if not repo_url:
            messagebox.showwarning("Warning", "Please enter your GitHub repository URL.")
            return

        clean_url = repo_url.rstrip("/").removesuffix(".git")
        parts = clean_url.split("/")
        if len(parts) < 5:
            messagebox.showerror("Error", "Invalid GitHub URL format (Expected: https://github.com/user/repo)")
            return
        
        user, repo = parts[-2], parts[-1]
        
        self.tree.delete(*self.tree.get_children())
        self.items_list = []
        
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
                                    
                                    item_type = "PKG" if "pkg" in path_lower else "FFPFSC"
                                    
                                    def parse_json_data(data):
                                        if isinstance(data, list):
                                            for elem in data:
                                                parse_json_data(elem)
                                        elif isinstance(data, dict):
                                            fname = data.get("filename") or data.get("name")
                                            furl = data.get("url", "")
                                            ftitle_id = data.get("titleId", "")
                                            ftitle = data.get("title", "")
                                            
                                            if fname and isinstance(fname, str) and not fname.startswith("http"):
                                                if not any(i[1] == fname for i in self.items_list):
                                                    # Retrieve overrides from saved config if available
                                                    saved_entry = self.metadata_data.get(fname, {})
                                                    icon = saved_entry.get("icon", "")
                                                    title_id = saved_entry.get("titleId", ftitle_id)
                                                    title = saved_entry.get("title", ftitle)
                                                    
                                                    self.items_list.append((item_type, fname, title_id, title, furl, icon))
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
                
        if not success or not self.items_list:
            messagebox.showerror("Scan Error", "No valid PKG or FFPFSC JSON files found in the remote repository.")
            return

        for row in self.items_list:
            self.tree.insert("", "end", values=row)
            
        messagebox.showinfo("Scan Complete", f"Success! Loaded {len(self.items_list)} elements from GitHub.")

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
            title="Select Icon/Poster Image",
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
        
        # Save to metadata dictionary structure
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