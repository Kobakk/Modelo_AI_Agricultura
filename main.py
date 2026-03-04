import sys
import os
from procesador import procesar_pdf
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 1. Capturamos solo el nombre del archivo
    nombre_archivo = sys.argv[1] if len(sys.argv) > 1 else "boletin_5_2025.pdf"

    # 2. Construimos la ruta completa dinámicamente
    ruta_completa = os.path.join("pdfs", nombre_archivo)

    # 3. Le pasamos la variable a la función, no el texto fijo
    procesar_pdf(ruta_completa)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
