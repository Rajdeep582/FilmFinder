# 🎬 Movie Recommendation System

![Python](https://img.shields.io/badge/Python-3.13%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)


## 📌 Overview

The **Movie Recommendation System** is a Python-based project that recommends **similar movies** based on the one you select.  
It uses **machine learning techniques** to calculate similarity between movies and suggests related titles instantly.  

Whether you’re looking for a blockbuster, rom-com, thriller, or action-packed adventure, this app will **find the best similar movies** for you. 🍿

---

## 🚀 Features

✅ **Movie Search** → Type a movie name & get recommendations instantly  
✅ **Similarity-based Recommendations** → Uses cosine similarity on movie features  
✅ **Interactive UI** → Built with [Streamlit](https://streamlit.io/) for a smooth experience  
✅ **Fast & Lightweight** → Optimized for quick responses  
✅ **Extensible** → You can integrate more datasets and models easily

---

## 🛠️ Tech Stack

| Technology       | Usage                        |
|-----------------|-----------------------------|
| **Python**      | Core programming language   |
| **Pandas**      | Data manipulation          |
| **NumPy**       | Numerical computations      |
| **Scikit-learn**| Cosine similarity          |
| **Pickle**      | Model serialization        |
| **Streamlit**   | Web interface              |
| **TMDB Dataset**| Movie details & metadata   |

---

## 📂 Project Structure

```bash
Movie-Recommender-System/
│── app.py                # Main Streamlit app
│── model/                # Pre-trained similarity model & movie data
│── requirements.txt      # Required dependencies
│── setup.sh              # Deployment setup (Heroku, optional)
│── Procfile              # For hosting on Heroku
│── README.md             # Project documentation
