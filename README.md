## Full Stack Trivia



## Installation Instructions

1. Download repository; make sure you have python installed
2. Go to the terminal and cd to the backend of the project
3. Set up virtual environment at https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
4. Install dependencies by typing in terminal : pip install -r requirements.txt
5. Set up database by typing psql trivia < trivia.psql
6. To run the back end server, type flask run --reload
7. To run front end, cd to frontend and type npm start
8. To run test cases, type:

dropdb trivia_test


createdb trivia_test


psql trivia_test < trivia.psql


python test_flaskr.py



## API Documentation

## Getting Started

-Base URL: At present, this app can only be run locally through http://localhost:3000/ 
-Authentication: Currently no authentication is required.

## Error Handling

Errors are returned in JSON objects in the following format:

{
"success": False,
"error": 404,
"message": "Not found"
}

4 error types : 400, 402, 404, 500


## Endpoints

## GET /categories

-Returns a list of categories, success value, and number of total categories

curl http://localhost:5000/categories
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}


## GET /questions

-Returns a list of questions, categories, current category, success value, and total number of questions.
-Questions are paginated 10 at a time

curl http://localhost:5000/questions

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": [
    6, 
    6, 
    3, 
    3, 
    3, 
    2, 
    2, 
    2, 
    2, 
    1
  ], 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ], 
  "success": true, 
  "total_questions": 29
}


## DELETE questions/<question_id>
-Deletes question that has id question_id (user choice) from the list of questions
-Returns success value and id of the deleted question

curl -X DELETE http://localhost:3000/questions/10

{
     'success': True,
     'deleted': 10
}


## POST questions
-Creates a new question, taking in the question, answer, category, and difficulty score
-Must contain question and answer

curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d '{'question': 'Who was the first president?', 'answer': 'George Washington', 'category': 'History', 'difficulty': 2}'

{
  'success': True,
  'created': 1
  'question': 'Who was the first president?'
  'category': History,
  'total_questions': 1
}


## POST questions/search
-Searches a question, querying through database for words that contain the substring
-Returns the list of matches, along with the amount of matches
-Sends error if no matches

curl -X POST http://localhost:5000/questions/search -H "Content-Type: application/json" -d '{'searchTerm': 'president'}'

{
  'success': True,
  'questions': 'Who was the first president?'
  'total_questions': 1
}


## GET categories/<id>/questions 
-Gets questions in category that has id.
-Returns list of questions in that selected category, with pagination of 10

curl http://localhost:5000/categories/1/questions
  
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
  
  
## POST quizzes
-Plays quiz of selected category
-Returns success value and random question in that category that has also not been seen before

curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{'quiz_category': 'History', 'previous_questions': []}'

{
  'success': True,
  'question': 'Who was the first president?'
}
