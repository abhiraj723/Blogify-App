from django.db import models

# Create your models here.

class LoginInfo(models.Model):
    usertype = models.CharField(max_length=15)    # user, admin
    user = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=256)

class Reader(models.Model):
    GENDER_CHOICES = (
        ('male','Male'),
        ('female','Female'),
        ('Na','prefer not to say')
    )
    user = models.OneToOneField(LoginInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    author = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images/",blank=True,null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
