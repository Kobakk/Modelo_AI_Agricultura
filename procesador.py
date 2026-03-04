import os
import json
from limpieza import  *

def procesar_pdf(ruta_pdf, carpeta_salida="./pdfs_procesados"):
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




