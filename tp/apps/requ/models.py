from django.contrib.auth.models import User
from django.db import models


class Request(models.Model):
    text = models.TextField('Текст заявки')
    is_solved = models.BooleanField('Проблема решена')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    solver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solver', blank=True, null=True)
    pub_date = models.DateTimeField('дата публикации')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Comment(models.Model):
    text = models.CharField('текст комментария', max_length=255)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
