import pickle
import streamlit as st
# import requests
import difflib


def recommend(movie_name):
    list_of_all_titles = movies['title'].tolist()
    find_close_match = difflib.get_close_matches(
        movie_name, list_of_all_titles)
    close_match = find_close_match[0]
    index_of_the_movie = movies[movies['title'] == close_match].index[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(
        similarity_score, key=lambda x: x[1], reverse=True)
    # print(sorted_similar_movies)
    recommended_movie_names = []
    i = 1
    for movie in sorted_similar_movies:
        # fetch the movie poster
        index = movie[0]
        title_from_index = movies[movies.index==index]['title'].values[0]
        if (i < 11):
            recommended_movie_names.append(title_from_index)
            i += 1
        print(recommended_movie_names)
    return recommended_movie_names

# working
# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(
#         list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     # recommended_movie_posters = []
#     for i in distances[1:11]:
#         # fetch the movie poster
#         movie_id = movies.iloc[i[0]].id
#         # recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movie_names.append(movies.iloc[i[0]].title)
    # return recommended_movie_names

# def fetch_poster(movie_id):
#     poster_path = updated_movies[updated_movies['id'] == movie_id]['poster_path'].values[0]
#     full_path =  poster_path
#     return full_path


st.header("Movie recommendation System ")
movies = pickle.load(open('artifacts/new_df.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity_new.pkl', 'rb'))
# updated_movies = pickle.load(open('artifacts/updated_movies.pkl', 'rb'))

movies_list = movies['title'].values
selected_movie = st.selectbox('Type or select a movie', movies_list)

if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)
    for movie_name in recommended_movie_names:
        st.text(movie_name)
