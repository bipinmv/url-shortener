from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Url(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    url=models.URLField(max_length=300)
    shorturl=models.URLField(max_length=200)
    urlkey=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.url
    