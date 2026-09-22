import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai

# Configuración inicial
st.set_page_config(page_title="Agente y Validación - Política IAG V11", layout="centered", page_icon="🧭")

# --- CONFIGURACIÓN DE LA API DE GEMINI ---
# Extrae la llave de seguridad desde los Secrets de Streamlit
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Instrucción central para acotar al agente al documento
    instruccion_sistema = """
    Eres un asistente pedagógico experto en la 'Política de uso de la Inteligencia Artificial Generativa (IAG) en actividades académicas - Versión 11-2026' de la Facultad de Ciencias de la Educación de la Universidad de La Salle.
    Tu misión es responder dudas de docentes y estudiantes sobre esta política, orientando específicamente sobre:
    1. La Brújula de Uso Responsable (Equidad, Rendición de cuentas, Transparencia, Seguridad).
    2. La tabla de Clasificación de Datos.
    3. La escala de 5 niveles de uso y su declaración obligatoria.
    4. Las Acciones Restaurativas en caso de prácticas inadecuadas.
    Sé amable, pedagógico y basa tus respuestas EXCLUSIVAMENTE en el marco de la Universidad de La Salle. No inventes reglas que no estén en la política.
    """
    
    # Inicializar el modelo con la instrucción
    modelo = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=instruccion_sistema
    )
except Exception as e:
    st.error("⚠️ Falta configurar la llave GOOGLE_API_KEY en los Secrets de Streamlit.")

# --- INTERFAZ ---
st.title("🧭 Agente de Consulta: Política IAG (Versión 11)")
st.write("Antes de proceder a la validación, converse con este asistente para resolver cualquier duda sobre las directrices, los niveles de uso o la declaración de autoría.")

# --- INTERFAZ ---
st.title("🧭 Agente de Consulta: Política IAG (Versión 11)")
st.write("Antes de proceder a la validación, converse con este asistente para resolver cualquier duda sobre las directrices, los niveles de uso o la declaración de autoría.")

# --- NUEVO: BOTÓN DE DESCARGA DEL PDF ---
st.markdown("### 📄 Documento de Estudio")
st.write("Descargue y lea la política completa antes de iniciar la validación:")

# Verificamos que el archivo exista para que la app no falle si olvidas subirlo
if os.path.exists("PoliticaV11.pdf"):
    with open("PoliticaV11.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    
    st.download_button(
        label="📥 Descargar Documento: Política IAG V11",
        data=PDFbyte,
        file_name="PoliticaV11.pdf",
        mime="application/pdf"
    )
else:
    st.warning("⚠️ El archivo PoliticaV11.pdf no se encuentra en el repositorio.")

st.markdown("---") # Una línea divisoria visual

# ... (Aquí continúa tu código del historial de chat) ...

# Inicializar variables de sesión
if "chat_session" not in st.session_state:
    try:
        st.session_state.chat_session = modelo.start_chat(history=[])
    except:
        pass
if "mensajes_ui" not in st.session_state:
    st.session_state.mensajes_ui = []
if "interacciones" not in st.session_state:
    st.session_state.interacciones = 0

# Mostrar el historial de mensajes en la interfaz
for msg in st.session_state.mensajes_ui:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input del chat
if prompt := st.chat_input("Ej: ¿Qué diferencia hay entre el Nivel 4 y el Nivel 5?"):
    # Mostrar el mensaje del usuario
    st.session_state.mensajes_ui.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Enviar a Gemini y recibir respuesta
    with st.chat_message("assistant"):
        with st.spinner("Revisando la política..."):
            try:
                respuesta = st.session_state.chat_session.send_message(prompt)
                st.markdown(respuesta.text)
                st.session_state.mensajes_ui.append({"role": "assistant", "content": respuesta.text})
                st.session_state.interacciones += 1
            except Exception as e:
                st.error("Error al conectar con la IA. Verifique la API Key.")

# --- FASE 2: DESBLOQUEO DEL FORMULARIO ---
st.markdown("---")

if st.session_state.interacciones >= 2:
    st.success("✅ ¡Gracias por explorar el documento! Ahora lo invitamos a dejar su validación final para apropiar este conocimiento.")
    
    with st.form("validacion_v11"):
        st.markdown("### 1. Identificación y Contexto")
        nombre = st.text_input("Nombres y apellidos completos")
        correo = st.text_input("Correo institucional")
        rol = st.selectbox("Rol en la Facultad", ["Estudiante de pregrado", "Estudiante de posgrado", "Docente", "Directivo", "Otro"])
        
        st.markdown("---")
        st.markdown("### 2. Valoración de la Política")
        p2_1 = st.slider("¿Qué tan clara y aplicable resulta la nueva tabla de 'Clasificación de datos'?", 1, 5, 3)
        p3_1 = st.slider("¿Considera que los 5 niveles propuestos permiten clasificar adecuadamente las interacciones con la IAG?", 1, 5, 3)
        p3_2 = st.slider("Evalúe la viabilidad práctica de exigir el nuevo formato obligatorio de declaración de uso en las entregas.", 1, 5, 3)
        
        p4_1 = st.selectbox("¿Cuál mecanismo tendrá mayor impacto real en la cultura académica?", 
                            ["Syllabus explícito", "Banco institucional de casos", "Talleres de apropiación", "Evaluación reflexiva"])
        
        p5_1 = st.slider("¿Qué tan pertinente es el enfoque formativo de las 'Acciones Restaurativas' frente a las prácticas inadecuadas?", 1, 5, 3)
        comentarios_finales = st.text_area("¿Tiene alguna observación específica, o identificó algún vacío al conversar con el agente?")
        
        enviado = st.form_submit_button("Enviar validación")
        
        if enviado:
            if nombre and correo:
                # Guardar respuesta
                nueva_respuesta = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nombre": nombre, "Correo": correo, "Rol": rol,
                    "Claridad_Datos": p2_1, "Viabilidad_Niveles": p3_1, 
                    "Viabilidad_Declaracion": p3_2, "Mecanismo_Impacto": p4_1,
                    "Pertinencia_Restaurativa": p5_1, "Comentarios": comentarios_finales
                }
                df_nuevo = pd.DataFrame([nueva_respuesta])
                archivo_csv = 'respuestas_validacion.csv'
                
                if not os.path.isfile(archivo_csv):
                    df_nuevo.to_csv(archivo_csv, index=False)
                else:
                    df_nuevo.to_csv(archivo_csv, mode='a', header=False, index=False)
                    
                st.success("¡Gracias! Sus aportes a la Versión 11 han sido registrados.")
            else:
                st.error("Por favor, complete al menos su nombre y correo.")
else:
    st.info("💡 **El formulario de validación institucional aparecerá aquí abajo tras interactuar al menos 2 veces con el agente de consulta.**")
