import streamlit as st 


# ---- PAGE SETUP----
about_page = st.Page(
    page="views/aboutme.py",
    title="About Us",
    icon=":material/home:",
    default=True,
)
Project_1_page = st.Page(
    page="views/chatbot.py",
    title="Legal ChatBot",
    icon=":material/smart_toy:",
    
)
Project_2_page= st.Page(
    page="views/legaldocs.py",
    title="Legal Document Assisstant",
    icon=":material/forum:",
    
)


#--- NAVIGATION SETUP ---
pg = st.navigation(
    {
        "Info": [about_page],
        "AI Assistance": [Project_1_page,Project_2_page],
    }
)

#-- SHARED ON ALL PAGES----
st.logo("assets/logo.jpeg",size="large")
st.sidebar.text("Made By Khushi Pal🦭")













#---- RUN NAVIGATION --- 
pg.run()
