# Residue Management Application

This application is designed to manage and visualize residue data. It consists of a backend API and a frontend client. The backend handles database operations and generates graphs, while the frontend provides a user interface for interacting with the data.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Endpoints](#endpoints)
- [License](#license)

## Features

- Add, update, and delete residue data.
- Generate graphs based on residue data.
- View residue data in a user-friendly interface.
- Automatically clear old images when the frontend is opened.

## Technologies Used

- Python
- Flask
- SQLite
- Pandas
- Matplotlib
- Seaborn
- HTML/CSS
- JavaScript

## Setup and Installation

1. **Clone the repository:**

## Project Structure

- **static/style.css**: Contains the CSS styles for the frontend.
- **templates/index.html**: Contains the HTML template for the frontend.
- **images/**: Directory where generated images are stored.
- **server.py**: Backend server handling API requests and database operations.
- **client.py**: Frontend client serving the HTML and clearing the images folder.
- **math.py**: Script for generating graphs based on residue data.
- **check_residue_types.py**: Script for checking residue types in the database.
- **data.db**: SQLite database file.

## Endpoints

### Backend API

- **GET /residues/**: Retrieve all residues.
- **POST /residues/**: Add a new residue.
- **PUT /residues/<int:residue_id>**: Update a residue.
- **DELETE /residues/<int:residue_id>**: Delete a residue.
- **GET /residue_types/**: Retrieve distinct residue types.
- **GET /residues/graph_data/**: Retrieve graph data for a specific residue type and date range.
- **POST /generate_graph**: Generate a graph for a specific residue type and date range.

### Frontend

- **GET /**: Serve the frontend HTML.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.