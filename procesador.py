import os
import json
from limpieza import  *

def procesar_pdf(ruta_pdf, carpeta_salida="./resultados"):
    """Pipeline completo: PDF → JSON listo para ChromaDB"""
    os.makedirs(carpeta_salida, exist_ok=True)
    nombre = os.path.basename(ruta_pdf).replace('.pdf', '')

    print(f"\n🔄 Procesando: {nombre}.pdf")

    # 1. Extraer
    paginas = extraer_texto_crudo(ruta_pdf)

    # 2. Detectar si es escaneado
    texto_total = sum(p['num_caracteres'] for p in paginas)
    if texto_total < 500:
        print("   ⚠️  PDF posiblemente escaneado — texto muy escaso")
        print("   💡 Considera usar OCR con pytesseract")

    # 3. Limpiar y chunkear
    todos_los_chunks = []
    for pagina in paginas:
        texto_limpio = limpiar_pagina(pagina['texto_crudo'])
        chunks = crear_chunks(texto_limpio, nombre, pagina['pagina'])
        todos_los_chunks.extend(chunks)

    print(f"   🔪 {len(todos_los_chunks)} chunks generados")

    # 4. Guardar como JSON — este es el "formato ChromaDB ready"
    salida = {
        "archivo_origen": f"{nombre}.pdf",
        "total_chunks": len(todos_los_chunks),
        "chunks": todos_los_chunks
    }

    ruta_json = os.path.join(carpeta_salida, f"{nombre}_chunks.json")
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Guardado en: {ruta_json}")
    return ruta_json

# Función que procesa todos los pdfs de una carpeta indicada (default "pdfs")
def procesar_carpeta_pdfs(carpeta_pdfs="./pdfs", carpeta_salida="./resultados"):

    # Verifica si existe la carpeta
    if not os.path.exists(carpeta_pdfs):
        print(f"La carpeta '{carpeta_pdfs}' no existe")
        return []

    # lista en una variable todos los archivos de la carpeta que sean ".pdf"
    archivos_pdf = [file for file in os.listdir(carpeta_pdfs) if file.lower().endswith('.pdf')]

    # Si hay cero archivos pdf retorna un array vacio
    if not archivos_pdf:
        print(f"No hay ningun archivo en pdf en '{carpeta_pdfs}'")
        return []

    # Si hay un archivo pdf o más realiza el procesamiento de los pdfs
    resultados = []
    for archivo in archivos_pdf:
        ruta_pdf = os.path.join(carpeta_pdfs, archivo)
        ruta_json = procesar_pdf(ruta_pdf, carpeta_salida)
        resultados.append(ruta_json)

    print(f"\nProcesados {len(resultados)} PDFs en total")
    return resultados