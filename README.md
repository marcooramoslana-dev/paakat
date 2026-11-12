# Paakat

**Guía turística inteligente para el patrimonio indígena de México.**

Paakat identifica monumentos arqueológicos a partir de una fotografía y devuelve su ficha turística (cultura, ubicación, época y descripción). Está pensado para lentes inteligentes basados en ESP32-CAM: los lentes capturan la imagen, el servidor la reconoce y la web muestra el resultado en el teléfono.

La identificación usa **CLIP zero-shot**: un modelo ya entrenado que compara la foto con descripciones de cada sitio guardadas en la base de datos. No se entrena ningún modelo propio.

---

## Cómo funciona

```
ESP32-CAM ──foto JPG──▶ POST /api/v1/recognize
                              │
                    valida y guarda la imagen
                              │
                 lee sitios y descripciones de MySQL
                              │
                   CLIP compara foto vs. descripciones
                              │
                 guarda el resultado en `recognitions`
                              │
        JSON ◀────────────────┘
          │
     web del teléfono muestra la ficha del monumento
```

1. La ESP32-CAM (o la web) envía una imagen por HTTP.
2. El backend valida el archivo, lo convierte a RGB y lo reduce a 1024 px como máximo.
3. CLIP genera un vector de la imagen y otro por cada descripción (`clip_prompt`) del catálogo.
4. Se calcula la similitud, se aplica softmax y se ordenan las coincidencias.
5. Si la mejor probabilidad supera el umbral (`MIN_CONFIDENCE`), el sitio se marca como identificado.
6. El resultado se guarda en MySQL y se devuelve a la web.

---

## Tecnologías

- **Backend:** FastAPI, Uvicorn, SQLAlchemy 2, PyMySQL
- **Visión:** Transformers + CLIP (`openai/clip-vit-base-patch32`), PyTorch, Pillow
- **Base de datos:** MySQL 8 / MariaDB
- **Frontend:** HTML, CSS y JavaScript sin frameworks ni build
- **Hardware (planeado):** ESP32-CAM

---

## Requisitos

- Python 3.9 o superior (probado en 3.9)
- MySQL 8 o MariaDB
- PyTorch (CPU o CUDA)
- Navegador moderno

En Python 3.9 se fijan `pydantic>=2.10,<2.11` y `transformers>=4.40,<4.46` por compatibilidad con `torch 2.0.x`.

---

## Instalación

### 1. Base de datos

Crea la base y carga los datos. Puedes usar MySQL Workbench o la consola:

```powershell
mysql -u root -p < database\schema.sql
mysql -u root -p < database\seed.sql
```

Esto crea la base `paakat` con 8 culturas y 14 sitios arqueológicos.

### 2. Configuración

```powershell
Copy-Item server\.env.example server\.env
```

Edita `server\.env` con tus credenciales:

```env
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/paakat?charset=utf8mb4
CLIP_MODEL_NAME=openai/clip-vit-base-patch32
CLIP_DEVICE=cpu
MIN_CONFIDENCE=0.30
TOP_K=3
API_KEY=
UPLOAD_DIR=uploads
MAX_UPLOAD_MB=10
CORS_ORIGINS=["*"]
```

### 3. Dependencias

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r server\requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

Para GPU usa el índice CUDA correspondiente en el último comando.

### 4. Arrancar el backend

```powershell
cd server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
```

- API: http://127.0.0.1:8010
- Documentación interactiva: http://127.0.0.1:8010/docs

La primera ejecución carga CLIP en memoria (unos segundos; el modelo se descarga una sola vez).

### 5. Arrancar la web

En otra terminal, desde la raíz del proyecto:

```powershell
python -m http.server 5500 --directory web
```

- Login: http://localhost:5500/login.html
- Aplicación: http://localhost:5500/index.html

La web apunta al puerto `8010`. Si usas otro puerto, cámbialo en **Configuración de conexión** o en `API_PORT` dentro de `web/index.html`.

---

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado de la API, la base y el modelo |
| GET | `/api/v1/elements` | Catálogo de sitios |
| GET | `/api/v1/elements/{slug}` | Detalle de un sitio |
| POST | `/api/v1/recognize` | Reconoce una imagen (`multipart/form-data`) |
| GET | `/api/v1/recognitions` | Historial de reconocimientos |
| GET | `/uploads/...` | Imágenes guardadas |
| GET | `/docs` | Swagger UI |

Ejemplo de reconocimiento:

```powershell
curl.exe -F "file=@C:\fotos\chichen.jpg" -F "device_id=esp32-test" `
  http://127.0.0.1:8010/api/v1/recognize
```

Respuesta:

```json
{
  "recognized": true,
  "label": "Chichen Itza",
  "confidence": 0.87,
  "top_k": [
    { "label": "Chichen Itza", "confidence": 0.87 },
    { "label": "Tulum", "confidence": 0.06 }
  ],
  "element": {
    "name": "Chichen Itza",
    "category": { "name": "Cultura Maya" },
    "location": "Yucatan, Mexico",
    "era": "Clasico Terminal (600-1200 d.C.)",
    "description": "Ciudad maya dominada por la piramide de Kukulcan..."
  },
  "recognition_id": 12
}
```

---

## Base de datos

| Tabla | Contenido |
|---|---|
| `categories` | Culturas (maya, mexica, teotihuacana, zapoteca, totonaca, tolteca, olmeca, purepecha) |
| `elements` | Sitios arqueológicos, con `clip_prompt` en inglés para CLIP |
| `recognitions` | Historial: etiqueta, confianza, imagen, dispositivo y fecha |

Para agregar un sitio nuevo basta con insertarlo en `elements` con su `clip_prompt`; no hay que reentrenar nada.

---

## Estructura del proyecto

```
paakat/
├── database/
│   ├── schema.sql
│   └── seed.sql
├── firmware/
│   └── esp32cam/          (pendiente)
├── server/
│   ├── app/
│   │   ├── api/           rutas y dependencias
│   │   ├── core/          configuración, logging y seguridad
│   │   ├── db/            sesión y repositorios
│   │   ├── models/        tablas SQLAlchemy
│   │   ├── schemas/       modelos Pydantic
│   │   ├── services/      CLIP, imágenes y reconocimiento
│   │   └── utils/         utilidades de imagen
│   ├── uploads/
│   ├── requirements.txt
│   ├── .env.example
│   └── .env
└── web/
    ├── index.html
    ├── login.html
    └── css/
        ├── styles.css
        └── login.css
```

---

## Notas y limitaciones

- **No se entrena un modelo propio.** CLIP ya viene entrenado por OpenAI; aquí se usa en modo zero-shot con descripciones de texto.
- Las probabilidades son **relativas al catálogo**: agregar o quitar sitios cambia la distribución.
- CLIP clasifica la **imagen completa**, no detecta objetos. Fotos con varias pirámides, personas o mucho cielo reducen la precisión.
- La calidad de los `clip_prompt` es la palanca principal para mejorar los resultados.
- El login actual es de demostración en el navegador (`localStorage`); todavía no hay autenticación real en la API.
- El firmware de la ESP32-CAM está pendiente.

---

## Próximos pasos

- Sketch de la ESP32-CAM: captura, WiFi y envío a `/api/v1/recognize`.
- Autenticación real (tabla de usuarios, hash de contraseñas, sesión o JWT).
- Más sitios y prompts más específicos.
- Opcional: modelo especializado (YOLO/ResNet fine-tuned) para mayor precisión, manteniendo el mismo endpoint.
