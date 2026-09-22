import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai

# Configuración inicial
st.set_page_config(page_title="Agente y Validación - Política IAG V11", layout="centered", page_icon="🧭")

# --- CONFIGURACIÓN DE LA API (Necesitas tu API Key de Google AI Studio) ---
# En Streamlit Cloud, debes guardar tu API Key en la sección de "Secrets" como GOOGLE_API_KEY
# genai.configure(api_key=st.secrets["GOOGLE_API_KEY"]) 
# Por ahora, usamos un mock si no hay API key configurada para que la app no falle.

st.title("🧭 Agente de Consulta: Política IAG (Versión 11)")
st.write("Antes de validar la política, converse con este asistente para resolver dudas sobre los niveles de uso, la brújula ética o las acciones restaurativas.")

# Inicializar historial de chat y contador de interacciones en session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "interacciones" not in st.session_state:
    st.session_state.interacciones = 0

# Mostrar historial de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del chat
if prompt := st.chat_input("Pregunte algo sobre la versión 11 de la política..."):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Aquí iría la llamada real a la API de Gemini pasándole el texto de la política como contexto.
    # Por ahora simulamos una respuesta genérica basada en tu política.
    respuesta_agente = f"Interesante pregunta sobre '{prompt}'. Según la Versión 11, la política prioriza la evaluación formativa y el reconocimiento del trabajo humano. ¿Tiene alguna otra duda sobre los niveles de uso o la declaración obligatoria?"
    
    with st.chat_message("assistant"):
        st.markdown(respuesta_agente)
    st.session_state.messages.append({"role": "assistant", "content": respuesta_agente})
    st.session_state.interacciones += 1

# --- FASE 2: DESBLOQUEO DEL FORMULARIO ---
st.markdown("---")

if st.session_state.interacciones >= 2:
    st.success("¡Gracias por explorar el documento! Ahora que ha interactuado con la política, lo invitamos a dejar su validación final.")
    
    # Aquí pegas exactamente el mismo bloque de formulario (with st.form("validacion_v11"): ...) 
    # que te pasé en el mensaje anterior.
    with st.form("validacion_v11"):
        st.markdown("### Validación Final")
        nombre = st.text_input("Nombres y apellidos completos")
        correo = st.text_input("Correo institucional")
        
        st.markdown("#### Sus valoraciones")
        p2_1 = st.slider("¿Qué tan clara resulta la tabla de 'Clasificación de datos'?", 1, 5, 3)
        comentarios_finales = st.text_area("¿Tiene alguna observación final para la versión definitiva?")
        
        enviado = st.form_submit_button("Enviar validación")
        
        if enviado:
            if nombre and correo:
                st.success("¡Gracias! Sus aportes han sido registrados exitosamente.")
                # Lógica de guardado en CSV (igual que en el código anterior)
            else:
                st.error("Por favor, complete su nombre y correo.")
else:
    st.info("💡 Interactúe al menos 2 veces con el agente mediante el chat de arriba para desbloquear el formulario de validación institucional.")
