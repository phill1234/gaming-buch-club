from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title

    def pub_date_pretty(self):
        return self.date.strftime("%b %e %Y")
