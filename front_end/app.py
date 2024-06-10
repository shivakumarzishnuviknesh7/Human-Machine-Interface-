
import streamlit as st
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def fetch_courses_by_instructor(instructor_name):
    url = "http://localhost:3000/course_by_instructor/"
    payload = {"instructor": instructor_name}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        try:
            courses = response.json()
            return courses
        except ValueError:
            st.error("Received non-JSON response from the server.")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching courses: {e}")
        return []

def fetch_courses_by_title(title_name):
    url = "http://localhost:3000/course_general/"
    payload = {"title": title_name}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        try:
            title = response.json()
            return title
        except ValueError:
            st.error("Received non-JSON response from the server.")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching courses: {e}")
        return []



st.title("Courses Search")

title = st.text_input("Enter your query:")

if title:
    courses = fetch_courses_by_title(title)
    if courses:
        for course in courses:

            # Convert all elements in the course list to strings
            course = [str(item) for item in course]

            # Calculate TF-IDF vectors for title and course
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform([title] + course)

            # Calculate cosine similarity
            cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])

            for sim in cosine_sim[0]:
                if sim > 0.1:
                    print("***********************************************")
                    for i, data in enumerate(course):
                        st.markdown(f"**Field {i + 1}:** {data}")
                    break  # Exit the loop after finding a similar course
                else:
                    st.write("No similar course found.")
    else:
        st.write("No courses related to", title)
