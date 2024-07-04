import os
import sqlite3
import numpy as np
import faiss
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz

# Initialize the TF-IDF vectorizer globally
tfidf_vectorizer = TfidfVectorizer()

# Function to vectorize learning objectives using a Sentence Transformer model
def vectorize_learning_obj(llm_name, learning_obj):
    model = SentenceTransformer(llm_name)
    vectors = model.encode(learning_obj)
    return vectors

# Function to store vectors in a Faiss index and save the index to a file
def store_in_faiss(records, faiss_index_file):
    # Create directory if it doesn't exist
    faiss_index_dir = os.path.dirname(faiss_index_file)
    if not os.path.exists(faiss_index_dir):
        os.makedirs(faiss_index_dir)

    # Vectorize only the title field for Faiss index
    llm_name = "sentence-transformers/all-MiniLM-L6-v2"
    titles = [record[0] for record in records]  # Extract titles
    vectors = vectorize_learning_obj(llm_name, titles)

    # Save the vectors to Faiss index
    dim = vectors.shape[1]  # Dimension of the vectors
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    # Save the index to a file
    faiss.write_index(index, faiss_index_file)
    st.write(f"Vectors stored in Faiss index and saved to {faiss_index_file}")

# Function to fetch learning objectives from SQLite database
def get_learning_obj_en(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        statement = 'SELECT title, instructor, learning_obj, course_contents, prerequisites, credits, evaluation, time, frequency, duration, course_type FROM zqm_module_en'
        cursor.execute(statement)
        records = cursor.fetchall()
        conn.close()
        return records
    except sqlite3.Error as e:
        st.error(f"SQLite error: {e}")
        return []

# Function to load Faiss index
def load_faiss_index(faiss_index_file):
    index = faiss.read_index(faiss_index_file)
    return index

# Function to vectorize user input
def vectorize_input(llm_name, user_input):
    model = SentenceTransformer(llm_name)
    vector = model.encode([user_input])[0]
    return vector

# Function to correct misspellings using fuzzy matching
def correct_spelling(input_text, valid_values, threshold=80):
    best_match = None
    highest_score = threshold
    for value in valid_values:
        score = fuzz.ratio(input_text, value)
        if score > highest_score:
            best_match = value
            highest_score = score
    return best_match if best_match else input_text

# Function to recommend input values based on TF-IDF similarity
def recommend_input(user_input, valid_values):
    valid_values_set = list(set(valid_values))  # Remove duplicates
    valid_values_set.append(user_input)  # Append user input for vectorization
    tfidf_matrix = tfidf_vectorizer.fit_transform(valid_values_set)
    user_vector = tfidf_matrix[-1]  # Get the vector for user input
    similarities = cosine_similarity(user_vector, tfidf_matrix[:-1])  # Compare with all other values
    recommendations = sorted(zip(valid_values_set[:-1], similarities[0]), key=lambda x: x[1], reverse=True)
    return [rec[0] for rec in recommendations[:5]]

# Function to perform search using Faiss index with optional filtering by various facets
def search_faiss_index(index, vector, records, instructor_name=None, course_type=None, duration=None, time=None, top_k=3):
    _, indices = index.search(np.array([vector]), top_k)
    filtered_indices = []
    for idx in indices[0]:
        record = records[idx]
        if instructor_name and record[1] != instructor_name:
            continue
        if course_type and record[10] != course_type:
            continue
        if duration and record[9] != duration:
            continue
        if time and record[7] != time:
            continue
        filtered_indices.append(idx)
    return filtered_indices[:top_k]

# Main function to run Streamlit app
def main():
    st.title("Learning Objectives Search Engine")

    # Load data and build Faiss index
    db_file = r"E:\Masters In Computer Science\HMI\hmivenv\data\db\courses.sqlite"  # Update with your actual database file path
    faiss_index_file = r"E:\Masters In Computer Science\HMI\hmivenv\data\faiss_index\faiss_index.idx"

    try:
        # Fetch learning objectives from SQLite database
        records = get_learning_obj_en(db_file)
        if not records:
            st.error("No records found in the database.")
            return

        # Check if Faiss index exists, otherwise create it
        if not os.path.exists(faiss_index_file):
            store_in_faiss(records, faiss_index_file)
        else:
            st.write("Using existing Faiss index.")

        # Load Faiss index
        index = load_faiss_index(faiss_index_file)

        # Prepare valid values for recommendations
        instructors = [record[1] for record in records]
        course_types = [record[10] for record in records]
        durations = [record[9] for record in records]
        times = [record[7] for record in records]

        # User input
        user_input = st.text_input("Enter your query:")

        if user_input:
            # Recommend inputs
            recommended_instructors = recommend_input(user_input, instructors)
            recommended_course_types = recommend_input(user_input, course_types)
            recommended_durations = recommend_input(user_input, durations)
            recommended_times = recommend_input(user_input, times)

            st.write(f"Recommended Instructors: {', '.join(recommended_instructors)}")
            st.write(f"Recommended Course Types: {', '.join(recommended_course_types)}")
            st.write(f"Recommended Durations: {', '.join(recommended_durations)}")
            st.write(f"Recommended Times: {', '.join(recommended_times)}")

            # Parse user input to handle faceted search
            if " && " in user_input:
                main_query, facet = map(str.strip, user_input.split(" && "))
                instructor_name, course_type, duration, time = None, None, None, None
                if "Prof. Dr." in facet:  # Assuming "Prof Dr" indicates an instructor's name
                    instructor_name = facet
                elif "One" in facet:
                    duration = facet
                elif "academic " in facet:
                    time = facet
                else:
                    course_type = facet

                # Correct spelling if necessary
                instructor_name = correct_spelling(instructor_name, instructors) if instructor_name else None
                course_type = correct_spelling(course_type, course_types) if course_type else None
                duration = correct_spelling(duration, durations) if duration else None
                time = correct_spelling(time, times) if time else None

                # Vectorize user input
                user_vector = vectorize_input("sentence-transformers/all-MiniLM-L6-v2", main_query)

                # Perform search with faceted filtering
                results = search_faiss_index(index, user_vector, records, instructor_name=instructor_name,
                                             course_type=course_type, duration=duration, time=time, top_k=3)

            else:
                main_query = user_input.strip()

                # Vectorize user input
                user_vector = vectorize_input("sentence-transformers/all-MiniLM-L6-v2", main_query)

                # Perform search without faceted filtering
                results = search_faiss_index(index, user_vector, records)

            if not results:
                st.write("No matching results found.")
            else:
                st.write(f"Number of results found: {len(results)}")
                st.subheader("Matching Learning Objectives:")
                for idx in results[:3]:
                    title, instructor, learning_obj, course_contents, prerequisites, credits, evaluation, time, frequency, duration, course_type = records[idx]
                    st.write(f"**Title**: {title}".replace("\\n", "\n").replace("\\t", "\t"))
                    st.write(f"**Instructor**: {instructor}".replace("\\n", "\n").replace("\\t", "\t"))
                    st.write(f"**Learning Objective**: {learning_obj}".replace("\\n", "\n").replace("\\t", "\t"))
                    st.write(f"**Course Contents**: {course_contents}".replace("\\n", "\n").replace("\\t", "\t"))
                    st.write(f"**Prerequisites**: {prerequisites}".replace("\\n", "\n").replace("\\t", "\t"))
                    st.write(f"**Credits**: {credits}".replace("\\n", "\n").replace("\\t", "\t"))
                    st.write(f"**Evaluation**: {evaluation}".replace("\\n", "\n").replace("\\t", "\t"))
                    st.write(f"**Time**: {time}".replace("\\n", "\n").replace("\\t", "\t"))
                    st.write(f"**Frequency**: {frequency}".replace("\\n", "\n").replace("\\t", "\t"))
                    st.write(f"**Duration**: {duration}".replace("\\n", "\n").replace("\\t", "\t"))
                    st.write(f"**Course Type**: {course_type}".replace("\\n", "\n").replace("\\t", "\t"))
                    st.write("---")

    except sqlite3.Error as e:
        st.error(f"SQLite error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
