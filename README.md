# Descartin Dashboard

This project is a dashboard for visualizing weight data using Streamlit and FastAPI. The data is stored in a JSON file and can be accessed and manipulated through the FastAPI endpoints.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/descartin-dashboard.git
    cd descartin-dashboard
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `.streamlit` directory in the `streamlit` folder:
    ```sh
    mkdir -p streamlit/.streamlit
    ```

2. Create a `secrets.toml` file in the `.streamlit` directory with the following content:
    ```toml
    # filepath: /home/bubu/Documents/Descartin/streamlit/.streamlit/secrets.toml
    password = "your_password_here"
    ```

    Replace `"your_password_here"` with your actual password.

## Running the Application

1. Start the FastAPI server:
    ```sh
    uvicorn server:app --reload
    ```

2. In a new terminal, start the Streamlit app:
    ```sh
    streamlit run streamlit/app.py
    ```

## API Endpoints

The following endpoints are available in the FastAPI server:

- `GET /weight/{index}`: Get weight data by index.
- `POST /weight`: Add new weight data.
- `PUT /weight/{index}`: Update weight data by index.
- `DELETE /weight/{index}`: Delete weight data by index.
- `GET /weight`: Get all weight data.

## Usage

1. Open your web browser and go to `http://localhost:8501` to access the Streamlit dashboard.
2. Enter the password to log in.
3. Use the dashboard to visualize weight data by type of residue, by month, and with a linear trend.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.