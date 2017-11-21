import unittest
from models import User
class UserAuthTestcase(unittest.TestCase):
    def setUp(self):
        self.new_user = User()
    
    def tearDown(self):
        pass 

    def test_user_registration(self):
        test = self.new_user.create_account('testacc', 'password')
        self.assertTrue(test.check_user('testacc'))
    
    def test_user_login(self):
        pass

    def test_failed_login(self):
        pass

    def test_duplicate_usernames(self):
        pass