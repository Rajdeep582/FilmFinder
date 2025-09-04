import pickle
import streamlit as st
import requests
import json


# =========================
# Fetch movie poster from TMDB API
# =========================
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url)
        data = response.json()

        if "poster_path" in data and data["poster_path"]:
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=Error"


# =========================
# Fetch detailed movie information from TMDB API
# =========================
def fetch_movie_details(movie_id):
    try:
        # Get movie details
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url)
        movie_data = response.json()

        # Get movie credits (cast and crew)
        credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=8265bd1679663a7ea12ac168da84d2e8"
        credits_response = requests.get(credits_url)
        credits_data = credits_response.json()

        # Extract director
        director = "N/A"
        if "crew" in credits_data:
            for person in credits_data["crew"]:
                if person["job"] == "Director":
                    director = person["name"]
                    break

        # Extract top cast (first 5)
        cast = []
        if "cast" in credits_data:
            cast = [person["name"] for person in credits_data["cast"][:5]]

        # Extract genres
        genres = []
        if "genres" in movie_data:
            genres = [genre["name"] for genre in movie_data["genres"]]

        # Get backdrop image for better visual
        backdrop_path = ""
        if "backdrop_path" in movie_data and movie_data["backdrop_path"]:
            backdrop_path = "https://image.tmdb.org/t/p/w1280/" + movie_data["backdrop_path"]

        return {
            "title": movie_data.get("title", "N/A"),
            "overview": movie_data.get("overview", "No overview available."),
            "poster_path": "https://image.tmdb.org/t/p/w500/" + movie_data["poster_path"] if movie_data.get(
                "poster_path") else "https://via.placeholder.com/500x750?text=No+Image",
            "backdrop_path": backdrop_path,
            "director": director,
            "cast": cast,
            "genres": genres,
            "release_date": movie_data.get("release_date", "N/A"),
            "runtime": movie_data.get("runtime", "N/A"),
            "vote_average": movie_data.get("vote_average", "N/A")
        }
    except Exception:
        return None


# =========================
# Recommend movies based on similarity
# =========================
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

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


# =========================
# Custom CSS for Dark Theme
# =========================
def apply_custom_css():
    st.markdown("""
    <style>
    /* Dark theme background */
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
    }

    /* Custom title styling */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 1rem;
        letter-spacing: -1px;
    }

    .subtitle {
        text-align: center;
        color: #8a8aa0;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        font-weight: 300;
    }

    /* Movie card styling */
    .movie-card {
        display: block;                    /* make full card clickable */
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 0.8rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
        height: 100%;
        cursor: pointer;
        text-decoration: none !important;  /* prevent link underline */
        color: inherit !important;         /* keep text color */
    }

    .movie-card:hover {
        transform: translateY(-8px);
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(102, 126, 234, 0.4);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
        text-decoration: none;
        color: inherit;
    }

    .movie-poster {
        border-radius: 12px;
        width: 100%;
        height: auto;
        margin-bottom: 0.8rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }

    .movie-title {
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 600;
        text-align: center;
        line-height: 1.3;
        padding: 0 0.3rem;
        min-height: 2.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Search container styling */
    .search-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stSelectbox > div > div:hover {
        border-color: rgba(102, 126, 234, 0.5);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 50px;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }

    /* Results section */
    .results-header {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2.5rem 0 1.5rem 0;
        padding-left: 0.5rem;
        border-left: 4px solid #667eea;
    }

    /* Movie Details Page Styling */
    .movie-details-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        margin: 1rem 0;
    }

    .movie-backdrop {
        width: 100%;
        height: 300px;
        object-fit: cover;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
    }

    .movie-detail-poster {
        border-radius: 16px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
        width: 100%;
        height: auto;
        max-width: 350px;
    }

    .movie-detail-title {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        line-height: 1.2;
    }

    .movie-detail-section {
        margin-bottom: 1.5rem;
    }

    .movie-detail-label {
        color: #667eea;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        display: block;
    }

    .movie-detail-text {
        color: #e0e0e0;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }

    .movie-stats {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }

    .stat-item {
        background: rgba(102, 126, 234, 0.1);
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        text-align: center;
        min-width: 100px;
    }

    .stat-value {
        color: #667eea;
        font-weight: 700;
        font-size: 1.1rem;
    }

    .stat-label {
        color: #a0a0a0;
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }

    .back-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 2rem;
        text-decoration: none;
        display: inline-block;
    }

    .back-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        text-decoration: none;
        color: white;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .movie-detail-title {
            font-size: 2rem;
        }

        .movie-stats {
            justify-content: center;
        }

        .stat-item {
            min-width: 80px;
            padding: 0.6rem 1rem;
        }

        .movie-backdrop {
            height: 200px;
        }
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    </style>
    """, unsafe_allow_html=True)


