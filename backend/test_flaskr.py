import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        my_password = "Asdfasdf1!"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', my_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_categories'], 6)

    def test_get_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['total_questions'])

    def test_get_questions_out_of_bounds(self):
        res = self.client().get('/questions?page=99999999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_get_questions_delete(self):
        toDelete = Question(question='Unit Test Question',
                            answer='Delete',
                            difficulty=1,
                            category=1)
        toDelete.insert()
        res = self.client().delete('/questions/{}'.format(toDelete.id))
        data = json.loads(res.data)
        deletedID = toDelete.id
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(Question.query.filter(Question.id == deletedID).one_or_none(), None)

    def test_get_questions_delete_fail(self):
        res = self.client().delete('/questions/{}'.format(55555555))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_question(self):
        toSubmit = {
            "question": 'Unit Test Question',
            "answer": 'Create',
            "difficulty": 1,
            "category": 1
        }

        res = self.client().post('/questions', json=toSubmit)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_question_fail(self):
        toSubmit = {
            "question": '',
            "answer": '',
            "difficulty": 1,
            "category": 1
        }

        res = self.client().post('/questions', json=toSubmit)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_questions_based_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 'Art')
        self.assertTrue(data['questions'])

    def test_get_questions_based_category_fail(self):
        res = self.client().get('/categories/999999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_search_questions(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'a'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    def test_search_questions_false(self):
        res = self.client().post('/questions/search', json={'searchTerm': '90834302932094023djsfo'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': [18], 'quiz_category':
            {'type': 'Entertainment', 'id': '5'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 5)

    def test_quiz_fail(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()