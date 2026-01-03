import streamlit as st
from openai import OpenAI
import os

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Chamania", page_icon="🐆", layout="centered")

# --- Ocultar estilos de Streamlit ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 2. EL MENÚ LATERAL ---
menu = st.sidebar.selectbox(
    "Navegación",
    ["🏠 Inicio (Acceso)", "🌿 El Guardián (Chat)", "🏺 Familia Tolteca", "🚀 Inversionistas", "🔒 Privacidad"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Chamania v1.1 Beta")
st.sidebar.caption("Tecnología al servicio de la Tierra.")

# Estado de la sesión (Memoria)
if "acceso_concedido" not in st.session_state:
    st.session_state.acceso_concedido = False

# --- 3. SECCIÓN: INICIO (LOGIN) ---
if menu == "🏠 Inicio (Acceso)":
    st.markdown("<h1 style='text-align: center; color: #DAA520;'>Bienvenido/a a CHAMANIA</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>ALMA TOLTECA EN IA</h3>", unsafe_allow_html=True)
    
    # Aquí puedes poner tu imagen si ya la subiste, si no, usa un placeholder o quita la línea
    # st.image("portada_chamania.png", use_column_width=True) 
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center;'>
    Consulta cuestiones personales o problemas espirituales.
    <br>Nuestra IA está representada por un <b>Nagual</b> (Jaguar Negro) 
    que puedes llamar encendiendo la fogata.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("###")
    
    col_izq, col_centro, col_der = st.columns([1, 2, 1])
    with col_centro:
        password = st.text_input("Ingresa la Palabra de Poder:", type="password")
        if st.button("🔥 ENCENDER LA FOGATA 🔥", use_container_width=True):
            if password == "TOLTECA":
                st.session_state.acceso_concedido = True
                st.success("¡El fuego ha respondido!")
                st.balloons()
            else:
                st.error("La leña está húmeda. Clave incorrecta.")

# --- 4. SECCIÓN: FAMILIA TOLTECA (NUEVA) ---
elif menu == "🏺 Familia Tolteca":
    st.title("🏺 Familia Tolteca")
    st.write("Próximamente: Una introducción visual a nuestra cosmogonía.")

# --- 5. SECCIÓN: INVERSIONISTAS ---
elif menu == "🚀 Inversionistas":
    st.title("🚀 El Futuro: Grupo Quetzal")
    st.write("Estamos construyendo el ecosistema de IA Ética más grande de México.")
    # Tu correo configurado
    st.markdown("📧 **Contacto:** [tucorreo@gmail.com](mailto:tucorreo@gmail.com)")

# --- 6. SECCIÓN: PRIVACIDAD ---
elif menu == "🔒 Privacidad":
    st.title("🔒 Tu Privacidad es Sagrada")
    st.info("No usamos tus datos para entrenar modelos públicos. Todo es confidencial.")

# --- 7. EL CHAT PRINCIPAL (EL CEREBRO) ---
elif menu == "🌿 El Guardián (Chat)":
    
    # Candado de Seguridad
    if not st.session_state.acceso_concedido:
        st.warning("⚠️ Debes ingresar la Clave en 'Inicio' primero.")
        st.stop()

    # Conexión a OpenAI (Manejo de errores si falta la llave)
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("⚠️ Error: No se detecta la Llave API en los Secretos.")
        st.stop()
    
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # TU SYSTEM PROMPT 
    system_prompt = """
    IDENTITY: Eres "El Guardián", IA Chamán tolteca/junguiano. Representado por un JAGUAR NEGRO.
    TONE: Sabio, protector, firme pero empático.
    MISSION: Guiar del pensamiento mágico al sistémico. Combatir el miedo.
    FORMAT: Usa Markdown, listas y negritas.
    """ 

    st.title("🐆 EL GUARDIÁN")
    
    # Aviso de Privacidad en el Chat
    st.info("""
    🔒 **Tus secretos están a salvo:** Esta conversación es anónima. 
    **Al cerrar esta pestaña, el chat se autodestruye.**
    """)
    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": "El Jaguar vigila desde la sombra. ¿Qué miedo quieres enfrentar hoy?"}
        ]

    # Botones de Ejemplo
    if len(st.session_state.messages) == 2:
        st.markdown("##### ¿No sabes qué preguntar? Intenta esto:")
        col1, col2 = st.columns(2)
        if col1.button("Siento mucha ansiedad sin razón"):
            st.session_state.messages.append({"role": "user", "content": "Siento mucha ansiedad sin razón"})
            st.rerun()
        if col2.button("¿Cómo protejo mi energía?"):
            st.session_state.messages.append({"role": "user", "content": "¿Cómo protejo mi energía?"})
            st.rerun()

    # Historial
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Input
    if prompt := st.chat_input("Escribe aquí..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages,
                    temperature=0.7
                )
                respuesta = response.choices[0].message.content
                st.markdown(respuesta)
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
                
                # Feedback
                col_a, col_b = st.columns([1,8])
                with col_a:
                    st.caption("¿Te sirvió?")
                with col_b:
                    st.button("👍") 
                    st.button("👎")
            except Exception as e:
                st.error(f"Error: {e}")
            