# =========================
# Movie Card Component (Clickable via link)
# =========================
def create_movie_card(movie_id, title, poster_url):
    # Use a proper <a> link so navigation works reliably in Streamlit
    return f"""
    <a class="movie-card" href="?page=details&movie_id={movie_id}">
        <img src="{poster_url}" class="movie-poster" alt="{title}" loading="lazy">
        <div class="movie-title">{title}</div>
    </a>
    """


# =========================
# Movie Details Page - FIXED HTML RENDERING AND RATING FORMAT
# =========================
def show_movie_details(movie_id):
    # Back button - positioned at top left
    if st.button("← Back to Recommendations"):
        st.query_params.clear()
        st.rerun()

    with st.spinner("Loading movie details..."):
        movie_details = fetch_movie_details(movie_id)

    if movie_details:
        # 1. BACKDROP IMAGE - Full width banner at top
        if movie_details["backdrop_path"]:
            st.markdown(f"""
                <img src="{movie_details['backdrop_path']}" class="movie-backdrop" alt="Backdrop">
            """, unsafe_allow_html=True)

        # Add some spacing after backdrop
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)

        # 2. TWO-COLUMN LAYOUT - Poster (left) + Movie Info (right)
        col1, col2 = st.columns([1, 2], gap="large")

        with col1:
            # LEFT COLUMN: Movie Poster (fixed size, top-aligned)
            st.markdown(f"""
                <div style="display: flex; justify-content: center;">
                    <img src="{movie_details['poster_path']}" class="movie-detail-poster" alt="{movie_details['title']}">
                </div>
            """, unsafe_allow_html=True)

        with col2:
            # RIGHT COLUMN: All movie information

            # Movie Title
            st.markdown(f'<h1 class="movie-detail-title">{movie_details["title"]}</h1>', unsafe_allow_html=True)

            # Stats Row (Rating, Duration, Year) - FIXED RATING FORMAT
            stats_html = '<div class="movie-stats">'
            if movie_details["vote_average"] != "N/A" and movie_details["vote_average"] is not None:
                # Format rating to 1 decimal place
                rating = float(movie_details["vote_average"])
                formatted_rating = f"{rating:.1f}"
                stats_html += f'''
                <div class="stat-item">
                    <div class="stat-value">⭐ {formatted_rating}/10</div>
                    <div class="stat-label">Rating</div>
                </div>
                '''

            if movie_details["runtime"] != "N/A":
                stats_html += f'''
                <div class="stat-item">
                    <div class="stat-value">{movie_details["runtime"]} min</div>
                    <div class="stat-label">Duration</div>
                </div>
                '''

            if movie_details["release_date"] != "N/A":
                year = movie_details["release_date"][:4] if movie_details["release_date"] else "N/A"
                stats_html += f'''
                <div class="stat-item">
                    <div class="stat-value">{year}</div>
                    <div class="stat-label">Year</div>
                </div>
                '''
            stats_html += '</div>'
            st.markdown(stats_html, unsafe_allow_html=True)

            # Genres
            if movie_details["genres"]:
                genres_str = " • ".join(movie_details["genres"])
                st.markdown(f'''
                    <div class="movie-detail-section">
                        <span class="movie-detail-label">🎭 Genres</span>
                        <div class="movie-detail-text">{genres_str}</div>
                    </div>
                ''', unsafe_allow_html=True)

            # Director
            st.markdown(f'''
                <div class="movie-detail-section">
                    <span class="movie-detail-label">🎬 Director</span>
                    <div class="movie-detail-text">{movie_details["director"]}</div>
                </div>
            ''', unsafe_allow_html=True)

            # Cast
            if movie_details["cast"]:
                cast_str = ", ".join(movie_details["cast"])
                st.markdown(f'''
                    <div class="movie-detail-section">
                        <span class="movie-detail-label">👥 Cast</span>
                        <div class="movie-detail-text">{cast_str}</div>
                    </div>
                ''', unsafe_allow_html=True)

        # Add spacing between columns and overview
        st.markdown('<div style="margin: 3rem 0 1rem 0;"></div>', unsafe_allow_html=True)

        # 3. OVERVIEW SECTION - Full width below both columns
        st.markdown(f'''
            <div class="movie-details-container">
                <span class="movie-detail-label">📖 Overview</span>
                <div class="movie-detail-text" style="margin-top: 1rem; font-size: 1.1rem; line-height: 1.8;">{movie_details["overview"]}</div>
            </div>
        ''', unsafe_allow_html=True)

    else:
        st.error("Unable to load movie details. Please try again.")
        if st.button("← Back to Recommendations"):
            st.query_params.clear()
            st.rerun()

