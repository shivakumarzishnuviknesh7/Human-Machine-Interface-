import streamlit as st
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def fetch_courses_by_title(title_name):
    url = "http://localhost:3000/course_general/"
    payload = {"title": title_name}

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


st.title("Courses Search")

title = st.text_input("Enter your query:")

if title:
    courses = fetch_courses_by_title(title)
    if courses:
        st.write(f"Found {len(courses)} courses related to '{title}':")

        # Vectorize the user's query
        tfidf_vectorizer = TfidfVectorizer()
        query_vector = tfidf_vectorizer.fit_transform([title])

        # Vectorize course titles
        course_titles = [course[1] for course in courses]
        course_vectors = tfidf_vectorizer.transform(course_titles)

        # Calculate cosine similarity between the query and course titles
        cosine_similarities = cosine_similarity(query_vector, course_vectors).flatten()

        # Sort courses based on similarity
        sorted_indices = cosine_similarities.argsort()[::-1]

        # Display top 5 similar courses
        for i in range(min(5, len(courses))):
            index = sorted_indices[i]
            course = courses[index]
            similarity = cosine_similarities[index]

            st.write("---")
            st.subheader(course[1])  # Display course title as subheader
            st.write("Duration:", course[14])
            st.write("Course Type:", course[15])

            #st.write("Similarity Score:", f"{similarity * 100:.2f}%")

            # Display a button to show more details
            if st.button("Show More Details", course[1]):
                st.write("Description:", course[3])
                st.write("Remarks:", course[16])
    else:
        st.write("No courses related to", title)
