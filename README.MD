# RAG Vitícola — Asistente de Boletines Agrícolas de La Rioja

Sistema de **Retrieval-Augmented Generation (RAG)** especializado en normativa y boletines oficiales de agricultura de La Rioja. Permite hacer preguntas en lenguaje natural sobre los documentos y obtener respuestas precisas citando la fuente original.

---

## ¿Qué hace este proyecto?

Toma PDFs oficiales (boletines de agricultura, normativas fitosanitarias) y los convierte en una base de conocimiento consultable mediante lenguaje natural. El modelo **no inventa** — solo responde con lo que está en los documentos.

```
PDFs oficiales
     ↓
Limpieza y chunking (local)
     ↓
Vectorización + ChromaDB (Colab)
     ↓
Gemma 3-4B responde preguntas
     ↓
Interfaz Gradio accesible desde el navegador
```

---

## Estructura del proyecto

```
proyecto_rag/
│
├── pdfs/                        # PDFs originales a procesar
│
├── resultados/                  # JSONs generados (input para Colab)
│   └── boletin_5_2025_chunks.json
│
├── vectordb_rioja/              # Base de datos ChromaDB (generada en Colab)
│
├── limpieza.py                  # Extracción y limpieza de texto de PDFs
├── procesador.py                # Orquesta el pipeline PDF → JSON
├── main.py                      # Punto de entrada CLI (local)
│
└── proyecto_ai_RAG_BOR.ipynb   # Notebook principal (se ejecuta en Colab)
```

---

## Requisitos

### Local (limpieza de PDFs)
```bash
pip install pymupdf
```

### Google Colab (vectorización + modelo + interfaz)
Las siguientes librerías se instalan en las primeras celdas del notebook:
```
transformers, accelerate, bitsandbytes, huggingface_hub
chromadb, sentence-transformers, pymupdf
gradio
```

---

## Paso 1 — Limpiar y preparar los PDFs (en local)

Este paso se hace en tu máquina. Toma los PDFs de la carpeta `pdfs/` y genera archivos JSON listos para vectorizar.

### Procesar un solo PDF
```bash
python main.py boletin_5_2025.pdf
```

### Procesar todos los PDFs de la carpeta `pdfs/`
```bash
python main.py --allpdfs
```

El resultado se guarda en `resultados/boletin_5_2025_chunks.json` con esta estructura:

```json
{
  "archivo_origen": "boletin_5_2025.pdf",
  "total_chunks": 42,
  "chunks": [
    {
      "texto": "fragmento del documento...",
      "fuente": "boletin_5_2025",
      "pagina": 3,
      "chunk_size": 712
    }
  ]
}
```

**¿Qué hace internamente?**
- `limpieza.py` extrae el texto página a página con PyMuPDF
- Elimina cabeceras/pies de página del BOE, números de página sueltos, caracteres basura
- Divide el texto en chunks de 800 caracteres con 150 de solapamiento (overlap) para no perder contexto entre fragmentos

---

## Paso 2 — Subir archivos a Google Colab

Sube a Colab los siguientes archivos:
- Los JSON generados en `resultados/` (ej: `boletin_5_2025_chunks.json`)
- El notebook `proyecto_ai_RAG_BOR.ipynb`

---

## Paso 3 — Ejecutar el notebook en Google Colab

El notebook realiza estas operaciones en orden:

### Celda I — Instalar dependencias
```python
!pip install -U transformers accelerate bitsandbytes huggingface_hub
!pip install chromadb sentence-transformers pymupdf gradio
```

### Celda II — Importar librerías y login HuggingFace
Se necesita un token de HuggingFace para descargar Gemma. Guárdalo en los Secrets de Colab con el nombre `HF_TOKEN`.

### Celda III — Configurar cuantización 4bit
Permite cargar Gemma 3-4B en los 15GB de VRAM gratuitos de Colab (T4).

### Celda IV — Cargar modelo Gemma 3-4B
```python
model_id = "google/gemma-3-4b-it"
# Se carga en 4bit — ocupa ~3-4GB de VRAM
```

### Celda V — Vectorizar los JSONs → ChromaDB
Lee los chunks del JSON, los convierte a vectores con `BAAI/bge-m3` y los almacena en ChromaDB en la carpeta `./vectordb_rioja`.

> ⚠️ Este paso solo hay que ejecutarlo una vez por cada PDF nuevo. Los vectores quedan guardados en disco.

### Celda VI — Conectar a ChromaDB
Reconecta a la base de datos ya creada y define la función `buscar_contexto()` que recupera los fragmentos más relevantes para cada pregunta.

### Celda VII — Inferencia RAG
Función principal: recibe una pregunta, recupera contexto de ChromaDB, construye el prompt y genera la respuesta con Gemma.

```python
mi_pregunta = "¿De qué trata este boletín y cuáles son los puntos principales?"
respuesta_final = generar_respuesta(mi_pregunta)
print(respuesta_final)
```

### Celda VIII — Interfaz gráfica con Gradio
Lanza un chatbot interactivo accesible desde el navegador. Al ejecutar la celda, Colab genera automáticamente una URL pública:

```
Running on public URL: https://xxxxxxxx.gradio.live
```

Cualquier persona con esa URL puede hacer preguntas al modelo mientras la sesión de Colab esté activa.

---

## Notas importantes

**Sobre la privacidad** — Todo el procesamiento ocurre en tu sesión de Colab. Los documentos no salen a ningún servicio externo.

**Sobre la VRAM** — Gemma 3-4B en 4bit ocupa ~3-4GB. El modelo de embeddings `BAAI/bge-m3` ocupa ~2GB adicionales. Con los 15GB de la T4 gratuita de Colab hay margen suficiente.

**Sobre la persistencia** — ChromaDB se guarda en `./vectordb_rioja`. Si la sesión de Colab se reinicia, hay que volver a subir esa carpeta o re-ejecutar la celda de vectorización.

**Sobre añadir nuevos PDFs** — Procesa el nuevo PDF con `python main.py nuevo_boletin.pdf`, sube el JSON a Colab y ejecuta solo la celda de vectorización. El resto no cambia.

---

## Tecnologías utilizadas

| Componente | Tecnología |
|---|---|
| Extracción PDF | PyMuPDF (fitz) |
| Modelo de lenguaje | Google Gemma 3-4B (4bit, HuggingFace) |
| Embeddings | BAAI/bge-m3 (sentence-transformers) |
| Base de datos vectorial | ChromaDB |
| Interfaz de usuario | Gradio |
| Entorno de ejecución | Google Colab (T4 GPU gratuita) |


## creación del entorno (recomendado)

```bash
# Creación del entorno en  la ruta que queramos
python3 -m venv nombre_entorno
#activamos el entorno
.nombre_entorno/ruta_archivo/activate.ps1
#Descargamos las librerias de nustro requirements.txt
pip install -r requirements.txt
```

## Enlazar rama con el git

```bash
git remote add origin "RUTA_SSH" <- importante tener configuraco el SSH en git!!!
```
