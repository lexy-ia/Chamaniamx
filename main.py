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
            
