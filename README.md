# Resume Editor

## Overview

* AI-powered Resume Editor built with Streamlit.
* Allows users to upload and edit resumes.
* Stores chat history using SQLite.
* Uses an LLM to provide resume editing suggestions and assistance.

## Features

* Upload resume files.
* Interactive AI chat for resume improvements.
* Save and retrieve chat history.
* Simple Streamlit-based web interface.
* Local SQLite database for persistent storage.

## Project Structure

* `app.py` – Main Streamlit application.
* `resume_db.py` – Database creation and chat history management.
* `resume.db` – SQLite database (created automatically).
* `.venv/` – Python virtual environment.
* `requirements.txt` – Project dependencies.

## Prerequisites

* Python 3.10 or later.
* Virtual environment (recommended).

## Installation

* Clone the repository.
* Navigate to the project directory.
* Create a virtual environment:

  ```bash
  python -m venv .venv
  ```
* Activate the virtual environment:

  * macOS/Linux:

    ```bash
    source .venv/bin/activate
    ```
  * Windows:

    ```bash
    .venv\Scripts\activate
    ```
* Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

## Running the Application

* Start the Streamlit server:

  ```bash
  streamlit run app.py
  ```
* Open the URL displayed in the terminal (typically `http://localhost:8501`).

## Database

* Chat history is stored in `resume.db`.
* The application automatically creates required tables on startup.
* Ensure `create_tables()` is called before saving any chat messages.

## Dependencies

* Streamlit
* SQLite3
* Python standard libraries
* LLM/API libraries (if configured)

## Notes

* Keep API keys in a `.env` file if required.
* Do not commit sensitive credentials to version control.
* Activate the virtual environment before running the project.
