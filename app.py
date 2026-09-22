import streamlit as st
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 1. Configuración de la página
st.set_page_config(page_title="Validación Política IAG V11", layout="centered", page_icon="🧭")

# 2. Inicialización de Firebase
if not firebase_admin._apps:
    try:
        # Extraer credenciales desde los secrets de Streamlit Cloud
        cred_dict = dict(st.secrets["firebase"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error de inicialización de Firebase. Revise los Secrets. Detalle: {e}")

# Conectar cliente de base de datos
try:
    db = firestore.client()
except Exception as e:
    db = None
    st.error("No se pudo iniciar el cliente de Firestore.")

# 3. Encabezado y Descarga de Documento
st.title("Validación y Apropiación: Política de uso de IAG")
st.subheader("Versión 11-2026 | Facultad de Ciencias de la Educación")
st.write("""
Este espacio abierto busca recoger sus valoraciones sobre la Versión 11 de la política de uso de IAG. 
Su participación es clave para consolidar un marco que fomente la equidad, la transparencia y el reconocimiento del trabajo humano.
""")

st.markdown("### 📄 Documento de Estudio")
st.write("Descargue y lea la política completa antes de iniciar la validación:")

if os.path.exists("PoliticaV11.pdf"):
    with open("PoliticaV11.pdf", "rb") as pdf_file:
        st.download_button(
            label="📥 Descargar Documento: Política IAG V11",
            data=pdf_file.read(),
            file_name="PoliticaV11.pdf",
            mime="application/pdf"
        )
else:
    st.warning("⚠️ El archivo PoliticaV11.pdf no se encuentra en el repositorio.")

st.markdown("---")

# 4. Formulario de Validación
with st.form("validacion_v11"):
    st.markdown("### 1. Identificación y Contexto")
    nombre = st.text_input("Nombres y apellidos completos")
    correo = st.text_input("Correo institucional")
    rol = st.selectbox("Rol en la Facultad", ["Estudiante de pregrado", "Estudiante de posgrado", "Docente", "Directivo", "Otro"])
    
    st.markdown("---")
    st.markdown("### 2. La Brújula Ética y Clasificación de Datos")
    p2_1 = st.slider("¿Qué tan clara y aplicable resulta la nueva tabla de 'Clasificación de datos'?", 1, 5, 3)
    p2_2 = st.text_area("¿Identifica algún vacío práctico en los cuatro puntos de la brújula (Equidad, Rendición de cuentas, Transparencia, Seguridad) frente a su realidad en el aula?")
    
    st.markdown("---")
    st.markdown("### 3. Niveles de Uso y Declaración Obligatoria")
    p3_1 = st.slider("¿Considera que los 5 niveles propuestos permiten clasificar adecuadamente cualquier interacción académica?", 1, 5, 3)
    p3_2 = st.slider("Evalúe la viabilidad práctica de exigir el nuevo formato obligatorio de 4 campos.", 1, 5, 3)
    p3_3 = st.text_area("¿Qué dificultades anticipa para redactar la 'Intervención del autor' (Aporte propio) en las declaraciones?")
    
    st.markdown("---")
    st.markdown("### 4. Mecanismos de Apropiación Pedagógica")
    p4_1 = st.selectbox("¿Cuál de los siguientes mecanismos considera que tendrá mayor impacto real en la cultura académica?", 
                        ["Declaración del nivel admitido desde el Syllabus", 
                         "Banco institucional de casos (buenas y malas prácticas)", 
                         "Talleres de apropiación socioafectiva e intelectual", 
                         "Evaluación reflexiva en los productos entregados"])
    p4_2 = st.text_area("¿Qué estrategias sugiere para que la verificación de declaraciones no sobrecargue la evaluación docente?")
    
    st.markdown("---")
    st.markdown("### 5. Acciones Restaurativas")
    p5_1 = st.slider("¿Qué tan pertinente considera el cambio de enfoque de 'sanción' a 'acción restaurativa'?", 1, 5, 3)
    p5_2 = st.text_area("¿Considera que el criterio de 'no sostener su trabajo' en una sustentación es suficiente y manejable para el docente?")
    
    st.markdown("---")
    comentarios_finales = st.text_area("¿Tiene alguna otra observación o recomendación específica para la versión definitiva?")
    
    enviado = st.form_submit_button("Enviar validación")

# 5. Lógica de guardado en la nube
if enviado:
    if nombre and correo:
        nueva_respuesta = {
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nombre": nombre,
            "Correo": correo,
            "Rol": rol,
            "Claridad_Datos": p2_1,
            "Vacio_Brujula": p2_2,
            "Viabilidad_Niveles": p3_1,
            "Viabilidad_Declaracion": p3_2,
            "Dificultad_AportePropio": p3_3,
            "Mecanismo_Impacto": p4_1,
            "Estrategia_CargaDocente": p4_2,
            "Pertinencia_Restaurativa": p5_1,
            "Criterio_Sustentacion": p5_2,
            "Comentarios_Finales": comentarios_finales
        }
        
        if db is not None:
            try:
                # Esto crea la colección automáticamente en Firestore y añade el documento
                db.collection("validacion_v11").add(nueva_respuesta)
                st.success("¡Gracias! Sus aportes a la Versión 11 han sido guardados de forma segura en la base de datos institucional.")
            except Exception as e:
                st.error(f"Ocurrió un error al guardar los datos en la nube: {e}")
        else:
            st.error("No hay conexión activa a la base de datos para guardar la respuesta.")
            
    else:
        st.error("Por favor, complete al menos su nombre y correo institucional.")
