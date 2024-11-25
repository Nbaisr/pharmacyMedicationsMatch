# pharmacyMedicationsMatch
Programa desarrollado para comparar 2 matrices de datos y buscar similitudes utilizando el algoritmo de distancia de Levenshtein


El objetivo de esta función es tomar dos conjuntos de datos representados como DataFrames (df1 y df2), comparar las descripciones textuales que contienen, y asignar un código (Código) de df1 al DataFrame df2 basado en las coincidencias más cercanas. Si no se encuentra una coincidencia directa, intenta buscar una coincidencia alternativa basada en la primera palabra.

