import streamlit as st
import requests

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
        st.write("Courses matched to", title, ":")
        for course in courses:
            st.write(course[:])  # Access the first element of each nested list
    else:
        st.write("No courses related to", title)
