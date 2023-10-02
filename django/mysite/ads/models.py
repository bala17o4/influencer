from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_influencer = models.BooleanField(default=False)
    is_advertiser = models.BooleanField(default=False)

class Post(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)

    

    def __str__(self):
        return f"{self.title} by {self.author}"
    
class Ad(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads")
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="adlikes", blank=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author}"
    
class AppliedBy(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="appliedby")
    influencer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appliedby")
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad} by {self.influencer}"

