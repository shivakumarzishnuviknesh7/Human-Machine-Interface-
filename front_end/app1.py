import streamlit as st
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to fetch unique instructors (stub implementation)
def fetch_unique_instructors():
    instructors = [
        'Prof Dr Michael Dornieden', 'Kai Hüschelrath', 'Prof. Dr. Carsten Roppel',
        'Prof. Dr. Manfred Herbert', 'Prof Dr Mareike Heinemann',
        'Prof Dr Robert Richert', 'N.N.', 'Prof. Dr. Andreas Kammel',
        'Prof. Dr. N. Richter', 'Prof. Dr.-Ing. G. Weidner',
        'Prof Dr Peter Schuster', 'Prof. Dr. Bachmann', 'Prof Dr Wiebke Störmann',
        'Prof. Dr. S. Roth'
    ]
    return instructors

# Function to fetch courses by instructor from API
def fetch_courses_by_instructor(instructor_name):
    url = "http://localhost:3000/course_by_instructor/"
    payload = {"instructor": instructor_name}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        courses = response.json()
        return courses
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching courses: {e}")
        return []

# Function to fetch courses by title from API
def fetch_courses_by_title(title_name):
    url = "http://localhost:3000/course_general/"
    payload = {"title": title_name}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        courses = response.json()
        return courses
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching courses: {e}")
        return []

# Transform list of lists to list of dictionaries
def transform_course_structure(course_list):
    keys = [
        'file_path', 'title', 'instructor', 'description', 'content', 'teaching_methods',
        'requirements', 'literature', 'application', 'workload', 'credit_points',
        'exam', 'year', 'frequency', 'duration', 'course_type', 'language'
    ]
    return [dict(zip(keys, course)) for course in course_list]

# Ensure instructor results have a consistent structure
def transform_instructor_courses(course_list):
    keys = [
        'file_path', 'title', 'instructor', 'description', 'content', 'teaching_methods',
        'requirements', 'literature', 'application', 'workload', 'credit_points',
        'exam', 'year', 'frequency', 'duration', 'course_type', 'language'
    ]
    transformed_courses = []
    for course in course_list:
        course_dict = dict(zip(keys, course)) if isinstance(course, list) else course
        if 'title' not in course_dict:
            course_dict['title'] = course_dict.get('file_path', 'Unknown Title')
        if 'instructor' not in course_dict:
            course_dict['instructor'] = 'Unknown Instructor'
        for key in ['description', 'content', 'teaching_methods', 'requirements', 'literature', 'application',
                    'workload', 'credit_points', 'exam', 'year', 'frequency', 'duration', 'course_type', 'language']:
            if key not in course_dict:
                course_dict[key] = 'N/A'
        transformed_courses.append(course_dict)
    return transformed_courses

# Function to combine results from title and instructor queries
def combine_results(title_results, instructor_results):
    title_courses = transform_course_structure(title_results)
    instructor_courses = transform_instructor_courses(instructor_results)

    combined = {course['title']: course for course in title_courses}
    for course in instructor_courses:
        if course['title'] not in combined:
            combined[course['title']] = course
    return list(combined.values())

# Main Streamlit application
def main():
    st.title("Courses Search")

    # Input for course title search
    title = st.text_input("Enter course title:")

    # Sidebar for selecting instructor
    unique_instructors = fetch_unique_instructors()
    selected_instructor = st.sidebar.selectbox("Select Instructor", [""] + unique_instructors)

    # Fetch courses by title if title is provided
    title_courses = fetch_courses_by_title(title) if title else []

    # Fetch courses by instructor if selected
    instructor_courses = fetch_courses_by_instructor(selected_instructor) if selected_instructor else []

    # Combine results from title and instructor searches
    courses = combine_results(title_courses, instructor_courses)

    # Display courses found or message if no courses found
    if courses:
        st.write(f"Found {len(courses)} courses related to the search:")

        # Vectorize the user's query if title is provided
        if title:
            try:
                # Initialize TfidfVectorizer
                tfidf_vectorizer = TfidfVectorizer()

                # Vectorize all course titles and query
                course_titles = [course['title'] for course in courses if 'title' in course]
                all_texts = course_titles + [title] if title else course_titles
                tfidf_matrix = tfidf_vectorizer.fit_transform(all_texts)

                # Separate query_vector and course_vectors
                query_vector = tfidf_matrix[-1] if title else None
                course_vectors = tfidf_matrix[:-1] if title else tfidf_matrix

                # Calculate cosine similarities
                cosine_similarities = cosine_similarity(query_vector, course_vectors).flatten() if query_vector is not None else []

                # Sort courses based on similarity
                sorted_indices = cosine_similarities.argsort()[::-1]

                # Display top 5 similar courses
                for i in range(min(5, len(sorted_indices))):
                    index = sorted_indices[i]
                    course = courses[index]
                    similarity = cosine_similarities[index]

                    st.write("---")
                    st.subheader(course['title'])  # Display course title as subheader
                    st.write("Duration:", course.get('duration', "N/A"))
                    st.write("Course Type:", course.get('course_type', "N/A"))

                    # Display a button to show more details
                    if st.button("Show More Details", key=f"{course['title']}_{i}"):
                        st.write("Description:", course.get('description', "N/A"))
                        st.write("Remarks:", course.get('remarks', "N/A"))

            except ValueError as ve:
                st.error(f"ValueError: {ve}")
        else:
            # Display all matched courses if no title search
            for course in courses:
                st.write("---")
                st.subheader(course['title'])  # Display course title as subheader
                st.write("Duration:", course.get('duration', "N/A"))
                st.write("Course Type:", course.get('course_type', "N/A"))

                # Display a button to show more details
                if st.button("Show More Details", key=f"{course['title']}"):
                    st.write("Description:", course.get('description', "N/A"))
                    st.write("Remarks:", course.get('remarks', "N/A"))
    else:
        st.write("No courses found related to the search criteria.")

if __name__ == "__main__":
    main()
