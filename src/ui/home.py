import streamlit as st
from src.recommender.engine import recommend
from src.utils.styling import create_recommendations_grid_streamlit


def show_home_page(movies, similarity):
    # ===========================
    # AMAZON PRIME VIDEO STYLE HEADER ✅
    # ===========================
    st.markdown("""
        <style>
            /* Header container */
            .custom-header {
                background-color: #0F171E; 
                padding: 18px;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                margin-bottom: 20px;
            }

            /* Left side (logo + title) */
            .header-left {
                display: flex;
                align-items: center;
                gap: 12px;
            }

            /* Logo circle */
            .logo {
                background-color: #00A8E1; 
                color: white;
                font-size: 22px;
                font-weight: bold;
                width: 46px;
                height: 46px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 3px 6px rgba(0, 0, 0, 0.3);
            }

            /* Title text — made larger */
            .header-title {
                color: white;
                font-size: 28px;  
                font-weight: 900; 
                letter-spacing: 1.2px;
                line-height: 1.2;
            }

            /* Right side tagline */
            .header-tagline {
                color: #B0BEC5;
                font-size: 15px;
                font-weight: 500;
                text-align: right;
                max-width: 420px;
            }
        </style>

        <div class="custom-header">
            <div class="header-left">
                <div class="logo">🎬</div>
                <div class="header-title">Movie Recommender</div>
            </div>
            <div class="header-tagline">Your personal AI-powered movie discovery assistant</div>
        </div>
    """, unsafe_allow_html=True)

    # ===========================
    # MOVIE SEARCH SELECT BOX
    # ===========================
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "🔍 Search or select a movie:",
        movie_list,
        index=None,  # No movie pre-selected
        placeholder="🔍 Search or select a movie:"  # Placeholder text
    )

    # ===========================
    # HANDLE GET RECOMMENDATIONS BUTTON ✅
    # ===========================
    if st.button("🔍 Get Recommendations", use_container_width=True):
        # Prevent empty string search
        if not selected_movie or selected_movie.strip() == "":
            st.warning("Please select a movie to get recommendations 🎬")
        else:
            with st.spinner("Finding perfect matches for you..."):
                raw_recommendations = recommend(selected_movie, movies, similarity)

                # Process recommendations to ensure all needed data is present
                processed_recommendations = []

                for i, movie in enumerate(raw_recommendations):
                    try:
                        # Get movie ID - try different possible keys
                        movie_id = None
                        for key in ['id', 'movie_id', 'tmdb_id', 'movieId']:
                            if key in movie:
                                movie_id = movie[key]
                                break

                        if movie_id is None:
                            movie_id = i  # Use index as fallback

                        # Get movie title - try different possible keys
                        title = None
                        for key in ['title', 'Title', 'original_title', 'movie_title']:
                            if key in movie and movie[key]:
                                title = movie[key]
                                break

                        if title is None:
                            title = f"Unknown Movie {i}"

                        # Get poster URL - try different possible keys
                        poster_url = None
                        for key in ['poster', 'poster_url', 'poster_path', 'Poster']:
                            if key in movie and movie[key]:
                                poster_url = movie[key]
                                break

                        if not poster_url:
                            poster_url = ""

                        processed_recommendations.append({
                            'id': movie_id,
                            'title': title,
                            'poster': poster_url
                        })

                    except Exception as e:
                        st.error(f"Error processing movie {i}: {e}")
                        st.write(f"Movie data: {movie}")

                # Store processed recommendations in session state
                st.session_state.recommended_movies = processed_recommendations

                st.success(f"Top {len(processed_recommendations)} show recommendations")

    # ===========================
    # DISPLAY RECOMMENDATIONS SECTION
    # ===========================
    if "recommended_movies" in st.session_state and len(st.session_state.recommended_movies) > 0:
        st.markdown('''
        <h2 style="text-align:center;">Movies You Might Love</h2>
        ''', unsafe_allow_html=True)

        # Use the Streamlit-based grid function
        try:
            clicked_movie_id = create_recommendations_grid_streamlit(st.session_state.recommended_movies)

            # Handle navigation if a movie was clicked
            if clicked_movie_id:
                st.query_params.page = "details"
                st.query_params.movie_id = str(clicked_movie_id)
                st.rerun()
        except Exception as e:
            st.error(f"Error creating movie grid: {e}")
            st.write("Falling back to simple list:")
            for movie in st.session_state.recommended_movies:
                st.write(f"- {movie['title']} (ID: {movie['id']})")

    # ===========================
    # SIMPLE FOOTER SECTION ✅
    # ===========================
    st.markdown("""
        <hr style="margin-top:30px; margin-bottom:10px;">
        <div style="text-align:center; padding:10px; font-size:14px; color:gray;">
            © 2025 Movie Recommender | Built with ❤️ using Streamlit
        </div>
    """, unsafe_allow_html=True)
