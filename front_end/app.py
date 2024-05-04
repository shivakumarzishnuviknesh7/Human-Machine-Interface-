import streamlit as st


def main():
    st.title("Search Page")

    # Create a search bar
    search_term = st.text_input("Enter search term:")

    # Create a search button
    search_button = st.button("Search")

    # Handle button click event
    if search_button:
        st.write(f"Searching for: {search_term}")


if __name__ == "__main__":
    main()
