import streamlit as st
import requests

API_URL = "https://p10-bbabd2f5chf6f6ep.westeurope-01.azurewebsites.net/recommend/" 

st.set_page_config(page_title="Recommendation d'article")

st.title("Moteur de Recommandation")

user_id = st.text_input("Entrez l'ID d'un utilisateur", value="123")

@st.cache_resource
def create_session():
    s = requests.Session()
    return s

s = create_session()

if st.button("Obtenir les recommandations"):
    
    with st.spinner('Connexion à l\'API Azure en cours...'):
        try:
            response = s.get(f"{API_URL}{user_id}")
            
            if response.status_code == 200:
                data = response.json()
                
                st.success("Recommandations générées avec succès !")

                st.subheader("Top 5 des articles à lire :")
                for article_id in data.get("articles", []):
                    st.markdown(f"- **Article n° {article_id}**")
                
            else:
                st.error(f"Erreur de l'API (Code {response.status_code})")
                
        except Exception as e:
            st.error(f"Impossible de joindre l'API Azure. L'erreur est : {e}")