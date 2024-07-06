

---

# Faceted Search Project

This project implements a faceted search application using Python. The application is designed to allow users to search and filter through a dataset with multiple facets.

## Prerequisites

- Python 3.11 or higher
- Git
- PyCharm (optional but recommended for ease of setup)

## Installation

### Step 1: Clone the Repository

Clone the project from the GitHub repository:

```bash
git clone https://github.com/yourusername/faceted-search-project.git
cd faceted-search-project
```

### Step 2: Setup Virtual Environment

Set up a virtual environment using Python 3.11+:

#### Using PyCharm (Recommended):

1. Open PyCharm and select "Open" from the "File" menu. 
2. Navigate to the project directory and click "Open".
3. PyCharm may prompt you to create a virtual environment. If not, you can manually set it up:
   - Go to `File` > `Settings` (or `PyCharm` > `Preferences` on macOS)
   - Navigate to `Project: faceted-search-project` > `Python Interpreter`
   - Click on the gear icon and select `Add...`
   - Choose `Virtualenv Environment` and ensure the base interpreter is set to Python 3.11+
   - Click `OK` to create the virtual environment.

#### Using Command Line:

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Required Packages

Install the required packages mentioned in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Server

Start the server by running `server.py`:

```bash
python server.py
```

### Step 5: Launch the Frontend

In a new terminal, navigate to the `frontend` directory and run the Streamlit app:

```bash
cd frontend
streamlit run app.py
```

## Usage

Once the server and the Streamlit app are running, you can access the faceted search interface through your web browser. Navigate to the URL provided by Streamlit (typically `http://localhost:8501`).

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
