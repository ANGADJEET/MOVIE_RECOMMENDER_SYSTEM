import pickle
import streamlit as st
import requests

# Function to fetch movie poster URL
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)  
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Main app code
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title('Movie Recommender System')

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie", movie_list)

if st.button('Show Recommendations'):
    st.subheader(f"Top 5 Recommendations for '{selected_movie}'")
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Calculate the number of columns to center the content
    num_columns = 5
    centered_col = st.columns([(12 - num_columns) // 2] + [1] * num_columns + [(12 - num_columns) // 2])
    
    for i, (name, poster_url) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
        with centered_col[i + 1], st.expander(f"Rec {i+1}"):
            st.text(name)
            st.image(poster_url, use_column_width=True)
            st.markdown("<style>img{width:100%;}</style>", unsafe_allow_html=True)  # Increase image size
