import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selections):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selections]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={"/": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.all()
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type

            return jsonify({
              'success': True,
              'categories': categories_dict,
              'total_categories': len(categories_dict)
            })
        except:
            abort(404)

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions')
    def get_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            if len(questions) == 0:
                abort(404)
            categories = Category.query.all()
            questions_listings = paginate_questions(request, questions)
            categories_dict = {}
            current_categories = []
            for question in questions_listings:
                current_categories.append(question['category'])
            for category in categories:
                categories_dict[category.id] = category.type
            if len(current_categories) == 0:
                abort(404)
            return jsonify({
              'success': True,
              'questions': questions_listings,
              'categories': categories_dict,
              'current_category': current_categories,
              'total_questions': len(questions)
            })
        except:
            abort(404)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            questionToDelete = Question.query.filter_by(id=question_id).first()
            if questionToDelete is None:
                abort(404)
            questionToDelete.delete()
            return jsonify({
              'success': True,
              'deleted': question_id
            })
        except:
            abort(404)

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            body = request.get_json()
            question = body.get('question', None)
            answer = body.get('answer', None)
            category = body.get('category', None)
            difficulty = body.get('difficulty', None)
            if body.get('question') == '' or body.get('answer') == '':
                abort(422)

            question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            question.insert()

            return jsonify({
              'success': True,
              'created': question.id,
              'question': question.question,
              'category': question.category,
              'total_questions': len(Question.query.all())
            })
        except:
            abort(422)

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        searchWord = body.get('searchTerm', None)
        try:
            searchQuestions = \
                Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(searchWord))).all()
            if len(searchQuestions) == 0:
                abort(404)
            paginatedQuestions = paginate_questions(request, searchQuestions)
            return jsonify({
                'success': True,
                'questions': paginatedQuestions,
                'total_questions': len(searchQuestions)
            })

        except:
            abort(404)

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def getCategoryQuestions(id):
        try:
            questions = Question.query.filter_by(category=id).all()
            paginatedQuestions = paginate_questions(request, questions)
            return jsonify({
              'success': True,
              'questions': paginatedQuestions,
              'current_category': Category.query.get(id).type,
              'total_questions': len(questions)
            })
        except:
            abort(404)
    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/quizzes', methods=['POST'])
    def getQuiz():
        def checkUsed(question):
            used = False
            if question.id in previous_questions:
                used = True

            return used

        try:
            body = request.get_json()
            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            if category is None:
                abort(404)

            if category['id'] != 0:
                select = Question.query.filter_by(category=category['id']).all()
            else:
                select = Question.query.all()

            next_question = select[random.randrange(0, len(select), 1)]
            while checkUsed(next_question):
                next_question = select[random.randrange(0, len(select), 1)]
            return jsonify({
                'success': True,
                'question': next_question.format()
              })

        except:
            abort(404)

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "Not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "resource not found"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
          "success": False,
          "error": 500,
          "message": "internal server error"
        }), 500

    return app
