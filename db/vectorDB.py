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
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    statement = 'SELECT title, instructor, learning_obj FROM zqm_module_en'
    cursor.execute(statement)
    records = cursor.fetchall()
    conn.close()
    return records

# Function to load Faiss index
def load_faiss_index(faiss_index_file):
    index = faiss.read_index(faiss_index_file)
    return index

# Function to vectorize user input
def vectorize_input(llm_name, user_input):
    model = SentenceTransformer(llm_name)
    vector = model.encode([user_input])[0]
    return vector

# Function to perform search using Faiss index with optional filtering by instructor_name
def search_faiss_index(index, vector, records, instructor_name=None, top_k=3):
    _, indices = index.search(np.array([vector]), top_k)
    if instructor_name:
        filtered_indices = []
        for idx in indices[0]:
            if records[idx][1] == instructor_name:  # Check instructor name
                filtered_indices.append(idx)
        return filtered_indices[:top_k]
    else:
        return indices[0][:top_k]

# Main function to run Streamlit app
def main():
    st.title("Learning Objectives Search Engine")

    # Load data and build Faiss index
    db_file = "../data/db/courses.sqlite"  # Update with your actual database file path
    faiss_index_file = "../data/faiss_index/faiss_index.idx"

    try:
        # Fetch learning objectives from SQLite database
        records = get_learning_obj_en(db_file)

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
            if " and " in user_input:
                main_query, instructor_name = user_input.split(" and ")
                main_query = main_query.strip()
                instructor_name = instructor_name.strip()

                # Vectorize user input
                user_vector = vectorize_input("sentence-transformers/all-MiniLM-L6-v2", main_query)

                # Perform search with faceted filtering
                results = search_faiss_index(index, user_vector, records, instructor_name=instructor_name)

                st.write(f"Number of results found: {len(results)}")
                st.subheader("Matching Learning Objectives:")
                for idx in results[:3]:
                    title, instructor, learning_obj = records[idx]
                    st.write(f"Title: {title}")
                    st.write(f"Instructor: {instructor}")
                    st.write(f"Learning Objective: {learning_obj}")
                    st.write("---")

            else:
                main_query = user_input.strip()

                # Vectorize user input
                user_vector = vectorize_input("sentence-transformers/all-MiniLM-L6-v2", main_query)

                # Perform search without faceted filtering
                results = search_faiss_index(index, user_vector, records)

                st.write(f"Number of results found: {len(results)}")
                st.subheader("Matching Learning Objectives:")
                for idx in results[:3]:
                    title, instructor, learning_obj = records[idx]
                    st.write(f"Title: {title}")
                    st.write(f"Instructor: {instructor}")
                    st.write(f"Learning Objective: {learning_obj}")
                    st.write("---")

    except sqlite3.Error as e:
        st.error(f"SQLite error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
