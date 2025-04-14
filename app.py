import pandas as pd
import streamlit as st
import pickle
import requests

import gdown
import os
#import pickle

# Only download if the file doesn't exist locally
if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/uc?id=13EmtG7bUUrNtttQxixiWDVsf7kXbt3G3"
    gdown.download(url, "similarity.pkl", quiet=False)

# Now load as usual
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)



def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5c2dc1c2f58976dcdb9d9e4c5480c652"
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


# Load movie data and similarity matrix
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
#similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]  # top 5 excluding the selected movie

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# Streamlit UI
st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Choose a movie you like:",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
