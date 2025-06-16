from datetime import datetime

from server.app import app  # update to correct import if needed
from server.models import db, Message  # ensure correct path to models

class TestMessage:
    '''Message model in models.py'''

    def setup_method(self):
        '''Push app context and clear test messages'''
        self.app_context = app.app_context()
        self.app_context.push()

        Message.query.filter_by(username="Liza", body="Hello 👋").delete()
        db.session.commit()

    def teardown_method(self):
        '''Pop app context after each test'''
        db.session.remove()
        self.app_context.pop()

    def test_has_correct_columns(self):
        '''has columns for message body, username, and creation time.'''
        hello_from_liza = Message(
            body="Hello 👋",
            username="Liza"
        )
        db.session.add(hello_from_liza)
        db.session.commit()

        assert hello_from_liza.body == "Hello 👋"
        assert hello_from_liza.username == "Liza"
        assert isinstance(hello_from_liza.created_at, datetime)

        db.session.delete(hello_from_liza)
        db.session.commit()
