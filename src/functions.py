import pandas as pd
from difflib import SequenceMatcher

def match_descriptions(df1, df2):
    """
    Función para comparar descripciones entre dos DataFrames y agregar el código correspondiente al segundo DataFrame.
    """
    # Asegurarse de que las descripciones sean cadenas de texto
    df1['Descripción'] = df1['Descripción'].astype(str)
    df2['Descripción'] = df2['Descripción'].astype(str)

    # Crear nuevas columnas en df2 para almacenar el código, descripción y score
    df2['Código'] = 'No encontrado'
    df2['Descripción Original'] = df2['Descripción']
    df2['Score'] = 0
    df2['Alternativa'] = ''
    df2['Código Alternativa'] = ''

    for i, desc2 in df2.iterrows():
        max_score = 0.78
        best_match = None

        # Comparar descripciones para encontrar el mejor match
        for j, desc1 in df1.iterrows():
            # Tomar el mismo número de caracteres de descriptions1 que tiene desc2
            desc2_text = desc2['Descripción']
            desc1_text = desc1['Descripción'][:len(desc2_text)]

            score = SequenceMatcher(None, desc2_text, desc1_text).ratio()
            #print('score')
            if score > max_score:
                max_score = score
                best_match = desc1

        if best_match is not None:
            df2.at[i, 'Código'] = best_match['Código']
            df2.at[i, 'Descripción'] = best_match['Descripción']
            df2.at[i, 'Score'] = max_score

        if df2.at[i, 'Código'] == 'No encontrado':
            # Intentar buscar por la primera palabra
            first_word = desc2['Descripción'].split()[0]
            max_score_alt = 0
            best_match_alt = None

            for j, desc1 in df1.iterrows():
                desc1_text = desc1['Descripción']
                score_alt = SequenceMatcher(None, first_word, desc1_text).ratio()
                if score_alt > max_score_alt:
                    max_score_alt = score_alt
                    best_match_alt = desc1

            if best_match_alt is not None:
                df2.at[i, 'Código Alternativa'] = best_match_alt['Código']
                df2.at[i, 'Alternativa'] = best_match_alt['Descripción']

    return df2
