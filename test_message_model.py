''' Message Model Test '''

import os
from unittest import TestCase
from models import db, User, Message, Follows
from sqlalchemy import exc

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""
    
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()
        self.uid = 94566
        u = User.signup("testing", "testing@test.com", "password", None)
        u.id = self.uid
        db.session.commit()
        self.u = User.query.get(self.uid)
        self.client = app.test_client()
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):

        msg = Message(
            text = "I am NOT a cat",
            user_id=self.uid
        )

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "I am NOT a cat")

        db.session.delete(msg)
        db.session.commit()

        self.assertEqual(len(self.u.messages), 0)

    def test_message_likes(self):
        msg1 = Message(
            text = "I am NOT a cat",
            user_id=self.uid
        )

        msg2 = Message(
            text = "I am a dog",
            user_id=self.uid
        )
        u = User.signup("testing1", "testing1@test.com", "password", None)
        uid = 5
        u.id = uid
        db.session.add_all([msg1, msg2, u])
        db.session.commit()

        
        u.liked_messages.append(msg1)

        db.session.commit()

        self.assertEqual(len(u.liked_messages), 1)