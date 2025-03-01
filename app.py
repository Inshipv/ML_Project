import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4debbec15010425b70e255d988049fc2"
    response = requests.get(url)

    if response.status_code != 200:
        return "Error: Could not fetch data"

    data = response.json()
    poster_path = data.get('poster_path')

    if not poster_path:
        return "Error: Poster not found"

    return f"http://image.tmdb.org/t/p/w500/{poster_path}"


def recommend(movie_name):
    movies_index = movies[movies['title'] == movie_name].index[0]
    distance = similarity[movies_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies  = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster through API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movies Recommended System')

Selection_movies_name = st.selectbox(
    "Select a movie:",
    movies['title'].values)

if st.button("Recommend"):
    names ,posters = recommend(Selection_movies_name)
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


