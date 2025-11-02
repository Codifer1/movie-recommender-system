import streamlit as st
import pickle
import pandas as pd
import requests

# -----------------------------
# Function to fetch movie poster
# -----------------------------
def fetch_poster(movie_id):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"  # ✅ Replace with your TMDB API key if different
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            # fallback poster if none available
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        print(f"Error fetching poster for {movie_id}: {e}")
        # fallback poster if error occurs
        return "https://via.placeholder.com/500x750?text=Image+Not+Found"


# -----------------------------
# Function to recommend movies
# -----------------------------
def recommend(movie):
    # find the movie index
    index = movies[movies['title'] == movie].index[0]

    # get the list of similarity scores
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:  # top 5 similar movies
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# -----------------------------
# Load the data
# -----------------------------
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# -----------------------------
# Streamlit UI
# -----------------------------
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Display recommended movies in 5 columns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
