# 🛡️ GuardShift-IA

[![Streamlit App](https://img.shields.io/badge/Open%20App-Streamlit-brightgreen?logo=streamlit)](https://guardshift-ai.streamlit.app)

**GuardShift-IA** es una aplicación web que utiliza Inteligencia Artificial para automatizar el procesamiento de turnos laborales registrados a través de mensajes de WhatsApp. Desarrollada con Python, Streamlit y Gemini 1.5 Flash, transforma mensajes copiados en un archivo Word en una planilla Excel limpia y lista para usar.

---

## 🚀 Link de la aplicación

👉 **[guardshift-ai.streamlit.app](https://guardshift-ai.streamlit.app)**

---

## 🔍 PARA REALIZAR LA PRUEBA

En este repositorio se incluye un documento de ejemplo llamado:

📄 **[2025-04-Cobertura Ejemplo.docx](./2025-04-Cobertura%20Ejemplo.docx)**

Este archivo simula los mensajes reales que la empresa **RF Seguridad** recibe por WhatsApp para registrar los turnos del personal.  
Podés usar este archivo para hacer pruebas y comprobar cómo la aplicación extrae la información y genera automáticamente un Excel organizado.

🔽 **Descargá el archivo desde el enlace anterior y usalo en la sección “Process Files” de la aplicación.**

---

## 🧠 ¿Qué problema resuelve?

En **RF Seguridad**, una empresa de seguridad privada, el personal informa sus turnos mediante mensajes de WhatsApp. Estos mensajes contienen:

- 📍 Objetivo (lugar de trabajo)
- 📅 Fecha
- 🕒 Horario
- 👮‍♂️ Nombre y DNI del vigilador
- 🧑‍💼 Supervisor

Este proceso manual es lento, propenso a errores humanos y requiere mucho tiempo de carga.

---

## 🤖 ¿Qué hace GuardShift-IA?

1. **Subís un archivo Word (.docx)** con los mensajes de WhatsApp copiados.
2. La IA analiza y extrae los datos estructurados.
3. Se genera una **planilla Excel (.xlsx)** con la información organizada.

---

## 🔧 Tecnologías utilizadas

- **Lenguaje**: Python 3.11
- **Framework**: Streamlit
- **Procesamiento IA**: Gemini 1.5 Flash
- **Entrada**: Documentos `.docx`
- **Salida**: Archivos `.xlsx`
- **Librerías clave**:
  - `streamlit`
  - `pandas`
  - `python-docx`
  - `re`
  - `google.generativeai`
  - `tempfile`
  - `datetime`
  - `os`

---

## 📥 Instalación local (opcional)

```bash
# 1. Clonar el repositorio
git clone https://github.com/hmfarias/GuardShift-IA.git
cd GuardShift-IA

# 2. Crear entorno virtual (opcional)
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar la clave de API de Gemini
# Crear archivo .streamlit/secrets.toml con el siguiente contenido:

[GOOGLE_API_KEY]
GOOGLE_API_KEY = "TU_API_KEY_AQUÍ"

# 5. Ejecutar la app
streamlit run app.py
```

---

## 📂 Estructura del proyecto

```
GuardShift-IA/
├── guardshift_app.py     # Código principal de la aplicación
├── requirements.txt      # Dependencias del proyecto
├── .gitignore            # Exclusión de archivos sensibles o temporales
├── README.md             # Documentación del proyecto
├── 2025-04-Cobertura Ejemplo.docx # Archivo de ejemplo para testeo
└── .streamlit/
    └── secrets.toml      # Archivo con la API Key de Gemini
```

---

## 🙏 Agradecimientos

Quiero expresar un especial agradecimiento a Norman Beltrán, profesor de la materia Inteligencia Artificial: Prompt Engineering para Programadores, y al tutor Hugo Mon, por su dedicación y acompañamiento.
Gracias por brindarnos el puntapié inicial en el mundo de la Inteligencia Artificial y guiarnos con tanta predisposición en este camino tan valioso para todo programador.

---

## 👨‍💻 Autor

Marcelo Farias
• LinkedIn
• GitHub

---

## 🛡️ Licencia

Este proyecto está bajo la Licencia MIT.
© 2025 Marcelo Farias