# =========================
# Main Application Logic
# =========================
def main():
    # Set page config
    st.set_page_config(
        page_title="Movie Recommender",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Apply custom CSS
    apply_custom_css()

    # Get query parameters (modern API)
    query_params = st.query_params
    page = query_params.get("page", "home")
    movie_id = query_params.get("movie_id", None)

    # Route to appropriate page
    if page == "details" and movie_id:
        st.markdown('<h1 class="main-title">🎬 Movie Details</h1>', unsafe_allow_html=True)
        show_movie_details(int(movie_id))
    else:
        show_home_page()


# =========================
# Home Page (Recommendations)
# =========================
def show_home_page():
    # Header
    st.markdown('<h1 class="main-title">🎬 Movie Recommender</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Discover your next favorite movie with AI-powered recommendations</p>',
                unsafe_allow_html=True)

    # Load movie data and similarity model
    movies = pickle.load(open('model/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))

    # Search container with proper structure
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            # Movie selection dropdown
            movie_list = movies['title'].values
            selected_movie = st.selectbox(
                "🔍 Type or select a movie you like:",
                movie_list,
                index=0,
                help="Start typing to search for a movie"
            )

            # Button for recommendations
            if st.button("✨ Get Recommendations", use_container_width=True):
                with st.spinner("Finding perfect matches for you..."):
                    recommended_movies = recommend(selected_movie)

                # Display recommendations header
                st.markdown('<h2 class="results-header">Movies You Might Love</h2>', unsafe_allow_html=True)
                st.markdown(
                    '<p style="color: #8a8aa0; text-align: center; margin-bottom: 2rem;">Click on any movie card to see detailed information</p>',
                    unsafe_allow_html=True)

                # Display in 5 columns with proper spacing
                cols = st.columns(5, gap="medium")

                for idx, col in enumerate(cols):
                    with col:
                        movie = recommended_movies[idx]
                        st.markdown(
                            create_movie_card(
                                movie['id'],
                                movie['title'],
                                movie['poster']
                            ),
                            unsafe_allow_html=True
                        )

    # Footer info
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;">
            Powered by TMDB API | Built with ❤️ using Streamlit ~ Rajdeep Biswas
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# Run the application
# =========================
if __name__ == "__main__":
    # Load global variables for the recommend function
    movies = pickle.load(open('model/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))
    main()