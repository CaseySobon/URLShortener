# URL Shortener
This is a simple URL shortener built with Flask and SQLAlchemy.

# Table of Contents
1. [Project Scope](#project-scope)
2. [Getting Started](#getting-started)
3. [Code Explanation](#Code-Explanation)
    - [app.py](#apppy)
    - [index.html](#indexhtml)
    - [homepage_style.css](#homepage_style)
    - [homepage_interactions.js](#homepage_interactionsjs)
4. [Development Process](#development-process)
   - [Backend](#backend)
   - [Frontend](#frontend)


## Project Scope
Build a URL shortener application.
The interface should allow a user to input a URL and display the shortened version after the user submits it. 

Implement the URL shortener API with two main functions: 
1. one that shortens the URL into a brief alphanumeric string. 
2. one that expands the string into the original URL. If no such URL exists, it should return an error. 

### Constraints
The project should contain a data storage method. 
The project should utilize dependencies such that it can shared without additional system configuration. 

### Bonus Features
1. Optional ability to create a personal URL.
2. Recalls previously shortened URLs if the original URL was already shortened.
3. Option to force create a new URL if URL was already shortened.
4. Easy copy button for URLs.

<br>  

![image](https://github.com/CaseySobon/URLShortener/assets/96227583/9208a99b-e309-4314-8e86-cde586f3e802)


<details id="getting-started">
<summary> <h2> Getting Started </h2> </summary>

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
</details>

<details id="Code-Explanation">
<summary><h2>Code Explanation</h2></summary>
This project follows a common pattern in web development where the codebase is divided into separate files based on their responsibilities, often referred to as separation of concerns. This makes the code easier to understand, maintain, and scale.

- `app.py`: This is the main driver of the application. It sets up and configures the Flask application and the SQLAlchemy database. It also defines the Link model for the database and the function to encode a number into base62 for URL shortening. This separation allows for a clear overview of the server-side logic and database management.

- `index.html`: This file serves as the webpage template. It structures the HTML content of the webpage and includes placeholders for dynamic content. Separating the HTML into its own file allows for a clear distinction between the structure of the webpage and its style or behavior.

- `homepage_style.css`: This file contains the styles for the webpage. It defines the look and feel of the webpage, including layout, colors, fonts, and animations. By separating the CSS into its own file, it's easier to make changes to the style without affecting the HTML or JavaScript code.

- `homepage_interactions.js`: This file contains the JavaScript code that manages the interactions on the webpage. It handles user events like clicks or form submissions, updates the dynamic content on the page, and communicates with the server when necessary. Separating the JavaScript into its own file allows for a clear distinction between the structure and style of the webpage and its behavior.

This structure allows each file to focus on a specific aspect of the application, making the code easier to understand and maintain. It also allows for easier collaboration, as different developers can work on different files without causing conflicts.

<details id="app.py">
<summary><h3>app.py</h3></summary>

This is the main driver of the application. It sets up and configures the Flask application and the SQLAlchemy database. It also defines the `Link` model for the database and the function to encode a number into base62 for URL shortening.

#### Importing Necessary Modules

The script begins by importing the necessary modules. These include `os` for interacting with the operating system, `flask` for the web framework, `flask_sqlalchemy` for the ORM to interact with the database, `string` for string operations, and `uuid` for generating unique identifiers.

```python
import os
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import string
import uuid
```
#### Initializing Flask App and SQLAlchemy
The Flask app is initialized and SQLAlchemy is configured with the database URL. If the `DATABASE_URL` environment variable is not set, it defaults to a SQLite database named `test.db` in the current directory.
```python
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
db = SQLAlchemy(app)
```
#### Defining the Link Model
The `Link` model is defined for SQLAlchemy. This model has three fields: `id` (a primary key), `original_url` (the original URL to be shortened), and `short_url` (the shortened URL).

```python
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(80), unique=True, nullable=False)
```

#### Creating Database Tables
All database tables are created within the app context. This ensures that the tables exist before they are used.
```python
with app.app_context():
    db.create_all()
```
#### Defining Characters for Short URLs
The characters to be used in the short URLs are defined. These include all lowercase letters, all uppercase letters, and all digits.
```python
chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
```

#### Encoding Function
A function `base62_encode(num)` is defined to encode a number into base62. This is used to generate the short URLs.
```python
def base62_encode(num):
    arr = []
    base = len(chars)
    while num:
        num, rem = divmod(num, base)
        arr.append(chars[rem])
    arr.reverse()
    return ''.join(arr)
```
#### Defining Routes

Several routes are defined for the Flask app:

- The home page route (`/`) accepts both GET and POST requests. If the request method is POST, it processes the form data to either shorten a new URL or expand a short URL. It then renders the home page with the original URL, short URL, and any errors.
```python
@app.route('/', methods=['GET', 'POST'])
def handle_url():
    # Initialize variables for the original URL, short URL, and any errors
    url = None
    short_url = None
    shorten_error = None  # Error for the "Shorten" section
    expand_error = None  # Error for the "Expand" section
    existing = False  # Flag to indicate if the original URL already exists
    domain = request.host_url.rstrip('/')  # Define domain here to be used in the template
```
1. The code first checks if the request method is `POST` and gets the original URL, custom short URL, short URL to expand, and new short URL option from the form. 
```python
if request.method == 'POST':
    original_url = request.form.get('url')
    custom_short_url = request.form.get('custom_short_url')
    short_url_input = request.form.get('short_url')
    new_short_url = request.form.get('new_short_url')
```
2. If an `original URL` was provided, the code checks if it already exists in the database. If it does and the user doesn't want a new short URL, it returns the existing short URL. Otherwise, it checks if a custom short URL was provided. If it was, it checks if it's already in use. If it is, it sets an error message. If it's not, it creates a new link with the original URL and custom short URL. If no custom short URL was provided, it creates a new link with a placeholder short URL, generates a new short URL using base62 encoding, and updates the link. If there were no errors and the original URL didn't already exist, it sets the short URL.
```python
if original_url:
    existing_link = Link.query.filter_by(original_url=original_url).first()
    if existing_link and not new_short_url:
        short_url = domain + '/' + existing_link.short_url
        existing = True
    else:
        if custom_short_url:
            existing_link = Link.query.filter_by(short_url=custom_short_url).first()
            if existing_link:
                shorten_error = "Custom short URL is already in use, please choose another name"
            else:
                link = Link(original_url=original_url, short_url=custom_short_url)
                db.session.add(link)
                db.session.commit()
        else:
            placeholder = str(uuid.uuid4())
            link = Link(original_url=original_url, short_url=placeholder)
            db.session.add(link)
            db.session.commit()
            short_url = base62_encode(link.id)
            link.short_url = short_url
            db.session.commit()

        if not shorten_error and not existing:
            short_url = domain + '/' + link.short_url
```
3. If a `short URL` was provided to expand, the code removes the domain from the short URL, checks if the short URL exists in the database, and if it does, sets the original URL. If the short URL doesn't exist, it sets an error message.
```python
elif short_url_input:
    short_url_input = short_url_input.split('/')[-1]
    link = Link.query.filter_by(short_url=short_url_input).first()
    if link:
        url = link.original_url
    else:
        expand_error = "URL doesn't exist"
    short_url = domain + '/' + short_url_input
```
4. Finally, it renders the home page with the original URL, short URL, and any errors.
```python
return render_template('index.html', url=url, short_url=short_url, shorten_error=shorten_error, expand_error=expand_error, existing=existing)
```


- The redirect route (`/<short_url>`) redirects from a short URL to the original URL. If the short URL does not exist in the database, it returns a 404 error.

```python
@app.route('/<short_url>')
def redirect_short_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first()
    if link:
        return redirect(link.original_url)
    else:
        return '404: URL not found', 404
```

- The expand route (`/expand/<short_url>`) expands a short URL into the original URL. If the short URL does not exist in the database, it returns an error.

```python
@app.route('/expand/<short_url>')
def expand_short_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first()
    if link:
        return link.original_url
    else:
        return 'Error: URL not found', 404
```

#### Running the App

Finally, the app is run on the host `0.0.0.0` and port `5000` (or the port specified by the `PORT` environment variable).

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```


</details>

<details id="index.html">
<summary><h3>index.html</h3></summary>

The `index.html` file is the main page of the URL shortener application. It is structured as follows:

- This section sets up the HTML document and includes the title of the webpage. It also links to the CSS file for styling and the JavaScript file for interactivity.

```html
<!DOCTYPE html>
<html>
<head>
    <title>URL shortener</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/homepage_styles.css') }}">
    <script src="{{ url_for('static', filename='js/homepage_interactions.js') }}"></script>
</head>
```
- This section contains the form for URL shortening. It includes text input fields for the URL and an optional custom short URL, a checkbox to create a new short URL for an existing URL, and a submit button. It also includes conditional blocks to display messages and the short URL.

```html
<body>
    <h1>FRESH SQUEEZED URLs</h1>
    <div class="box">
        <h2> Submit URL For Squeezing</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="URL">
            <input type="text" name="custom_short_url" placeholder="(optional) Choose name">
            <div class="checkbox-line">
                <input type="checkbox" name="new_short_url" value="true">
                <span>Create new short URL for existing URL</span>
            </div>
            <input type="submit" value="Shorten">
            {% if existing %}
            <p>This URL has already been shortened. The existing short URL is: {{ short_url }}. Please choose another name.</p>
            {% endif %}
            {% if shorten_error %}
            <p>{{ shorten_error }}</p>
            {% endif %}
        </form>
        {% if short_url and not existing %}
        <div id="short-url">
            <a href="{{ short_url }}">{{ short_url }}</a>
            <button onclick="copyToClipboard('{{ short_url }}')">Copy</button>
        </div>
        {% endif %}
    </div>
```
-This section contains the form for URL expanding. It includes a text input field for the short URL and a submit button. It also includes conditional blocks to display the original URL or an error message.
```html
    <div class="box">
        <h2>Expand Short URL</h2>
        <form method="POST">
            <input type="text" name="short_url" placeholder="Short URL" >
            <input type="submit" value="Expand">
        </form>
        {% if url %}
        <div id="original-url">
            <a href="{{ url }}">{{ url }}</a>
            <button onclick="copyToClipboard('{{ url }}')">Copy</button>
        </div>
        {% elif expand_error %}
        <p>{{ expand_error }}</p>
        {% endif %}
    </div>
</body>
</html>
```


</details>
<details id="homepage_style">
<summary><h3>homepage_style.css</h3></summary>

The `homepage_styles.css` file provides the styling for the URL shortener application. It is structured as follows:

- This section sets the global styles for the body of the webpage. It sets the background color to a light gray, the font to Arial, and removes the default margin and padding.

```css
body {
    background-color: #f0f0f0;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}
```
- This section centers the text for all `h1`, `h2`, and `p` elements.

```css
h1, h2, p {
    text-align: center;
}
```
- This section styles the `.box` class, which is used to contain the forms for URL shortening and expanding. It sets the background color to white, adds padding and rounded corners, centers the box with auto margins, and sets the width and maximum width.

```css
.box {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    margin-top: 20px;
    margin-bottom: 20px;
    margin-left: auto;
    margin-right: auto;
    width: 80%;
    max-width: 900px;
    display: block;
}
```
- This section styles the form elements. It uses flexbox to arrange the `form` inputs in a column and center them.

```css
form {
    display: flex;
    flex-direction: column;
    align-items: center;
}
```

- This section styles the text input fields. It sets the width, height, and bottom margin.

```css
input[type="text"] {
    width: 300px;  
    height: 30px;
    margin-bottom: 10px;
}
```

- This section styles the `.checkbox-line` class, which is used for the line containing the checkbox and its label. It uses flexbox to align the checkbox and label, and sets the font size.

```css
.checkbox-line {
    display: flex;
    align-items: center;
    font-size: 0.8em;
}
```

- This section centers the text for the `#short-url` and `#original-url` IDs, which are used to display the short and original URLs.

```css
#short-url, #original-url {
    text-align: center;
}
```
    
</details>
<details id="homepage_interactions.js">
<summary><h3>homepage_interactions.js</h3></summary>

The `homepage_interactions.js` file provides the interactivity for the URL shortener application. It contains the following function:

- This function, copyToClipboard(text), is used to copy text to the clipboard. Here's how it works:

1. It calls the navigator.clipboard.writeText(text) method, which attempts to copy the text to the clipboard. This method returns a promise.
2. If the promise is fulfilled (i.e., the text is successfully copied), it logs a success message to the console.
3. If the promise is rejected (i.e., the text could not be copied), it logs the error to the console.

    This function is called when the "Copy" button is clicked, allowing the user to easily copy the short or original URL to their clipboard.

```javascript
/* JavaScript function to copy text to clipboard */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        console.log('Copying to clipboard was successful!');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}
```

</details>
</details>


<details id="development-process">
<summary> <h2> Development Process </h2> </summary>

The development of the URL shortener application can be broken down into two major components: the `backend`, and the `frontend`.

The main focus was to reach the mandatory functionality of the scope and ensure things would run seamlessly with basic functionality. This was done incrementally, taking each part of the project separately and then integrating everything together one part at a time. This allowed for easy testing and didn't require any long debugging process at the end of the project.

Some additional functionality was included to ensure there was some semblance of a useful application. This was kept to a minimum but could have easily been expanded in many ways. One way to make this more useful would be the implementation of different users and online server for the data base. This was considered too far out of the reach of the scope give for now but the framework was designed to ensure this could be done in the future.


<details id="backend">
<summary> <h3> Backend </h3> </summary>

Several components need to be considered when making the app. The `API`, `URL encoder`, `DB`, `error handling`, and some optional inputs to make the app more useable. 
** **
#### API Language: Flask

Flask was chosen for the backend due to its simplicity and flexibility. It doesn't enforce a specific project structure, allowing for more freedom in the design of the application. Flask also has a large and active community, which means it's easy to find solutions to problems and there are many extensions available.

*Options Considered:*

1. **Django:** Django is another Python framework that was considered. It's more robust than Flask and comes with many built-in features like an admin interface, an ORM, and authentication support. However, Django can be overkill for smaller applications and it follows a strict project structure, which can be limiting.

2. **FastAPI:** FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. It was considered for its speed and its built-in support for data validation and interactive API documentation. However, Flask was chosen for its larger community and wealth of available resources.

** **
#### URL Encoding: Base62 with Database ID

For encoding the URLs, I chose to use a **Base62 with Database ID encoding** (characters a-z, A-Z, 0-9) to generate a unique identifier for each URL. This provides a good balance between the length of the encoded string and the number of possible unique identifiers. Since the application was designed to be simple, this seemed to be the best most consistent option.  

The encoding process involves two main components: the database `ID` and the `Base62` encoding function.

1. **Database ID:** When a new URL is shortened, I generate a unique ID for it in the database. This ID is an integer that auto-increments with each new URL. This ensures that each URL has a unique identifier, which is crucial for the encoding process.

2. **Base62 Encoding Function:** This function takes the unique ID as input and encodes it into a Base62 string. The encoding process involves repeatedly dividing the ID by 62 and using the remainder to index into the character set (a-z, A-Z, 0-9). The result is a unique Base62 string that represents the ID.

*Advantages:*

- **Uniqueness:** Since each URL has a unique ID in the database, the resulting Base62 string is also unique.

- **Consistency:** The same URL will always be shortened to the same Base62 string, as long as it's not deleted from the database.

- **Efficiency:** The encoding process is fast and doesn't require any complex computations or data structures.

- **Short URLs:** Base62 encoding allows the app to represent a large number of URLs with relatively short strings.

*Disadvantages:*
- **Collision Risk:** If URLs are deleted from the database, their IDs could potentially be reused, leading to different URLs having the same short URL.

*Options Considered:*

- **Hashing functions:** such as MD5 or SHA-256, could be used to generate a unique identifier for each URL. However, these functions produce long strings and would not result in very short URLs. Additionally, they generate the same output for the same input, which could lead to collisions if two users try to shorten the same URL at the same time.

- **Random String Generation:** Generating a random string for each URL could also provide uniqueness and short URLs. However, this method would require additional checks to ensure that the same string isn't generated for different URLs. It also wouldn't provide consistency, as the same URL could be shortened to different strings.

- **Sequential IDs:** Using a simple sequential ID for each URL would ensure uniqueness and consistency, but it wouldn't provide very short URLs unless the number of URLs is very small. It also exposes the order in which URLs were shortened, which might not be desirable.

- **Base64 Encoding:** Base64 encoding could be used to generate a unique identifier for each URL. However, Base64 includes characters that are not safe for URLs, so it would require additional processing to replace these characters. It also produces longer strings than Base62 encoding.

** **

#### Database Development: SQLAlchemy with SQLite

For the database, I chose to use **SQLAlchemy with SQLite**. SQLAlchemy is a SQL toolkit and Object-Relational Mapping (ORM) system for Python, providing a full suite of well-known enterprise-level persistence patterns. SQLite is a C library that provides a lightweight disk-based database. It seemed to fit well into the scope of the project and limits any issues with sharing the project or needing to secure a server for others to use.

The database development process involves two main components:

1. **Link Model:** This is a Python class that represents the `Link` table in the database. It has three fields: `id`, `original_url`, and `short_url`. The `id` is an auto-incrementing integer that serves as the primary key. The `original_url` and `short_url` are strings that store the original URL and its shortened version, respectively.

2. **SQLAlchemy ORM:** This is used to interact with the database. It allows the app to create, query, and manipulate the `Link` objects in Python code, which is then translated into SQL commands by SQLAlchemy.

*Advantages:*

- **Simplicity:** SQLAlchemy with SQLite is easy to set up and requires minimal configuration. It's a good choice for small to medium-sized applications.

- **Portability:** SQLite databases are serverless and self-contained, meaning they can be easily copied and moved around.

- **Pythonic:** SQLAlchemy allows the app to interact with the database using Python code instead of writing SQL commands.

- **Flexibility:** SQLAlchemy supports multiple database systems, not just SQLite. If I decide to switch to a different database in the future, I can do so with minimal changes to the code.

*Disadvantages:*

- **Scalability:** SQLite is not the best choice for very large applications or applications with high concurrency, as it can only handle a limited number of simultaneous writes.

- **Lack of Certain Features:** SQLite does not support some features that are available in other database systems, such as RIGHT and FULL OUTER JOIN.

*Options Considered:*

- **PostgreSQL:** This is a powerful, open-source object-relational database system. It's a good choice for large applications, but it's more complex to set up and manage than SQLite.

- **MySQL:** This is another popular open-source database system. It's more scalable than SQLite, but it's also more complex and requires a separate server to run.

- **NoSQL databases:** These databases, such as MongoDB or CouchDB, are more flexible and scalable than SQLite. However, they have a different data model and do not support SQL, which might not be suitable for this application.

** **

#### Error Handling
The application uses a simple approach to error handling, primarily through the use of conditional statements to check for potential issues and set appropriate error messages.

For instance, when processing form data, I check if the original URL already exists in the database or if a custom short URL is already in use. If either of these conditions is true, I set an error message to be displayed on the home page.

Similarly, when a user attempts to access a short URL, I check if the short URL exists in the database. If it doesn't, I return a 404 error.

*Advantages:*
- **Simplicity:** This approach is straightforward and easy to implement. It doesn't require any additional libraries or complex logic.

- **User-Friendly:** By setting error messages to be displayed on the home page, I provide feedback to the user about what went wrong.

*Disadvantages:*
- **Limited Scope:** This approach only handles a few specific errors. There may be other potential issues that are not currently being checked for.

- **Lack of Detailed Error Information:** The error messages are quite generic and may not provide enough information for debugging more complex issues.

Despite these disadvantages, I chose this simple approach due to the limited scope and time of the project. For a larger or more complex application, a more comprehensive error handling system might be necessary.

** **

#### Bonus Features

In addition to the core functionality, the application includes several bonus features that enhance the user experience and provide additional options for URL shortening.

1. **Optional Personal URL:** Users have the option to create a personal short URL. This allows users to create memorable or meaningful short URLs, which can be useful for branding or ease of use.

2. **Recall Previously Shortened URLs:** If a user tries to shorten a URL that has already been shortened, the application will recall and return the previously shortened URL. This prevents the creation of multiple short URLs for the same original URL, keeping the database clean and efficient.

3. **Force Create New URL:** Despite the above feature, users have the option to force the creation of a new short URL for an already shortened original URL. This can be useful in situations where different short URLs for the same original URL are needed, for example, for tracking clicks from different sources.

4. **Easy Copy Button for URLs:** To make it easy for users to copy the shortened URL, we've added a copy button next to the URL. This eliminates the need for manual text selection and copying, improving the user experience.


</details>

<details id="frontend">
<summary><h3>Frontend</h3></summary>

The frontend of the application was developed using HTML, CSS, and JavaScript. I used the Flask framework's templating engine, Jinja2, to dynamically generate HTML pages. The main goal was to make something useable but simple as to not use too much time on development. There was still an attempt to play with the visuals to ensure the page didn't look too difficult to understand. Along with the user-friendly options implemented the project is very simple-looking but easily expanded upon.

- **HTML:** Structures the content of the web pages. This includes forms for users to input URLs they want to shorten, tables to display the shortened URLs, and buttons for actions like copying the URL.

- **CSS:** This includes setting colors, fonts, and layout properties to make the application visually appealing and user-friendly.

- **JavaScript:** I used JavaScript to add interactivity to the web pages. This includes actions like copying the shortened URL to the clipboard when the copy button is clicked.

- **Jinja2 Templating:** This enables inserting variables and other dynamic content into the HTML. For example, it can generate a table row for each URL in the database.

The development process involved designing the user interface, implementing the HTML structure, adding styles with CSS, and then adding interactivity with JavaScript. Then integrated the frontend with the backend using Flask and Jinja2.

</details>
</details>



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
