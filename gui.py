import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import subprocess
import pandas as pd
from scraper import extract_data
from config import EXPORT_FILE, BACKUP_FILE

class ScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Commercial Scraper")
        self.root.geometry("700x500")
        

        style = ttk.Style()
        style.configure("TButton", padding=5)
        style.configure("TLabel", font=("Arial", 10))


        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)


        ttk.Label(main_frame, text="Commercial Data Extractor", font=("Arial", 14, "bold")).pack(pady=(0, 10))


        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="URL:").pack(side=tk.LEFT, padx=(0, 10))
        self.url_entry = ttk.Entry(input_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.url_entry.focus()


        self.extract_btn = ttk.Button(main_frame, text="Iniciar Extracción (Enter)", command=self.run_scraper)
        self.extract_btn.pack(pady=10)


        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("title", "price", "stock")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("title", text="Título")
        self.tree.heading("price", text="Precio")
        self.tree.heading("stock", text="Stock")
        
        self.tree.column("title", width=350)
        self.tree.column("price", width=100)
        self.tree.column("stock", width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="Listo para empezar")
        self.status_label = ttk.Label(bottom_frame, textvariable=self.status_var, foreground="gray")
        self.status_label.pack(side=tk.LEFT)
        
        self.download_btn = ttk.Button(bottom_frame, text="Descargar CSV", command=self.download_csv)
        self.download_btn.pack(side=tk.RIGHT)
        
        self.history_btn = ttk.Button(bottom_frame, text="Ver Historial Completo", command=self.open_backup)
        self.history_btn.pack(side=tk.RIGHT, padx=5)


        self.root.bind('<Return>', lambda e: self.run_scraper())
        
        self.handle_session_startup()
        self.load_existing_data()

    def handle_session_startup(self):
        if os.path.exists(EXPORT_FILE):
            response = messagebox.askyesno("Nueva Sesión", "¿Desea iniciar una nueva sesión?\n(Esto limpiará la lista actual, pero mantendrá el historial de backup)")
            if response:
                try:
                    os.remove(EXPORT_FILE)
                except Exception as e:
                    messagebox.showwarning("Aviso", f"No se pudo limpiar la sesión anterior: {str(e)}")

    def load_existing_data(self):
        if os.path.exists(EXPORT_FILE):
            try:
                df = pd.read_csv(EXPORT_FILE)
                for _, row in df.iterrows():
                    self.tree.insert("", tk.END, values=(row["title"], row["price"], row["stock"]))
            except:
                pass

    def run_scraper(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Atención", "Por favor, ingrese una dirección web válida.")
            return

        self.status_var.set("Procesando... por favor espere.")
        self.root.update_idletasks()
        
        try:
            data = extract_data(url)
            self.tree.insert("", tk.END, values=(data["title"], data["price"], data["stock"]))
            self.tree.see(self.tree.get_children()[-1])
            self.status_var.set("¡Éxito! Datos extraídos.")
            self.url_entry.delete(0, tk.END)
        except PermissionError as e:
            self.status_var.set("Archivo bloqueado.")
            messagebox.showwarning("Archivo Abierto", str(e))
        except Exception as e:
            self.status_var.set("Error durante la extracción.")
            messagebox.showerror("Error", f"Ocurrió un problema: {str(e)}")

    def download_csv(self):
        if not os.path.exists(EXPORT_FILE):
            messagebox.showinfo("Sin Datos", "Aún no hay datos para descargar.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="datos_extraidos.csv"
        )
        
        if file_path:
            try:
                shutil.copy2(EXPORT_FILE, file_path)
                messagebox.showinfo("Éxito", f"Archivo guardado correctamente en:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

    def open_backup(self):
        if not os.path.exists(BACKUP_FILE):
            messagebox.showinfo("Sin Historial", "Aún no hay un historial de backup creado.")
            return
        
        self.show_history_window()

    def show_history_window(self):
        history_win = tk.Toplevel(self.root)
        history_win.title("Extraction History")
        history_win.geometry("800x500")
        
        frame = ttk.Frame(history_win, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Historial de Datos Guardados", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        columns = ("title", "price", "stock")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        tree.heading("title", text="Title")
        tree.heading("price", text="Price")
        tree.heading("stock", text="Stock")
        
        tree.column("title", width=450)
        tree.column("price", width=100)
        tree.column("stock", width=100)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        try:
            df = pd.read_csv(BACKUP_FILE)
            for _, row in df.iterrows():
                tree.insert("", tk.END, values=(row["title"], row["price"], row["stock"]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el historial: {str(e)}")
            history_win.destroy()
            return

        ttk.Button(frame, text="Cerrar", command=history_win.destroy).pack(pady=10)

def launch_gui():
    root = tk.Tk()
    app = ScraperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
