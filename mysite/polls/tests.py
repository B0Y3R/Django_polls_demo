import datetime
from django.http import response 

from django.test import TestCase
from django.utils import timezone 
from django.urls import reverse

from .models import Question 

# Create your tests here.

def create_question(question_text, days):
    """
        Create a question with the given `question_text` 
        and published given the number of `days` offset to now
        (negative for questions published in the past, postive 
        for questions that have yet to be published)
    """

    time = timezone.now() + datetime.timedelta(days=days)

    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):

    def test_no_questions(self):
        """
            If no questions exist, an appropriate message is dispalyed.
        """

        # call page polls index 
        response = self.client.get(reverse('polls:index'))
        
        # expect to find the page, an have a 200 status code 
        self.assertEqual(response.status_code, 200)

        # expect that there are now questions (we haven't created any), and that a message is present
        self.assertContains(response, "No polls are available")

        # expect the query_set to return an empty list 
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_past_question(self):
        """
            Questions with a pub_date in the past are displayed on the index page.
        """

        # create a question with our helper func
        create_question(question_text="Past question.", days=-30)

        # call page polls index 
        response = self.client.get(reverse('polls:index'))

        # expect to find the question we just created in the query_set
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_future_question(self):
        """
            Questions with a pub_date in the future are NOT displayed on the index page.
        """

        # create a question with our helper func
        create_question(question_text="Future question.", days=30)

        # call page polls index 
        response = self.client.get(reverse('polls:index'))

        # expect response to return a message about no polls being found 
        self.assertContains(response, "No polls are available.")
    

    
    def test_future_and_past_question(self):
        """
            If both future and past questions exist,
            only the past questions are displayed
        """

        create_question(question_text="Past Question.", days=-30)
        create_question(question_text="Future Question.", days=30)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question.>'])

    def test_two_past_questions(self):
        """
            The questions index page may display muiltiple questions
        """

        create_question(question_text="Past Question 1", days=-5)
        create_question(question_text="Past Question 2", days=-30)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question 1>', '<Question: Past Question 2>'])
    
    def test_was_published_recent_with_future_question(self):
        """ 
            was_published_recent() returns 
            False for questions whose pub_date
            is in the future. 
        """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recent(), False)
    
    def test_was_published_recent_with_old_question(self):
        """
            was_publilshed_recent() returns
            False for questions whose pub_date
            is older than 1 day 
        """

        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        one_day_old_question = Question(pub_date=time)

        self.assertIs(one_day_old_question.was_published_recent(), False)

    def test_was_published_recent_with_recent_question(self):
        """
            was_published_recently() returns
            True for questions whose pub_date
            is within the last day.
        """

        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59);
        within_last_day_question = Question(pub_date=time)
        
        self.assertIs(within_last_day_question.was_published_recent(), True)

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
            The detail view of a question with
            a pub_date in the future returns 
            a 404 not found.
        """

        future_question = create_question(question_text='Future Question', days=30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
            The detail view of a question with 
            a pub_date in the past displays
            the questions text.
        """

        past_question = create_question(question_text='Past Question', days=-30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTexts(TestCase):

    def test_future_question(self):
        """
            The results view of a question with
            a pub_date in the future returns a 
            404 not found. 
        """

        future_question = create_question(question_text='Future Question', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
            The result view of a question with
            a pub_date in the past returns the 
            questions text
        """

        past_question = create_question(question_text='Past Question', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)

        self.assertContains(response, 'Past Question')