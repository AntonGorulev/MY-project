from django.db import models

# Create your models here.


class Material(models.Model):
    name = models.CharField(max_length=250)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name