# Fast API Tutorial with Database

I followed a tutorial that did a simple get request to a postgresql database as well as post.

From there, I added update/put and delete requests. I also added a make_requests.py file to programatically make the requests.

This project helped me understand the fundamentals of building a database and populating it using sqlalchemy.

After initially using postgresql on my local machine as the database, I researched how to use a local database next to my code (quizapplication.db) and replaced the postgresql database with this one. Worked perfectly!

## Instructions

Clone repository to local machine:  
`git clone git@github.com:mike-jacks/fast-api-tutorial-with-database.git`

Create a new python environment:  
`python -m venv .venv`

Run uvicorn server in terminal:  
`uvicorn main:app --reload`

Run make_requests.py in separate terminal:  
`python make_requests.py`
