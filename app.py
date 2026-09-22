import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuración inicial de la página
st.set_page_config(page_title="Validación Política IAG V11", layout="centered", page_icon="🧭")

# Título y descripción
st.title("Validación y Apropiación: Política de uso de IAG")
st.subheader("Versión 11-2026 | Facultad de Ciencias de la Educación")
st.write("""
Este espacio abierto busca recoger sus valoraciones sobre la Versión 11 de la política de uso de IAG. 
Su participación es clave para consolidar un marco que fomente la equidad, la transparencia y el reconocimiento del trabajo humano.
""")

# Crear el formulario
with st.form("validacion_v11"):
    
    st.markdown("### 1. Identificación y Contexto")
    nombre = st.text_input("Nombres y apellidos completos")
    correo = st.text_input("Correo institucional")
    rol = st.selectbox("Rol en la Facultad", ["Estudiante de pregrado", "Estudiante de posgrado", "Docente", "Directivo", "Otro"])
    programa = st.text_input("Programa al que pertenece")
    
    st.markdown("---")
    st.markdown("### 2. La Brújula Ética y Clasificación de Datos")
    st.info("La versión 11 incorpora una tabla explícita de clasificación de datos (Públicos, Personales, Sensibles, Confidenciales e Institucionales) y refuerza el reconocimiento del trabajo humano.")
    
    p2_1 = st.slider("¿Qué tan clara y aplicable resulta la nueva tabla de 'Clasificación de datos' para decidir qué información introducir en una IAG?", 1, 5, 3)
    p2_2 = st.text_area("¿Identifica algún vacío práctico en los cuatro puntos de la brújula (Equidad, Rendición de cuentas, Transparencia, Seguridad) frente a su realidad en el aula?")
    
    st.markdown("---")
    st.markdown("### 3. Niveles de Uso y Declaración Obligatoria")
    st.info("Se refinó la escala de 5 niveles (diferenciando el 4 del 5 por su propósito) y se instauró un formato de declaración con cuatro campos fijos: Sistema, Función, Nivel y Aporte propio.")
    
    p3_1 = st.slider("¿Considera que los 5 niveles propuestos permiten clasificar adecuadamente cualquier interacción académica con la IAG?", 1, 5, 3)
    p3_2 = st.slider("Evalúe la viabilidad práctica de exigir el nuevo formato obligatorio de 4 campos en todas las entregas académicas.", 1, 5, 3)
    p3_3 = st.text_area("¿Qué dificultades anticipa por parte de estudiantes o docentes al momento de redactar la 'Intervención del autor' (Aporte propio) en las declaraciones?")
    
    st.markdown("---")
    st.markdown("### 4. Mecanismos de Apropiación Pedagógica")
    st.info("Para que la política viva en el aula, se propone visibilizar los niveles en el syllabus, crear un banco de casos, realizar talleres y cuidar la proporcionalidad de la carga docente.")
    
    p4_1 = st.selectbox("¿Cuál de los siguientes mecanismos considera que tendrá mayor impacto real en la cultura académica?", 
                        ["Declaración del nivel admitido desde el Syllabus", 
                         "Banco institucional de casos (buenas y malas prácticas)", 
                         "Talleres de apropiación socioafectiva e intelectual", 
                         "Evaluación reflexiva en los productos entregados"])
    p4_2 = st.text_area("El numeral 7.6 advierte sobre la carga docente. ¿Qué estrategias sugiere para que la verificación de declaraciones no sobrecargue la evaluación?")
    
    st.markdown("---")
    st.markdown("### 5. Acciones Restaurativas")
    st.info("La política transita de las 'sanciones' hacia 'acciones restaurativas' que se activan principalmente si el estudiante no logra sostener o sustentar su trabajo.")
    
    p5_1 = st.slider("¿Qué tan pertinente considera el cambio de enfoque de 'sanción' a 'acción restaurativa' para fortalecer el aprendizaje?", 1, 5, 3)
    p5_2 = st.text_area("¿Considera que el criterio de 'no sostener su trabajo' en una sustentación es suficiente y manejable para el docente? ¿Qué ajustes propone?")
    
    st.markdown("---")
    comentarios_finales = st.text_area("¿Tiene alguna otra observación o recomendación específica para la versión definitiva de este documento?")
    
    # Botón de envío
    enviado = st.form_submit_button("Enviar validación")

# Lógica de guardado al enviar
if enviado:
    if nombre and correo:
        # Crear un diccionario con los datos
        nueva_respuesta = {
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nombre": nombre,
            "Correo": correo,
            "Rol": rol,
            "Programa": programa,
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
        
        # Guardar en CSV
        df_nuevo = pd.DataFrame([nueva_respuesta])
        archivo_csv = 'respuestas_validacion.csv'
        
        if not os.path.isfile(archivo_csv):
            df_nuevo.to_csv(archivo_csv, index=False)
        else:
            df_nuevo.to_csv(archivo_csv, mode='a', header=False, index=False)
            
        st.success("¡Gracias! Sus aportes a la Versión 11 de la política han sido registrados exitosamente.")
    else:
        st.error("Por favor, complete al menos su nombre y correo institucional.")