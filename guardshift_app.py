import streamlit as st
import os
import re
import pandas as pd
from docx import Document
from google import genai
from datetime import datetime
import tempfile

# --- Page configuration ---
st.set_page_config(page_title="GuardShift-AI", layout="centered")

# --- API key configuration ---
API_KEY = st.secrets["GOOGLE_API_KEY"] if "GOOGLE_API_KEY" in st.secrets else os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ Missing Google Gemini API key.")
    st.stop()

# --- Gemini client configuration ---
client = genai.Client(api_key=API_KEY)


def verify_gemini_api():
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say hello"
        )
        return "hello" in response.text.lower()
    except Exception as e:
        st.error(f"❌ Gemini API Error: {e}")
        return False


if verify_gemini_api():
    st.success("✅ Gemini API conectada.")
else:
    st.stop()

# --- Sidebar Navigation ---
st.sidebar.title("GuardShift-AI")
section = st.sidebar.radio(
    "Navigation",
    ["Procesar Archivos", "Acerca del Proyecto", "Acerca de mi", "Agradecimientos"]
)

# --- Section: Acerca de mi ---
if section == "Acerca de mi":
    st.title("👤 Acerca de mi")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("profile.png", caption="Marcelo Farias", width=150)

    with col2:
        st.markdown("""
**Marcelo Farias**  
Licenciado en Informática | Desarrollador Web  

Soy Marcelo Farias, licenciado en Informática con estudios en Desarrollo Web (Front-End y Back-End).  

Durante mis 28 años de trayectoria en la Policía de la Provincia, comencé en el área de programación y desarrollo de software, y fui avanzando hacia roles de mayor responsabilidad, donde adquirí sólidas habilidades en liderazgo, gestión de proyectos y toma de decisiones estratégicas.

Actualmente, mi enfoque está completamente orientado al desarrollo web, tanto en el front-end como en el back-end. Manejo tecnologías como:

- **HTML, CSS (Bootstrap y Tailwind)**  
- **JavaScript (React y Next.js)**  
- **Node.js (Express, Websockets, Socket.io)**  
- **MongoDB (Mongoose)** / **MySQL (Sequelize)**  
- **Git**  
- **Scrum**

Mi pasión es crear soluciones eficientes, escalables y centradas en la experiencia del usuario. Esto me motiva a mantenerme en constante aprendizaje y evolución.

Tras haber finalizado mi carrera en la Policía en diciembre de 2018, estoy en la búsqueda de mi primera oportunidad profesional en el mundo del desarrollo web, un ámbito que siempre me ha entusiasmado pero que, hasta ahora, no había podido explorar en profundidad.

Estoy listo para aportar mis conocimientos técnicos, capacidad analítica y experiencia en gestión a equipos dinámicos y desafiantes, mientras continúo creciendo en este apasionante mundo de la tecnología.

---

🔗 **Conectá conmigo:**  
- [LinkedIn](https://www.linkedin.com/in/hugo-marcelo-farias/)  
- [GitHub](https://github.com/hmfarias?tab=repositories)
""")

# --- Section: Acerca del Proyecto ---
elif section == "Acerca del Proyecto":
    st.title("📄 Acerca del Proyecto")
    st.markdown("""
**GuardShift-AI** es una aplicación desarrollada con **Python** y **Streamlit**, que utiliza la inteligencia artificial de **Gemini** para automatizar el procesamiento de turnos de trabajo enviados por **WhatsApp**.

### 🚧 El Problema

En la empresa de seguridad privada **RF Seguridad**, el registro de horas trabajadas por el personal en diferentes contratantes se realiza manualmente, a partir de mensajes de WhatsApp.

Estos mensajes contienen información como:

- Nombre del **objetivo**
- **Fecha**
- **Horario cubierto**
- Nombres y **DNI** de los vigiladores
- Supervisores a cargo

Este proceso es **lento** y propenso a **errores humanos**.

### 🤖 La Solución

GuardShift-AI permite:

1. Subir un archivo **Word** con mensajes copiados de WhatsApp.
2. La IA extrae y organiza los datos automáticamente.
3. Genera un archivo **Excel** listo para usar.

### 🧱 Tecnologías

- **Lenguaje**: Python
- **Framework**: Streamlit
- **IA**: Gemini
- **Entrada**: archivos .docx
- **Salida**: archivos Excel (.xlsx)

### ✅ Ventajas

- **Ahorra tiempo**
- **Reduce errores**
- **Agiliza la gestión**
- **Evita la carga manual**

---
🔄 Transformá tus mensajes de WhatsApp en reportes profesionales en segundos.
""")

