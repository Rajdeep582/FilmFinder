import streamlit as st


def apply_custom_css():
    """Apply custom CSS with proper encoding handling"""
    # Only essential inline CSS that can't be moved to external file
    additional_css = """
    <style>
    /* Hide Streamlit default elements - Framework specific */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Streamlit app container override - Framework specific */
    .stApp > div > div {
        max-width: 100%;
        padding: 0;
    }

    /* Streamlit scrollbar override - Framework specific */
    .stApp {
        overflow-y: auto;
        background-color: var(--primary-bg);
    }
    </style>
    """

    st.markdown(additional_css, unsafe_allow_html=True)

    try:
        with open("src/utils/style.css", "r", encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except UnicodeDecodeError:
        try:
            with open("src/utils/style.css", "r", encoding='utf-8-sig') as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except UnicodeDecodeError:
            with open("src/utils/style.css", "r", encoding='cp1252', errors='ignore') as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def create_movie_card_streamlit(movie_id, title, poster_url):
    """Create a movie card using Streamlit components for proper navigation (opens details in new tab)"""
    with st.container():
        st.markdown(
            f"""
            <div class="movie-card-container">
                <div class="movie-poster-wrapper">
                    <img src="{poster_url}" alt="{title}" class="movie-poster-img" loading="lazy">
                </div>
                <div class="movie-title">{title}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        details_url = f"?page=details&movie_id={movie_id}"
        st.markdown(
            f"""
            <a href="{details_url}" target="_blank" class="details-button">
                Show Details
            </a>
            """,
            unsafe_allow_html=True
        )


def create_movie_card(movie_id, title, poster_url):
    """Create a movie card with Netflix-style design"""
    card_id = f"card_{movie_id}"

    return f"""
    <div class="movie-card" id="{card_id}" data-movie-id="{movie_id}">
        <img src="{poster_url}" class="movie-poster" alt="{title}" loading="lazy">
        <div class="movie-overlay">
            <div class="movie-title">{title}</div>
        </div>
    </div>
    """


def create_movie_details_layout(movie_data):
    """Create the Netflix-style movie details page layout"""
    # Extract data with defaults
    title = movie_data.get('title', 'Unknown Title')
    poster_url = movie_data.get('poster_url', '')
    rating = movie_data.get('rating', 'N/A')
    duration = movie_data.get('duration', 'N/A')
    year = movie_data.get('year', 'N/A')
    genres = movie_data.get('genres', [])
    director = movie_data.get('director', 'Unknown')
    cast = movie_data.get('cast', 'Unknown')
    overview = movie_data.get('overview', 'No overview available.')

    # Use poster as banner if no separate banner image
    banner_url = movie_data.get('banner_url', poster_url)

    return f"""
    <div class="movie-banner">
        <img src="{banner_url}" class="movie-banner-image" alt="{title}">
        <div class="movie-banner-gradient"></div>
        <div class="movie-banner-content">
            <h1 class="movie-title-main">{title}</h1>
            <div class="movie-meta-info">
                <span class="match-score">98% Match</span>
                <span class="meta-item">{year}</span>
                <span class="meta-item">{duration} min</span>
                <span class="rating-badge">{rating}/10</span>
            </div>
        </div>
    </div>

    <div class="movie-details-wrapper">
        <div class="movie-details-container">
            <div class="movie-info-main">
                <div class="movie-poster-sidebar">
                    <img src="{poster_url}" alt="{title}" loading="lazy">
                </div>

                <div class="movie-details-content">
                    <div class="action-buttons-group">
                        <button class="btn-primary">
                            <span>▶</span> Play
                        </button>
                        <button class="btn-secondary">
                            <span>+</span> My List
                        </button>
                        <button class="btn-icon" title="Like">👍</button>
                        <button class="btn-icon" title="Love">❤️</button>
                    </div>

                    <div class="genres-list">
                        {create_genre_pills(genres)}
                    </div>

                    <div class="movie-overview">
                        <h2 class="section-title">Overview</h2>
                        <p class="overview-text">{overview}</p>
                    </div>

                    <div class="cast-crew-grid">
                        <div class="info-section">
                            <div class="info-label">Director</div>
                            <div class="info-value">{director}</div>
                        </div>
                        <div class="info-section">
                            <div class="info-label">Cast</div>
                            <div class="info-value">{cast}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """


def create_genre_pills(genres):
    """Create genre pills HTML"""
    if isinstance(genres, str):
        genres = genres.split(', ')
    elif not isinstance(genres, list):
        return ""

    pills_html = ""
    for genre in genres[:5]:  # Limit to 5 genres
        pills_html += f'<span class="genre-pill">{genre.strip()}</span>'

    return pills_html


def create_recommendations_grid_streamlit(movies):
    """Create a responsive grid using Streamlit components"""
    if not movies or len(movies) == 0:
        st.write("No movies to display")
        return None

    # Determine number of columns based on screen (default to 5)
    num_cols = min(5, len(movies))
    cols = st.columns(num_cols, gap="small")
    clicked_movie_id = None

    for idx, movie in enumerate(movies[:num_cols]):
        movie_id = movie.get('id', idx)
        title = movie.get('title', 'Unknown Title')
        poster_url = movie.get('poster', '')

        with cols[idx]:
            create_movie_card_streamlit(movie_id, title, poster_url)

    return clicked_movie_id


def create_recommendations_grid(movies):
    """Create a responsive grid for movie recommendations"""
    grid_html = '<div class="movies-grid">'

    for movie in movies:
        movie_id = movie.get('id', movie.get('movie_id', ''))
        title = movie.get('title', movie.get('Title', 'Unknown Title'))
        poster_url = movie.get('poster_url', movie.get('Poster', ''))

        grid_html += create_movie_card(movie_id, title, poster_url)

    grid_html += '</div>'
    return grid_html


def create_home_header():
    """Create the home page header with Netflix-style branding"""
    return """
    <div class="header-section">
        <h1 class="main-title">
            <span class="highlight">Movie</span> Recommender
        </h1>
        <p class="subtitle">Discover your next favorite movie with AI-powered recommendations</p>
    </div>
    """


def create_search_section():
    """Create a search section header"""
    return """
    <div class="search-container">
        <div class="search-wrapper">
            <h2 style="text-align: center; color: var(--primary-text); margin-bottom: 16px;">
                Search for a movie to get started
            </h2>
        </div>
    </div>
    """


def handle_movie_card_navigation():
    """Handle movie card clicks using JavaScript"""
    st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const cards = document.querySelectorAll('.movie-card');
        cards.forEach(card => {
            card.addEventListener('click', function(e) {
                e.preventDefault();
                const movieId = this.getAttribute('data-movie-id');
                if (movieId) {
                    const url = new URL(window.location);
                    url.searchParams.set('page', 'details');
                    url.searchParams.set('movie_id', movieId);
                    window.location.replace(url.toString());
                }
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)