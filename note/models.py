from django.db import models

# Create your models here.
class AddNote(models.Model):
    username = models.CharField(max_length=122)
    title = models.CharField(max_length=1000)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.username