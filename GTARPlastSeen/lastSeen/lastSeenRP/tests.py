from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone


from .models import Appearance
# Create your tests here.

class AppearanceModelTests(TestCase):

    def test_appearance_is_before_right_now(self):
        ''' form should not accept appearances of a character that appear in the future '''

        time = datetime.now() + timedelta(days=30)
        future_appearance = Appearance(date_of_appearance=time)
        self.assertIs(future_appearance.recently_published(), False)

    def test_was_published_recently_with_old_appearance(self):
        '''was_published_recently() returns False for appearances that were published more than a day ago'''

        time = datetime.now() - timedelta(days=1, hours=1)
        old_appearance = Appearance(date_of_appearance=time)
        self.assertIs(old_appearance.recently_published(), False)


    def test_was_published_recently_with_recent_appearance(self):
        '''was_published_recently() returns True for appearances that were published within the last day'''

        time = datetime.now()
        recent_appearance = Appearance(date_of_appearance=time)
        self.assertIs(recent_appearance.recently_published(), True)

        