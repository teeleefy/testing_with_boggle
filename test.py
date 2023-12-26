from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
app.config['DEBUG_TB_HOSTS']= ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        '''Required set-up before running each test'''
        self.client = app.test_client()
        app.config["TESTING"] = True
        with self.client as client:
            # Set up the session with your own information first using session_transaction:
            with client.session_transaction() as change_session:
                # Design a board to test
                change_session['board'] = [['C','R','A','S','H'],
                                           ['A','P','P','L','E'],
                                           ['T','A','L','I','A'],
                                           ['C','L','E','C','R'],
                                           ['H','I','O','K','T']]

    def test_home(self):
        with self.client:
            response = self.client.get('/')
            html = response.get_data(as_text=True)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('times_played'))
            self.assertIn("Words Found:", html)
            self.assertIn("Score:", html)
            self.assertIn("Seconds Left:", html)

    def test_valid_word(self):
        '''Appropriately responds to a valid boggle word'''
        # with self.client as client:
        #     # Set up the session with your own information first using session_transaction:
        #     with client.session_transaction() as change_session:
        #         # Design a board to test
        #         change_session['board'] = [['C','R','A','S','H'],
        #                                    ['A','P','P','L','E'],
        #                                    ['T','A','L','I','A'],
        #                                    ['C','L','E','C','R'],
        #                                    ['H','I','O','K','T']]
        response = self.client.get('/check-word?new_word=heart')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        '''Test if "check_valid_word" in boggle.py is appropriately catching invalid words'''
        response = self.client.get('/check-word?new_word=dollar')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_a_word(self):
        '''Verifies that the game is appropriately responding to strings that are not a word'''
        self.client.get('/')
        response = self.client.get('/check-word?new_word=tacocat')
        self.assertEqual(response.json['result'], 'not-word')

    # def test_post_score(self):
    # #     '''Test to see if app appropriately posts score at end of game and counts times played'''
    #     with self.client:
    #         self.client.post('/post-score', data={"score": "5"})
            
    #         self.assertEqual(session.get('highscore'), 5)
            

    # def tearDown(self):
    #     '''Stuff to do after each test'''

    