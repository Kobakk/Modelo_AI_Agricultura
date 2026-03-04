import re
import fitz

def extraer_texto_crudo(ruta_pdf):
    """Extrae texto página a página con metadatos"""
    doc = fitz.open(ruta_pdf)
    paginas = []

    for num, pagina in enumerate(doc):
        texto = pagina.get_text("text")
        paginas.append({
            "pagina": num + 1,
            "texto_crudo": texto,
            "num_caracteres": len(texto)
        })

    print(f"   📄 {len(paginas)} páginas extraídas")
    return paginas

def limpiar_pagina(texto):
    """Limpieza específica para BOE y documentos gubernamentales"""

    # 1. Palabras cortadas al final de línea (muy común en PDFs)
    texto = re.sub(r'(\w)-\n(\w)', r'\1\2', texto)

    # 2. Eliminar cabeceras/pies de página típicos del BOE
    # "Núm. 5 Miércoles 8 de enero de 2025 Sec. I. Pág. 1234"
    texto = re.sub(r'Núm\.\s*\d+.*?Pág\.\s*\d+', '', texto)

    # 3. Eliminar líneas con solo números (números de página sueltos)
    texto = re.sub(r'^\s*\d+\s*$', '', texto, flags=re.MULTILINE)

    # 4. Colapsar espacios múltiples
    texto = re.sub(r'[ \t]+', ' ', texto)

    # 5. Máximo 2 saltos de línea seguidos
    texto = re.sub(r'\n{3,}', '\n\n', texto)

    # 6. Eliminar caracteres raros / basura de PDF
    texto = re.sub(r'[^\w\s\.,;:()áéíóúÁÉÍÓÚñÑüÜ¿?¡!\-\/\"\'%]', '', texto)

    # 7. Eliminar líneas demasiado cortas (artefactos del PDF)
    lineas = texto.split('\n')
    lineas = [l for l in lineas if len(l.strip()) > 15 or l.strip() == '']
    texto = '\n'.join(lineas)

    return texto.strip()

def crear_chunks(texto, nombre_archivo, pagina, chunk_size=800, overlap=150):
    """Divide el texto en chunks con solapamiento"""
    chunks = []
    paso = chunk_size - overlap

    for i in range(0, len(texto), paso):
        fragmento = texto[i:i + chunk_size]
        if len(fragmento.strip()) > 100:  # descartar chunks vacíos
            chunks.append({
                "texto": fragmento,
                "fuente": nombre_archivo,
                "pagina": pagina,
                "chunk_size": len(fragmento)
            })

    return chunks