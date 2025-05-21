import streamlit as st
import joblib
import requests

# Load data
anime = joblib.load("anime.joblib")
similarity = joblib.load("similarity.joblib")

# Set page config
st.set_page_config(page_title="Anime Recommender", page_icon="🇮🇳", layout="wide")

# Meta tag for mobile responsiveness
st.markdown("<meta name='viewport' content='width=device-width, initial-scale=1'>", unsafe_allow_html=True)

# Custom CSS for styling and responsiveness
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }

    h1 {
        text-align: center;
        color: #e63946;
        font-family: 'Comic Sans MS', cursive;
    }

    .stSelectbox label, .stButton button {
        font-size: 18px;
    }

    .anime-card {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 15px;
    }

    .anime-card img {
        max-width: 100%;
        height: auto;
        border-radius: 10px;
    }

    @media screen and (max-width: 768px) {
        .anime-card {
            flex-direction: column;
            text-align: center;
        }

        .anime-card img {
            width: 100%;
            max-width: 300px;
            margin: 0 auto;
        }

        .stSelectbox label, .stButton button {
            font-size: 16px;
        }

        h1 {
            font-size: 26px;
        }
    }

    .footer {
        position: fixed;
        right: 10px;
        bottom: 10px;
        font-size: 16px;
        color: #555;
        font-family: 'Comic Sans MS', cursive;
        background-color: #ffffffcc;
        padding: 6px 12px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        z-index: 100;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🎌 Anime Recommendation System 🎌")

# Function to get anime details from Jikan API
def fetch_anime_info(anime_name):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1"
        response = requests.get(url)
        data = response.json()
        if data["data"]:
            anime_data = data["data"][0]
            title = anime_data["title"]
            synopsis = anime_data["synopsis"]
            image_url = anime_data["images"]["jpg"]["image_url"]
            return {"title": title, "synopsis": synopsis, "image": image_url}
    except:
        pass
    return {"title": anime_name, "synopsis": "Description not available.", "image": ""}

# Recommendation logic
def recommend(anime_name):
    matches = anime[anime['name'].str.lower() == anime_name.lower()]
    if matches.empty:
        return []

    anime_index = matches.index[0]
    anime_pos = anime.index.get_loc(anime_index)
    distances = similarity[anime_pos]
    anime_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommendations = []
    for i in anime_list:
        recommended_pos = i[0]
        recommended_index = anime.index[recommended_pos]
        recommended_name = anime.loc[recommended_index, 'name']
        recommendations.append(recommended_name)
    
    return recommendations

# Anime selection
st.markdown("### 🎥 Choose an anime to get similar recommendations:")
selected_anime = st.selectbox("", anime['name'].str.title().sort_values().unique())

# Recommend button
if st.button("✨ Recommend"):
    st.subheader("🔮 Recommended Anime:")
    recommended_names = recommend(selected_anime)

    if not recommended_names:
        st.error("No recommendations found.")
    else:
        for name in recommended_names:
            info = fetch_anime_info(name)
            with st.container():
                st.markdown(f"<div class='anime-card'>", unsafe_allow_html=True)
                cols = st.columns([1, 2])
                with cols[0]:
                    if info["image"]:
                        st.image(info["image"], use_column_width=True)
                with cols[1]:
                    st.markdown(f"#### {info['title']}")
                    st.write(info["synopsis"])
                st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        🇮🇳 Made by Meet ❤️ Love for Anime
    </div>
""", unsafe_allow_html=True)
