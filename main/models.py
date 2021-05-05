from django.db import models
from django.contrib.auth.models import User


class Material(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
    verbose_name='Владелец статьи', blank=True, null=True)
    name = models.CharField(max_length=250)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Comments(models.Model):
    article = models.ForeignKey(Material, on_delete = models.CASCADE, verbose_name='Статья', blank = True, null = True,related_name='comments_articles' )
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Автор комментария', blank = True, null = True )
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость статьи', default=False)
