import requests

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
BASE_URL = "https://api.themoviedb.org/3"

def fetch_poster(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    return "https://image.tmdb.org/t/p/w500/" + data.get("poster_path", "")

def fetch_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    movie_data = requests.get(url).json()

    credits_url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
    credits_data = requests.get(credits_url).json()

    director = next((p["name"] for p in credits_data.get("crew", []) if p["job"] == "Director"), "N/A")
    cast = [p["name"] for p in credits_data.get("cast", [])[:5]]
    genres = [g["name"] for g in movie_data.get("genres", [])]

    return {
        "title": movie_data.get("title", "N/A"),
        "overview": movie_data.get("overview", "No overview available."),
        "poster_path": "https://image.tmdb.org/t/p/w500/" + movie_data.get("poster_path", ""),
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/" + movie_data.get("backdrop_path", ""),
        "director": director,
        "cast": cast,
        "genres": genres,
        "release_date": movie_data.get("release_date", "N/A"),
        "runtime": movie_data.get("runtime", "N/A"),
        "vote_average": movie_data.get("vote_average", "N/A")
    }
