import datetime 

from django.utils import timezone
from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    def was_published_recent(self):
        now = timezone.now()
        # should return false if pub_date is in the future
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

        was_published_recent.admin_order_field = 'pub_date'
        was_published_recent.boolean = True
        was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text