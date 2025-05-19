import streamlit as st 
import joblib 

df=joblib.load("anime.joblib")
similarity=joblib.load("similarity.joblib")
if 'page' not in st.session_state:
    st.session_state.page = 'home'
def home():
    st.title("Anime Recommendation")
def recommend(movie):
        # Convert both movie and dataset titles to lowercase and strip whitespace
        anime = anime.lower().strip()
        matches = anime[anime['name'].str.lower().str.strip() == movie]

        if matches.empty:
            st.warning(f"Movie '{movie}' not found in the dataset.")
            return []

        anime_index = anime.index[0]
        distances = similarity[anime_index]
        anime_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

        recommended_movies = []
        
        for i in anime_list:
            
            recommended_movies.append(anime.iloc[i[0]]['name'].title())
            
            
        return recommended_movies


selected_anime = st.selectbox("Select a anime:", df['name'].str.title().values)

   # Center the Recommend button
st.button("recommend")
st.subheader("recommended movies:")

     
     
    