# --- Section: Agradecimientos ---
elif section == "Agradecimientos":
    st.title("🙏 Agradecimientos")
    st.markdown("""
Mi más profundo agradecimiento al **Profesor Norman Beltrán**, quien lideró el curso *Inteligencia Artificial: Prompt Engineering para Programadores*.  
Su dedicación, conocimiento y estilo de enseñanza inspirador nos brindaron las herramientas esenciales para dar con confianza nuestros primeros pasos en el fascinante mundo de la Inteligencia Artificial.

Un agradecimiento muy especial también para nuestro tutor, **Hugo Mon**, por su constante apoyo y compromiso.  
Su claridad, predisposición y acompañamiento fueron fundamentales para que este recorrido no solo fuera posible, sino también enriquecedor y sumamente motivador.

Esta experiencia nos abrió nuevas puertas, mostrándonos cómo la IA puede transformar la forma en que pensamos, creamos y resolvemos problemas como programadores.  
Fue mucho más que un curso: fue la chispa que encendió una nueva pasión por explorar y construir con el poder de la inteligencia artificial.

---

🚀 *A ambos, gracias por iluminar el camino hacia adelante.*
""")
    st.image("thanks.png", width=500)

# --- Section: File Processor ---
elif section == "Procesar Archivos":
    st.title("🛡️ GuardShift-AI")
    st.write("Cargar un documento de WhatsApp Word y convertirlo en un archivo Excel limpio.")

    uploaded_file = st.file_uploader("Subir mensajes de WhatsApp (.docx)", type=["docx"])

    if st.button("Procesar Archivo") and uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        doc = Document(tmp_path)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        messages = full_text.split("==============")
        result_data = []

        for message in messages:
            if not message.strip():
                continue

            prompt = f"""
You are an assistant that extracts structured data from unstructured WhatsApp messages.

The message below may include:
- one 'Objetivo'
- one 'Fecha'
- multiple 'DNI + Nombre + Horario'

Extract the data in table format with EXACTLY these columns:
Objetivo | Fecha | DNI | Nombre | Entrada | Salida

Rules:
- Return ONLY the table.
- Do not add explanations.
- Do not add markdown.
- Do not add ``` or extra text.
- 'Horario' or 'Turno' may appear as:
    * 07 a 19
    * 07:30hs a 19:00hs
    * 07/19
- Use 24h format (hh:mm) for Entrada and Salida.
- One 'Horario' may apply to multiple 'DNI + Nombre' lines.
- If multiple 'DNI' exist, repeat Objetivo and Fecha.
- If data is missing, leave the field empty.

Text:
\"\"\"
{message}
\"\"\"
            """

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                raw = response.text.strip()
                lines = [line for line in raw.split("\n") if "|" in line]

                if len(lines) >= 2:
                    headers = [h.strip() for h in lines[0].split("|")]

                    for line in lines[1:]:
                        parts = [p.strip() for p in line.split("|")]

                        if len(parts) == len(headers):
                            row = dict(zip(headers, parts))
                            result_data.append(row)

            except Exception as e:
                st.error(f"❌ Error processing message: {e}")

        if not result_data:
            st.warning("⚠️ No data was extracted.")
        else:
            df = pd.DataFrame(result_data)

            # Normalize expected columns
            expected_columns = ["Objetivo", "Fecha", "DNI", "Nombre", "Entrada", "Salida"]
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ""

            df = df[expected_columns]

            # Clean empty or hyphen-only rows
            df = df[
                ~df.apply(
                    lambda row: all(re.fullmatch(r"[-–—\s]*", str(cell)) for cell in row),
                    axis=1
                )
            ]

            def format_time(value):
                value = str(value).replace("hs", "").replace("HS", "").strip()

                if re.match(r"^\d{1,2}$", value):
                    return f"{int(value):02d}:00"

                if "/" in value:
                    value = value.replace("/", ":")

                match = re.match(r"^(\d{1,2})([:hH]?)(\d{0,2})$", value)
                if match:
                    hour = int(match.group(1))
                    minute = int(match.group(3)) if match.group(3) else 0
                    return f"{hour:02d}:{minute:02d}"

                return value

            df["Entrada"] = df["Entrada"].apply(format_time)
            df["Salida"] = df["Salida"].apply(format_time)

            def format_date(value):
                value = str(value).strip()

                for fmt in ("%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%d-%m-%y"):
                    try:
                        date_obj = datetime.strptime(value, fmt)
                        return date_obj.strftime("%d/%m/%Y")
                    except:
                        continue

                return value

            df["Fecha"] = df["Fecha"].apply(format_date)

            # Save to Excel
            filename = os.path.splitext(uploaded_file.name)[0] + ".xlsx"

            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_xlsx:
                df.to_excel(tmp_xlsx.name, index=False)

                st.success("✅ Archivo procesado con éxito!")
                st.dataframe(df)

                with open(tmp_xlsx.name, "rb") as f:
                    st.download_button(
                        "⬇️ Descargar Archivo Excel",
                        data=f,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
