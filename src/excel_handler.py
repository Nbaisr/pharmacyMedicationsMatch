import pandas as pd

class ExcelHandler:
    def __init__(self, header):
        self.header = header  # Define si el archivo tiene encabezado o no
        self.data = None

    def get_sheet_names(self, file_path):
        """
        Obtener los nombres de las hojas del archivo Excel.

        :param file_path: Ruta del archivo Excel.
        :return: Lista de nombres de hojas.
        """
        xls = pd.ExcelFile(file_path)
        return xls.sheet_names

    def load_excel(self, file_path, sheet_name):
        """
        Cargar los datos de una hoja específica del archivo Excel.

        :param file_path: Ruta del archivo Excel.
        :param sheet_name: Nombre de la hoja a cargar.
        :return: DataFrame con los datos cargados.
        """
        self.data = pd.read_excel(file_path, sheet_name=sheet_name, header=self.header)
        return self.data
