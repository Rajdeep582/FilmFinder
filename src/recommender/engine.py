from src.utils.tmdb import fetch_poster

def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title
        movie_poster = fetch_poster(movie_id)
        recommended_movies.append({
            'id': movie_id,
            'title': movie_title,
            'poster': movie_poster
        })

    return recommended_movies
