import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch poster
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7e52678929272575f8f067b637d171e4&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Apply Custom Styling
st.markdown(
    """
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

    /* Background Styling */
    .stApp, .appview-container {
        background: url("https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80") no-repeat center center fixed;
        background-size: cover;
        background-blend-mode: overlay;
        background-color: rgba(0, 0, 0, 0.7);
    }

    /* Title Styling */
    h1 {
        color: #afeeee !important;
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        font-family: 'Roboto', sans-serif !important;
        text-shadow: 3px 3px 3px #000000 !important;
    }

    /* Custom Button */
    div.stButton > button {
        background-color: #ff4500 !important; /* Orange */
        border-radius: 12px !important;
        color: white !important;
        padding: 12px 30px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-transform: uppercase;
        font-family: 'Roboto', sans-serif !important;
        transition: all 0.3s ease-in-out !important;
    }

    /* Center Align Button */
    div.stButton {
        display: flex;
        justify-content: center;
    }

    /* Button Hover Effect */
    div.stButton > button:hover {
        background-color: #ff6347 !important; /* Tomato */
        transform: scale(1.1);
        box-shadow: 0px 4px 15px rgba(255, 99, 71, 0.5);
    }

    /* Recommended Movie Name Styling */
    .movie-name {
        color: #afeeee !important; 
        font-size: 18px !important;
        font-weight: bold !important;
        text-align: center !important;
        font-family: 'Roboto', sans-serif !important;
    }

    /* Footer Styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #FFD700;
        text-align: center;
        font-size: 24px;
        font-family: 'Roboto', sans-serif !important;
        padding: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Title with Forced Color
st.markdown("<h1>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

# Movie Selection
selected_movie_name = st.selectbox(
    'Which movie do you want to watch?',
    movies['title'].values
)

# Recommendation Button
if st.button('🔍 Recommend'):
    names, posters = recommend(selected_movie_name)

    # Display Recommended Movies
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"<p class='movie-name'>{names[0]}</p>", unsafe_allow_html=True)
        st.image(posters[0])
    with col2:
        st.markdown(f"<p class='movie-name'>{names[1]}</p>", unsafe_allow_html=True)
        st.image(posters[1])
    with col3:
        st.markdown(f"<p class='movie-name'>{names[2]}</p>", unsafe_allow_html=True)
        st.image(posters[2])
    with col4:
        st.markdown(f"<p class='movie-name'>{names[3]}</p>", unsafe_allow_html=True)
        st.image(posters[3])
    with col5:
        st.markdown(f"<p class='movie-name'>{names[4]}</p>", unsafe_allow_html=True)
        st.image(posters[4])

# Footer
st.markdown(
    """
    <div class="footer">
        <p>Find your next favorite movie effortlessly! 🎬✨</p>
    </div>
    """,
    unsafe_allow_html=True
)