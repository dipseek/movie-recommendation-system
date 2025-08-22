import streamlit as st
import pickle
import pandas as pd
import requests
import os



# Google Drive file ID
FILE_ID = "1sDtlacVGAtRXyOUuEDbJl_7xyZy_RJrT"
URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
OUTPUT = "similarity.pkl"

# Download only if not exists
if not os.path.exists(OUTPUT):
    r = requests.get(URL)
    if r.status_code == 200:
        with open(OUTPUT, "wb") as f:
            f.write(r.content)
    else:
        st.error("❌ Failed to download similarity.pkl from Google Drive. Check file permissions.")
        st.stop()

# Load files safely
movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)



def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f93c743b09ac2af7b1828d4bebbecd3e&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    m_list = sorted(list(enumerate(distances)), reverse =True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in m_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# movies = pickle.load(open('movies.pkl','rb'))
# movies_list = movies['title'].values

# similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
'Select a Movie: ',
movies_list
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    
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

    




