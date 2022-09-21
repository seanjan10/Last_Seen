import datetime

from django.test import TestCase
from django.utils import timezone


from .models import Appearance
# Create your tests here.

class AppearanceModelTests(TestCase):

    def test_appearance_is_before_right_now(self):
        ''' form should not accept appearances of a character that appear in the future '''

        time = timezone.now() + datetime.timedelta(days=1)
        future_appearance = Appearance(date_of_appearance=time)
        self.assertIs(future_appearance.recently_published(), False)