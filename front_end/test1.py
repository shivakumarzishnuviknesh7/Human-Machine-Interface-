import os
import sqlite3
import numpy as np
import faiss
import streamlit as st
from sentence_transformers import SentenceTransformer


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


# Function to perform search using Faiss index with optional filtering by various facets
def search_faiss_index(index, vector, records, instructor_name=None, course_type=None, duration=None, time=None,
                       top_k=3):
    _, indices = index.search(np.array([vector]), top_k)

    filtered_indices = []
    for idx in indices[0]:
        record = records[idx]
        if (instructor_name and record[1] != instructor_name):
            continue
        if (course_type and record[10] != course_type):
            continue
        if (duration and record[9] != duration):
            continue
        if (time and record[7] != time):
            continue
        filtered_indices.append(idx)

    return filtered_indices[:top_k]


# Main function to run Streamlit app
def main():
    st.title("Learning Objectives Search Engine")

    # Load data and build Faiss index
    db_file = "../data/db/courses.sqlite"  # Update with your actual database file path
    faiss_index_file = "../data/faiss_index/faiss_index.idx"

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

        # User input
        user_input = st.text_input("Enter your query:")

        if user_input:
            # Parse user input to handle faceted search
            if " && " in user_input:
                main_query, facet = map(str.strip, user_input.split(" && "))
                if "Prof. Dr." in facet:  # Assuming "Prof Dr" indicates an instructor's name
                    instructor_name = facet
                    course_type = None
                    duration = None
                    time = None
                elif "One" in facet:
                    instructor_name = None
                    course_type = None
                    duration = facet
                    time = None
                elif "academic " in facet:
                    instructor_name = None
                    course_type = None
                    duration = None
                    time = facet
                else:
                    instructor_name = None
                    course_type = facet
                    duration = None
                    time = None

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

            st.write(f"Number of results found: {len(results)}")
            st.subheader("Matching Learning Objectives:")
            for idx in results[:3]:
                title, instructor, learning_obj, course_contents, prerequisites, credits, evaluation, time, frequency, duration, course_type = \
                    records[idx]
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
