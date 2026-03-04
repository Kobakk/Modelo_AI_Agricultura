import sys
from procesador import procesar_pdf
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ruta = sys.argv[1] if len(sys.argv) > 1 else "boletin_5_2025.pdf"
    procesar_pdf(ruta)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
