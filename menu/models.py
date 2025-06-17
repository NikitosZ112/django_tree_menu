from django.db import models
from django.urls import reverse, NoReverseMatch

class Menu(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return self.name

    icon = models.CharField(max_length=50, blank=True, help_text="Например: 'fa-home' для FontAwesome")

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField('Заголовок', max_length=100)
    url = models.CharField('URL', max_length=255, blank=True)
    named_url = models.CharField('Named URL', max_length=100, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return self.url or '/'
        return self.url or '/'