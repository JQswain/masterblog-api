#Masterblog
Masterblog is a basic blog application built with Flask. It includes a RESTful API and a simple HTML+JavaScript frontend. It also includes Swagger UI for interactive API documentation.

##Features
View all blog posts

Add new posts

Edit or delete existing posts

Search posts by title or content

Sort posts by title or content

Swagger documentation for the API

##Project Structure
php
Copy
Edit
masterblog/
├── app.py                # Backend API (runs on port 5002)
├── frontend.py           # Frontend server (runs on port 5001)
├── static/
│   ├── masterblog.json   # Swagger API definition
│   ├── styles.css        # Styles for the frontend
│   └── main.js           # JavaScript logic for the frontend
├── templates/
│   └── index.html        # Frontend homepage

##Setup Instructions
1. Install Dependencies
Make sure Python 3 is installed. Then install the required packages:

nginx
Copy
Edit
pip install flask flask-cors flask-swagger-ui
2. Run the Backend API
nginx
Copy
Edit
python app.py
The backend will start on:
http://localhost:5002
Swagger UI will be available at:
http://localhost:5002/api/docs

3. Run the Frontend App
In a separate terminal:

nginx
Copy
Edit
python frontend.py
The frontend will be available at:
http://localhost:5001

##API Endpoints
Method	Endpoint	Description
GET	/api/posts	Get all posts (with sorting)
POST	/api/posts	Create a new post
PUT	/api/posts/{post_id}	Update an existing post
DELETE	/api/posts/{post_id}	Delete a post by ID
GET	/api/posts/search	Search by title and/or content

##Notes
Use the Swagger UI at /api/docs to test the API.

Posts are stored in memory and reset on server restart.

##License
This project is for learning and demonstration purposes.
