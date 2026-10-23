import os
import json
import streamlit as st

# Configuración de página con estética moderna y temática veterinaria
st.set_page_config(
    page_title="Triaje Veterinario IA",
    page_icon="🐾",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para una presentación premium (Soporte Light / Dark Mode)
st.markdown("""
<style>
    /* Tipografía y contenedor principal */
    .main-title {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #059669, #10B981, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #64748B;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    @media (prefers-color-scheme: dark) {
        .sub-title { color: #94A3B8; }
    }
    
    /* Breadcrumb / Historial de síntomas */
    .breadcrumb-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    @media (prefers-color-scheme: dark) {
        .breadcrumb-box {
            background-color: #0F172A;
            border-color: #334155;
            color: #E2E8F0;
        }
    }
    .breadcrumb-item {
        color: #059669;
        font-weight: 600;
    }
    @media (prefers-color-scheme: dark) {
        .breadcrumb-item { color: #34D399; }
    }
    .breadcrumb-sep {
        color: #94A3B8;
        font-weight: 400;
        margin: 0 5px;
    }
    
    /* Tarjeta de pregunta actual (Clínica) */
    .question-card {
        background: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        padding: 1.8rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    .question-card h3 {
        color: #1E293B;
    }
    .question-desc {
        color: #64748B;
    }
    @media (prefers-color-scheme: dark) {
        .question-card {
            background: #1E293B;
            border-color: #334155;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        }
        .question-card h3 {
            color: #F8FAFC !important;
        }
        .question-desc {
            color: #94A3B8 !important;
        }
    }
    
    /* Badge de nivel / Severidad */
    .level-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background-color: #ECFDF5;
        color: #047857;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        border: 1px solid #A7F3D0;
    }
    @media (prefers-color-scheme: dark) {
        .level-badge {
            background-color: #064E3B;
            color: #6EE7B7;
            border-color: #065F46;
        }
    }
    
    /* Tarjeta final (Emergencia/Recomendación) */
    .final-card {
        border-left: 6px solid #EF4444 !important;
    }
    .final-badge {
        background-color: #FEF2F2 !important;
        color: #B91C1C !important;
        border-color: #FECACA !important;
    }
    @media (prefers-color-scheme: dark) {
        .final-badge {
            background-color: #7F1D1D !important;
            color: #FCA5A5 !important;
            border-color: #991B1B !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Funciones para manejo de datos del árbol
# -------------------------------------------------------------
# Cambiamos el archivo al contexto veterinario
JSON_FILE = "TriageMascotas.json" 

def cargar_arbol(ruta_archivo=JSON_FILE):
    """Carga el árbol desde el archivo JSON de forma segura."""
    if not os.path.exists(ruta_archivo):
        return None, f"No se encontró el archivo '{ruta_archivo}'."
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            if not isinstance(datos, dict) or "valor" not in datos:
                return None, "El formato del JSON debe contener al menos un nodo raíz con la clave 'valor'."
            return datos, None
    except json.JSONDecodeError as e:
        return None, f"Error al decodificar JSON: {e}"
    except Exception as e:
        return None, f"Error al leer archivo: {e}"

# -------------------------------------------------------------
# Inicialización del estado de la sesión
# -------------------------------------------------------------
if "arbol" not in st.session_state or st.session_state.arbol is None:
    arbol, error = cargar_arbol()
    st.session_state.arbol = arbol
    st.session_state.error_arbol = error
    st.session_state.historial = [arbol] if arbol else []
    st.session_state.explicacion_ia = None

def reiniciar_navegacion():
    """Reinicia la navegación al nodo raíz."""
    if st.session_state.arbol:
        st.session_state.historial = [st.session_state.arbol]
    else:
        st.session_state.historial = []
    st.session_state.explicacion_ia = None

def recargar_archivo():
    """Recarga el archivo JSON desde el disco."""
    arbol, error = cargar_arbol()
    st.session_state.arbol = arbol
    st.session_state.error_arbol = error
    reiniciar_navegacion()

# -------------------------------------------------------------
# Barra lateral (Configuración y utilidades)
# -------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913465.png", width=80) # Icono veterinario
    st.markdown("### ⚙️ Configuración del Asistente")
    
    # Selector de modelo Ollama
    modelo_ollama = st.text_input(
        "Modelo de Ollama:",
        value="triaje-veterinario",
        help="Nombre del modelo descargado localmente."
    )
    
    # Temperatura más baja por ser contexto médico
    temperatura = st.slider(
        "Creatividad de IA (Temperatura):",
        min_value=0.0,
        max_value=1.0,
        value=0.3, 
        step=0.1,
        help="Se recomienda 0.2 o 0.3 para respuestas médicas precisas."
    )
    
    st.markdown("---")
    st.markdown("### 📂 Gestión del Triaje")
    if st.button("🔄 Recargar Base de Datos", use_container_width=True):
        recargar_archivo()
        st.toast("Protocolos actualizados correctamente", icon="✅")
        st.rerun()

    if st.button("⏪ Nuevo Paciente (Reiniciar)", use_container_width=True):
        reiniciar_navegacion()
        st.rerun()

# -------------------------------------------------------------
# Cabecera principal
# -------------------------------------------------------------
st.markdown('<div class="main-title">🏥 Triaje Veterinario Inteligente</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Asistente de emergencias y primeros auxilios asistido por IA local</div>', unsafe_allow_html=True)

# Manejo de error si no existe el archivo JSON
if st.session_state.error_arbol:
    st.error(st.session_state.error_arbol)
    st.info(f"Asegúrate de haber guardado el árbol binario de mascotas con el nombre: **{JSON_FILE}** en la misma carpeta que este script.")
    st.stop()

# Nodo actual y camino recorrido
historial = st.session_state.historial
if not historial:
    st.session_state.historial = [st.session_state.arbol]
    historial = st.session_state.historial

nodo_actual = historial[-1]
camino_titulos = [nodo["valor"].split(" (")[0] for nodo in historial] # Limpiamos los títulos largos
nivel_actual = len(historial)
hijos = nodo_actual.get("hijos", [])

# -------------------------------------------------------------
# Miga de pan / Historial Clínico
# -------------------------------------------------------------
breadcrumb_html = '<div class="breadcrumb-box"><span>📋 <b>Historial de síntomas:</b></span><br>'
for idx, tit in enumerate(camino_titulos):
    if idx > 0:
        breadcrumb_html += '<span class="breadcrumb-sep">➔</span> '
    breadcrumb_html += f'<span class="breadcrumb-item">{tit}</span> '
breadcrumb_html += '</div>'
st.markdown(breadcrumb_html, unsafe_allow_html=True)

# -------------------------------------------------------------
# Lógica de Paso a Paso: Pregunta y Sub-ramas
# -------------------------------------------------------------
if hijos:
    # AÚN HAY SÍNTOMAS: Mostramos la pregunta dinámica
    st.session_state.explicacion_ia = None 
    
    # Extraemos la pregunta si está embebida en el texto (ej: "... (Siguiente pregunta: ¿X?)")
    texto_nodo = nodo_actual['valor']
    if "(Siguiente pregunta:" in texto_nodo:
        pregunta_texto = texto_nodo.split("(Siguiente pregunta:")[1].replace(")", "").strip()
    elif nivel_actual == 1:
        pregunta_texto = "¿Cuál es la emergencia principal que presenta su mascota?"
    else:
        pregunta_texto = "Por favor, seleccione el síntoma más preciso que observa:"

    st.markdown(f"""
    <div class="question-card">
        <span class="level-badge">🩺 Fase de Evaluación {nivel_actual}</span>
        <h3 style="margin-top:0.3rem; margin-bottom:0.5rem; font-weight:600;">{pregunta_texto}</h3>
        <p class="question-desc" style="font-size:0.9rem; margin-bottom:0;">Seleccione la opción que mejor describa el estado del paciente:</p>
    </div>
    """, unsafe_allow_html=True)

    # Renderizado dinámico de las opciones
    cols = st.columns(min(len(hijos), 2)) # Mejor 2 columnas para textos largos
    for i, hijo in enumerate(hijos):
        col_act = cols[i % len(cols)]
        
        # Limpiar el texto del botón para que no muestre la siguiente pregunta
        texto_completo = hijo.get("valor", f"Opción {i+1}")
        etiqueta_boton = texto_completo.split(" (Siguiente pregunta:")[0]
        
        # Iconos clínicos
        icono = "🔍" if hijo.get("hijos") else "🚑"
        
        if col_act.button(f"{icono} {etiqueta_boton}", key=f"btn_hijo_{nivel_actual}_{i}", use_container_width=True):
            st.session_state.historial.append(hijo)
            st.rerun()

    # Botones de navegación hacia atrás
    st.markdown("<br>", unsafe_allow_html=True)
    col_nav1, col_nav2, _ = st.columns([1, 1, 2])
    with col_nav1:
        if nivel_actual > 1:
            if st.button("⬅️ Corregir síntoma", use_container_width=True):
                st.session_state.historial.pop()
                st.rerun()
    with col_nav2:
        if nivel_actual > 1:
            if st.button("🔄 Nuevo paciente", use_container_width=True):
                reiniciar_navegacion()
                st.rerun()

else:
    # -------------------------------------------------------------
    # NIVEL FINAL (HOJA): Resultado del Triaje y Primeros Auxilios
    # -------------------------------------------------------------
    
    # Extraemos el pre-diagnóstico y los primeros auxilios del texto final
    texto_final = nodo_actual['valor']
    
    st.markdown(f"""
    <div class="question-card final-card">
        <span class="level-badge final-badge">🚨 Evaluación Completada</span>
        <h3 style="margin-top: 0.3rem; margin-bottom: 0.5rem;">Reporte Preliminar</h3>
        <p class="question-desc" style="font-size: 0.9rem; margin-bottom: 0;">
            <b>Información del sistema:</b> {texto_final}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Controles inferiores
    col_back1, col_back2, _ = st.columns([1, 1, 2])
    with col_back1:
        if st.button("⬅️ Atrás (Cambiar síntoma)", use_container_width=True):
            st.session_state.historial.pop()
            st.rerun()
    with col_back2:
        if st.button("🔄 Nuevo Paciente", use_container_width=True):
            reiniciar_navegacion()
            st.rerun()

    st.markdown("---")
    st.subheader(f"🤖 Recomendación de Primeros Auxilios ({modelo_ollama})")

    # Prompt adaptado al contexto VETERINARIO
    prompt = (
        f"El dueño de la mascota reportó este historial de síntomas: {' -> '.join(camino_titulos[:-1])}. "
        f"El sistema arrojó la siguiente conclusión: {texto_final}. "
        "Basado estrictamente en esa conclusión, redacta un reporte de primeros auxilios. "
        "Estructura tu respuesta así: 1) Gravedad de la situación, 2) Acciones INMEDIATAS paso a paso que el dueño debe hacer ahora mismo, "
        "y 3) Una advertencia clara indicando que debe ir al veterinario. Sé empático, profesional y directo. No inventes medicamentos."
    )

# ---------------------------------------------------------
    # --- REEMPLAZA DESDE AQUÍ ---
    # ---------------------------------------------------------
    # Prompt adaptado al contexto VETERINARIO
    instruccion_clinicas = """

    RECUERDA: Al final de tu respuesta, DEBES pegar exactamente esta lista de clínicas de Popayán recomendadas:
    ### 🏥 Clínicas Recomendadas en Popayán:
    * Clínica Veterinaria Doctora Balcázar (24 Horas) | Calle 64 BN #9-20 | 📞 300 637 7077
    * C.V. Pelos & Patas (Urgencias 24h) | Carrera 10 # 1N - 58 | 📞 311 372 5268
    * La Veterinaria (Urgencias 24h) | Transversal 9 #62N - 83 | 📞 301 228 4396
    * Clínica Veterinaria Unicauca (Diurno) | Vereda Las Guacas
    * Animed Clínica Veterinaria (Diurno) | Carrera 9 # 17N-50
    """

    prompt = (
        f"El dueño de la mascota reportó este historial de síntomas: {' -> '.join(camino_titulos[:-1])}. "
        f"El sistema arrojó la siguiente conclusión: {texto_final}. "
        "Basado estrictamente en esa conclusión, redacta un reporte de primeros auxilios. "
        "Estructura tu respuesta así: 1) Gravedad de la situación, 2) Acciones INMEDIATAS paso a paso que el dueño debe hacer ahora mismo, "
        "y 3) Una advertencia clara indicando que debe ir al veterinario. Sé empático, profesional y directo. No inventes medicamentos."
        + instruccion_clinicas # <--- Inyectamos las clínicas a la fuerza aquí
    )

    # Generación con Ollama (Streaming)
    try:
        import ollama

        if st.session_state.explicacion_ia is None:
            with st.spinner(f"Analizando caso con {modelo_ollama}..."):
                stream = ollama.chat(
                    model=modelo_ollama,
                    messages=[
                        # ELIMINAMOS el rol system para que no bloquee tu Modelfile
                        {"role": "user", "content": prompt}
                    ],
                    options={"temperature": temperatura, "top_p": 0.9},
                    stream=True
                )
                
                def generar_stream():
                    for chunk in stream:
                        yield chunk['message']['content']

                respuesta_completa = st.write_stream(generar_stream)
                st.session_state.explicacion_ia = respuesta_completa
        else:
            st.markdown(st.session_state.explicacion_ia)
            if st.button("🔄 Regenerar informe"):
                st.session_state.explicacion_ia = None
                st.rerun()
    # ---------------------------------------------------------
    # --- HASTA AQUÍ ---
    # ---------------------------------------------------------

    except Exception as e:
        error_msg = str(e)
        st.error("⚠️ No se pudo comunicar con el servidor local de Ollama.")
        
        col_err1, col_err2 = st.columns([1, 1])
        with col_err1:
            if st.button("🔄 Reintentar conexión", use_container_width=True):
                st.session_state.explicacion_ia = None
                st.rerun()
        with col_err2:
            if st.button("💡 Ver protocolo offline", use_container_width=True):
                st.session_state.explicacion_ia = (
                    f"### 🚑 Protocolo de Emergencia (Offline)\n\n"
                    f"**Alerta del sistema:** `{texto_final}`\n\n"
                    f"⚠️ **Atención:** Usted está viendo el protocolo base porque la IA está desconectada. "
                    f"Siga las instrucciones mencionadas arriba en la sección de Primeros Auxilios y comuníquese inmediatamente con su clínica veterinaria de confianza."
                )
                st.rerun()

        with st.expander("🛠️ ¿Cómo solucionar el error de Ollama?"):
            st.markdown(f"""
            1. **Inicie el servidor de Ollama**:
               Abra una terminal y ejecute:
               ```bash
               ollama serve
               ```
            2. **Verifique que tiene el modelo descargado (`{modelo_ollama}`)**:
               ```bash
               ollama run {modelo_ollama}
               ```
            """)