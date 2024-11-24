import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from threading import Thread
from PIL import Image, ImageTk
from excel_handler import ExcelHandler
from functions import match_descriptions


class ExcelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Gestión")

        # Configuración de la ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 800
        window_height = 500
        position_x = int((screen_width / 2) - (window_width / 2))
        position_y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Cargar imagen de fondo
        self.bg_image = Image.open("images/background.jpg")
        self.bg_image = self.bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Canvas para el fondo
        self.canvas = tk.Canvas(self.root, width=window_width, height=window_height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Crear manejadores para los dos archivos Excel
        self.excel_handler1 = ExcelHandler(header=1)
        self.excel_handler2 = ExcelHandler(header=0)

        # Crear el menú principal
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()

        # Asegurar que el canvas existe
        if not hasattr(self, "canvas"):
            self.canvas = tk.Canvas(self.root, width=self.root.winfo_width(), height=self.root.winfo_height())
            self.canvas.pack(fill="both", expand=True)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Añadir etiquetas y botones al canvas
        self.create_label("Menú Principal", 200, 50, font_size=24)
        self.create_button("Obtener código de medicamentos", self.show_medicamento_view, 300, 100)
        self.create_button("Corregir Rut", self.show_corregir_rut_view, 300, 200)
        self.create_button("Salir", self.root.quit, 300, 300)

    def show_medicamento_view(self):
        self.clear_window()

        # Vista para obtener medicamentos
        self.create_label("Obtener Código de Medicamentos", 200, 50, font_size=24)
        description = "Cargue dos archivos Excel y compare las descripciones para obtener los códigos."
        self.create_description_text(description, 200, 100)

        self.create_button("1. Cargar Primer Excel", lambda: self.load_excel(self.excel_handler1, "Primer"), 300, 200)
        self.create_button("2. Cargar Segundo Excel", lambda: self.load_excel(self.excel_handler2, "Segundo"), 300, 270)
        self.create_button("3. Comparar y Agregar Código", self.compare_and_add_code, 300, 340)
        self.create_button("Volver", self.create_main_menu, 300, 410)

    def show_corregir_rut_view(self):
        self.clear_window()

        # Vista para corregir RUT
        self.create_label("Corregir RUT", 200, 50, font_size=24)
        description = "Función para corregir RUT en un archivo Excel (próximamente)."
        self.create_description_text(description, 200, 100)

        self.create_button("Volver", self.create_main_menu, 300, 200)

    def clear_window(self):
        for widget in self.root.winfo_children():
            if widget != self.canvas:  # No destruir el canvas principal
                widget.destroy()

    def create_button(self, text, command, x, y):
        button = tk.Button(
            self.root,
            text=text,
            command=command,
            font=("Helvetica", 12),
            bg="#004D99",
            fg="black",
            activebackground="#0066CC",
            activeforeground="blue",
            relief=tk.RAISED,
            width=20,
            height=2
        )
        self.canvas.create_window(x, y, anchor="nw", window=button)

    def create_label(self, text, x, y, font_size=16, color="white"):
        label = tk.Label(
            self.root,
            text=text,
            font=("Helvetica", font_size, "bold"),
            bg="#004D99",  # Fondo azul oscuro
            fg=color,  # Texto blanco
            padx=10,
            pady=5,
        )
        self.canvas.create_window(x, y, anchor="nw", window=label)

    def create_description_text(self, text, x, y):
        text_widget = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=5, font=("Helvetica", 12))
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)  # Solo lectura
        self.canvas.create_window(x, y, anchor="nw", window=text_widget)

    def load_excel(self, handler, order):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                sheet_names = handler.get_sheet_names(file_path)
                self.sheet_selection_window(file_path, sheet_names, handler, order)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def sheet_selection_window(self, file_path, sheet_names, handler, order):
        sheet_window = tk.Toplevel(self.root)
        sheet_window.title(f"Seleccionar Hoja ({order} Excel)")

        tk.Label(sheet_window, text="Seleccionar Hoja:").pack(pady=10)
        sheet_listbox = tk.Listbox(sheet_window)
        for sheet in sheet_names:
            sheet_listbox.insert(tk.END, sheet)
        sheet_listbox.pack(pady=10)

        def select_sheet():
            selection = sheet_listbox.curselection()
            if selection:
                sheet_name = sheet_listbox.get(selection)
                sheet_window.destroy()
                handler.load_excel(file_path, sheet_name)
            else:
                messagebox.showerror("Error", "No se seleccionó ninguna hoja")

        tk.Button(sheet_window, text="Seleccionar", command=select_sheet).pack(pady=10)

    def compare_and_add_code(self):
        if self.excel_handler1.data is not None and self.excel_handler2.data is not None:
            try:
                df_result = match_descriptions(self.excel_handler1.data, self.excel_handler2.data)
                save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                         filetypes=[("Excel files", "*.xlsx")])
                if save_path:
                    df_result.to_excel(save_path, index=False)
                    messagebox.showinfo("Éxito", f"Archivo guardado en: {save_path}")
                    self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Debe cargar ambos archivos Excel antes de comparar")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelApp(root)
    root.mainloop()