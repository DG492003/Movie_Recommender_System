import pickle
import streamlit as st
import requests
import gzip


movies_list = pickle.load(open('movies.pkl','rb'))
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity_list = pickle.load(f)

def get_movie_poster(movie_name):
    prefix_link = "https://www.omdbapi.com/?apikey=ddbc542c&t="
    res = requests.get(prefix_link + movie_name)
    poster_link = res.json()['Poster']
    re = requests.get(poster_link)
    return re.content

def recommend(movie):
    index = movies_list[movies_list['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity_list[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:7]:
        movie_id = movies_list.iloc[i[0]].id
        recommended_movie_names.append(movies_list.iloc[i[0]].title)
        recommended_movie_posters.append(get_movie_poster(movies_list.iloc[i[0]].title))
    return recommended_movie_names,recommended_movie_posters


lst = movies_list['title'].values
st.title("Movie Recommendation System")
Selected_movie_name = st.selectbox(
    'Please Choose any one Movie: ',(lst)
)
if st.button('Recommend Movies related to selected Movies'):

    recommended_movie_names, recommended_movie_posters = recommend(Selected_movie_name)
    for i in range(0, len(recommended_movie_names), 3):
        cols = st.columns(3)
        
        if i < len(recommended_movie_names):
            with cols[0]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i], width=150)  
                
        if i + 1 < len(recommended_movie_names):
            with cols[1]:
                st.text(recommended_movie_names[i + 1])
                st.image(recommended_movie_posters[i + 1], width=150) 
                
        if i + 2 < len(recommended_movie_names):
            with cols[2]:
                st.text(recommended_movie_names[i + 2])
                st.image(recommended_movie_posters[i + 2], width=150)