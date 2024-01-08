# URLShortener
This is a simple URL shortener built with Flask and SQLAlchemy.

# Table of Contents
1. [Project Scope](#project-scope)
2. [Getting Started](#getting-started)



## Project Scope
Build a URL shortener application.
The interface should allow a user to input a URL and display the shortened version after the user submits it. 

Implement the URL shortener API with two main functions: 
1. one that shortens the URL into a brief alphanumeric string. 
2. one that expands the string into the original URL. If no such URL exists, it should return an error. 

### Constraints
The project should contain a data storage method. 
The project should utilize dependencies such that it can shared without additional system configuration. 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine.

### Installing

Follow these steps to run this project on your local machine:

1. **Clone the Repository**: First, clone the repository to your local machine:

    ```bash
    git clone <repository-url>
    ```

    Replace `<repository-url>` with the URL of this GitHub repository.

2. **Navigate to the Project Directory**: Change directory to the project directory:

    ```bash
    cd <project-directory>
    ```

    Replace `<project-directory>` with the name of the directory that was created when you cloned the repository.

3. **Create a Virtual Environment**: It's recommended to create a virtual environment for Python projects. To create one, run:

    ```bash
    python -m venv venv
    ```

4. **Activate the Virtual Environment**: Activate the virtual environment with this command:

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

5. **Install the Dependencies**: Install the project dependencies by running:

    ```bash
    pip install -r requirements.txt
    ```

6. **Set the Environment Variables**: If the application requires any environment variables (like `DATABASE_URL`), you need to set them in your terminal or add them to a `.env` file.

7. **Run the Application**: Now, you can run the application:

    ```bash
    flask run
    ```

    The application should now be running at `http://localhost:5000`.

## Built With

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL Toolkit and ORM

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
