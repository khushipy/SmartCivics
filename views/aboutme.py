import streamlit as st 
st.title("Smart Civics",anchor=False)
from forms.contact import contact_form

@st.dialog("Register")
def show_contact_form():
    contact_form()



#-- HERO SECTION---
col1,col2 = st.columns(2,gap="small",vertical_alignment="center")
with col1:
    st.image("./assets/homelogo2.jpg",width=230)
    if st.button("Read Preamble"):
        st.write("""We, the people of India, having 
                 solemnly resolved to constitute India into a 
                 SOVEREIGN SOCIALIST SECULAR
                 DEMOCRATIC REPUBLIC and to secure 
                 to all its citizens:
                      JUSTICE, social, economic and 
                      political;
                      LIBERTY of thought, expression, belief, 
                      faith and worship;
                      EQUALITY of status and of opportunity;
                      FRATERNITY assuring the dignity of 
                      the individual and the unity and 
                      integrity of the Nation;
                 IN OUR CONSTITUENT ASSEMBLY
                this twenty-sixth day of November, 1949, do 
                HEREBY ADOPT, ENACT AND GIVE TO
                OURSELVES THIS CONSTITUTION.""")
with col2:
    st.markdown("<h2 style='font-size: 30px;'>सत्यमेव जयते</h2>", unsafe_allow_html=True)
    
    st.write(
        """Welcome to SmartCivics, AI-powered guide to law and the constitution.Your trusted source for insights on law, constitution, and legal affairs. Stay informed with expert analysis, updates, and resources.
"""
    )
    if st.button("✉️ Register Here"):
        show_contact_form()

