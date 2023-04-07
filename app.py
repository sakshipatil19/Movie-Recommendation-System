import pickle
import streamlit as st
import difflib
from imdb import IMDb
import requests

st.set_page_config(
    page_title="Movie Recomendation System",
    page_icon="🎞️",
    initial_sidebar_state="expanded",
    menu_items=None
)


def page1():
    url = 'https://api.themoviedb.org/3/movie/latest'
    params = {'api_key': '8e95934e4df34e2fb4934f3b34b18f58', 'language': 'en-US'}
    page_bg_img = """
      <style>
        [data-testid="stAppViewContainer"]{
        background-image: url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80");
        background-size: cover;
      }
      </style>
      """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown("<h1 style='color:white'>MOVIE RECOMMENDATION SYSTEM</h1>",
                unsafe_allow_html=True)

    response = requests.get(url, params=params)
    data = response.json()
    import imdb

    ia = imdb.IMDb()

    movies = ia.get_top250_movies()[:10]
    st.write("<h2 style='color:white'>#Top rated</h2>", unsafe_allow_html=True)

    for movie in movies:
        st.write(
            f'<h6 style="color: white;">{movie["title"]} ({movie["year"]})</h6>', unsafe_allow_html=True)

    st.write("<h2 style='color:white'>#Trending Now</h2>",
             unsafe_allow_html=True)
    st.write(
        f"<h6 style='color:white'>Title: {data['title']}</h6>", unsafe_allow_html=True)
    st.write(
        f"<h6 style='color:white'>Release Date: {data['release_date']}</h6>", unsafe_allow_html=True)
    st.write(
        f"<h6 style='color:white'>Original Language: {data['original_language']}</h6>", unsafe_allow_html=True)
    st.write(
        f"<h6 style='color:white'>Overview: {data['overview']}</h6>", unsafe_allow_html=True)

    imdb_id = response.json()['imdb_id']
    if imdb_id is not None:

        imdb_url = f'https://www.imdb.com/title/{imdb_id}'

        st.markdown(f'<a href="{imdb_url}">IMDB </a>', unsafe_allow_html=True)
    poster_path = data['poster_path']
    # if poster_path is not None:
    #     poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    #     st.write(
    #         f'<div><img src="{poster_url}" width="300" height="500" >{data["title"]}</div>', unsafe_allow_html=True)
    # else:
    #     st.write("Poster not available")
    st.write("")
    if st.button("Get started"):

        st.session_state["page"] = "page2"
    hide_menu_style = """
      <style>
      #MainMenu {visibility:hidden;}
      footer{visibility:hidden;}
      </style>
     """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


ia = IMDb()
movies = pickle.load(open('artifacts/new_df.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity_new.pkl', 'rb'))


def page2():
    page_bg_img = """
      <style>
        [data-testid="stAppViewContainer"]{
        background-image: url("https://t4.ftcdn.net/jpg/02/86/32/13/360_F_286321335_NBvhp1nTWr6z6EQMVVWqHWWZvNmzFfqS.jpg");
        background-size: cover;
      }
      </style>
      """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    def get_imdb_url(movie_name):
        search_results = ia.search_movie(movie_name)
        if search_results:
            movie_id = search_results[0].getID()
            return ia.get_imdbURL(ia.get_movie(movie_id))

    def get_imdb_rating(imdb_id):
        movie = ia.get_movie(imdb_id)
        if 'rating' in movie:
            return movie['rating']
        else:
            return None

    def recommend(movie_name, num_movies):
        list_of_all_titles = movies['title'].tolist()
        find_close_match = difflib.get_close_matches(
            movie_name, list_of_all_titles)
        close_match = find_close_match[0]
        index_of_the_movie = movies[movies['title'] == close_match].index[0]
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(
            similarity_score, key=lambda x: x[1], reverse=True)
        recommended_movie_names = []
        i = 1
        for movie in sorted_similar_movies:
            index = movie[0]
            title_from_index = movies[movies.index == index]['title'].values[0]
            if (title_from_index == movie_name):
                continue
            if (i <= num_movies):
                recommended_movie_names.append(title_from_index)
                i += 1
            else:
                break
        return recommended_movie_names

    st.markdown("<h1 style='color:black'>Movie recommendation System</h1>",
                unsafe_allow_html=True)

    movies_list = movies['title'].values
    selected_movie = st.selectbox('Type or select a movie', movies_list)
    num_movies = st.slider(
        'Select number of movies to recommend', min_value=5, max_value=25)
    sort_order = st.selectbox(
        'Sort order', ('Descending', 'Ascending'), index=0)

    if st.button('Show Recommendation'):
        recommended_movie_names = recommend(
            selected_movie, num_movies)
        if sort_order == 'Ascending':
            recommended_movie_names = sorted(recommended_movie_names, key=lambda x: get_imdb_rating(
                ia.search_movie(x)[0].getID()) or 0)
        else:
            recommended_movie_names = sorted(recommended_movie_names, key=lambda x: get_imdb_rating(
                ia.search_movie(x)[0].getID()) or 0, reverse=True)
        with st.container():
            col1, col2 = st.columns([3, 1])
            col1.write('<h6>Movies suggested</h6>', unsafe_allow_html=True)
            col2.write('<h6>Rating</h6>', unsafe_allow_html=True)
            if (len(recommended_movie_names) > 0 and recommended_movie_names[0] == selected_movie):
                recommended_movie_names = recommended_movie_names[1:]
            for movie_name in recommended_movie_names:
                movie = ia.search_movie(movie_name)[0]
                imdb_url = get_imdb_url(movie_name)
                link = f'<a href="{imdb_url}" target="_blank">{movie_name}</a>'
                col1.write(
                    f'<div><img src="{movie.data["cover url"]}" width="100" height="150" style="float:left;margin-right:10px">{link}</div>', unsafe_allow_html=True)
                with col2:
                    imdb_id = movie.getID()
                    rating = get_imdb_rating(imdb_id)
                    st.write(f"({rating}/10)")
                    st.write(f"")
                    st.write(f"")
                    st.write(f"")
                    st.write(f"")
                    st.write(f"")
                    st.write(f"")
                    st.write(f"")
                    # st.write(movie.summary())
                    st.write("\n")

    if st.button("Home Page"):
        st.session_state["page"] = "page1"
    hide_menu_style = """
      <style>
      #MainMenu {visibility:hidden;}
      footer{visibility:hidden;}
      </style>
     """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state["page"] = "page1"
if st.session_state["page"] == "page1":
    page1()
else:
    page2()
