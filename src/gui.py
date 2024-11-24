import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from threading import Thread
from excel_handler import ExcelHandler
from functions import match_descriptions


class ExcelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Gestión")

        # Obtener el tamaño de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Definir el tamaño de la ventana (doble de grande que antes)
        window_width = 800
        window_height = 400

        # Calcular la posición para centrar la ventana
        position_x = int((screen_width / 2) - (window_width / 2))
        position_y = int((screen_height / 2) - (window_height / 2))

        # Configurar el tamaño y la posición de la ventana
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Crear manejadores para los dos archivos Excel
        self.excel_handler1 = ExcelHandler(header=1)
        self.excel_handler2 = ExcelHandler(header=0)

        # Crear el menú principal
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()

        # Crear y mostrar los botones del menú principal
        tk.Label(self.root, text="Menú Principal", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(self.root, text="Obtener código de medicamentos", command=self.show_medicamento_view).pack(pady=10)
        tk.Button(self.root, text="Corregir Rut", command=self.show_corregir_rut_view).pack(pady=10)
        tk.Button(self.root, text="Salir", command=self.root.quit).pack(pady=10)

    def show_medicamento_view(self):
        self.clear_window()

        # Título y descripción
        tk.Label(self.root, text="Obtener Código de Medicamentos", font=("Helvetica", 16)).pack(pady=20)
        description = ("Esta función permite cargar dos archivos Excel y realizar la comparación de descripciones "
                       "para obtener los códigos correspondientes.")
        self.create_description_text(description)

        # Botones para cargar archivos y comparar
        tk.Button(self.root, text="Cargar Primer Excel", command=self.load_first_excel).pack(pady=10)
        tk.Button(self.root, text="Cargar Segundo Excel", command=self.load_second_excel).pack(pady=10)
        tk.Button(self.root, text="Comparar y Agregar Código", command=self.compare_and_add_code).pack(pady=10)

        # Etiqueta para mostrar la información de los archivos cargados y el estado de la comparación
        self.info_label = tk.Label(self.root, text="")
        self.info_label.pack(pady=10)

        # Etiqueta para mostrar el estado de procesamiento
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)

        # Botón de "Volver"
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=10)

    def show_corregir_rut_view(self):
        self.clear_window()

        # Título y descripción
        tk.Label(self.root, text="Corregir RUT", font=("Helvetica", 16)).pack(pady=20)
        description = "Esta función permite corregir los RUT en un archivo Excel (próximamente)."
        self.create_description_text(description)

        # Botón de "Volver"
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=10)

    def create_description_text(self, text):
        """
        Crear y mostrar el widget de texto con la descripción, con ajuste automático de líneas.
        """
        text_widget = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=4, font=("Helvetica", 12))
        text_widget.pack(pady=10)
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)  # Hacer que el widget sea de solo lectura

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_first_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                sheet_names = self.excel_handler1.get_sheet_names(file_path)
                self.sheet_selection_window(file_path, sheet_names, self.excel_handler1, "Primer")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def load_second_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                sheet_names = self.excel_handler2.get_sheet_names(file_path)
                self.sheet_selection_window(file_path, sheet_names, self.excel_handler2, "Segundo")
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
                self.info_label.config(
                    text=f"{order} Excel cargado: {sheet_name}\nCantidad de registros: {len(handler.data)}")
            else:
                messagebox.showerror("Error", "No se ha seleccionado ninguna hoja")

        tk.Button(sheet_window, text="Seleccionar", command=select_sheet).pack(pady=10)

    def compare_and_add_code(self):
        if not self.excel_handler1.data is None and not self.excel_handler2.data is None:
            try:
                self.status_label.config(text="Procesando...", fg="red")
                self.root.update_idletasks()

                df_result = match_descriptions(self.excel_handler1.data, self.excel_handler2.data)
                save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                         filetypes=[("Excel files", "*.xlsx")])
                if save_path:
                    df_result.to_excel(save_path, index=False)
                    messagebox.showinfo("Éxito", f"Archivo guardado en: {save_path}")
                self.status_label.config(text="")

            except Exception as e:
                self.status_label.config(text="")
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Debe cargar ambos archivos Excel antes de comparar")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelApp(root)
    root.mainloop()
