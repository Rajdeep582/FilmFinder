import streamlit as st
from src.utils.tmdb import fetch_movie_details


def show_movie_details(movie_id):
    if st.button("← Back to Recommendations"):
        st.query_params.clear()
        st.rerun()

    with st.spinner("Loading movie details..."):
        movie_details = fetch_movie_details(movie_id)

    if not movie_details:
        st.error("Unable to load movie details. Please try again.")
        return

    if movie_details["backdrop_path"]:
        st.markdown(f"""
            <div style="width: 100%; margin-bottom: 20px;">
                <img src="{movie_details['backdrop_path']}" 
                     style="width: 100%; height: 300px; object-fit: cover; border-radius: 10px;" 
                     class="movie-backdrop">
            </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        # Option 1: Use HTML with CSS for better control
        st.markdown(f"""
            <div style="width: 100%;">
                <img src="{movie_details['poster_path']}" 
                     style="width: 100%; height: auto; max-height: 600px; object-fit: contain; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);" 
                     alt="Movie Poster">
            </div>
        """, unsafe_allow_html=True)

        # Option 2: Alternative using st.image with use_column_width
        # st.image(movie_details["poster_path"], use_column_width=True)

    with col2:
        st.markdown(f'<h1 class="movie-detail-title">{movie_details["title"]}</h1>', unsafe_allow_html=True)

        rating = movie_details['vote_average']
        if rating is not None:
            st.write(f"⭐ **Rating:** {rating:.1f}/10")
        else:
            st.write("⭐ **Rating:** N/A")

        st.write(f"⏱ **Duration:** {movie_details['runtime']} min")
        st.write(f"📅 **Release Year:** {movie_details['release_date'][:4]}")
        st.write(f"🎭 **Genres:** {', '.join(movie_details['genres'])}")
        st.write(f"🎬 **Director:** {movie_details['director']}")
        st.write(f"👥 **Cast:** {', '.join(movie_details['cast'])}")

    st.markdown("### 📖 Overview")
    st.write(movie_details["overview"])