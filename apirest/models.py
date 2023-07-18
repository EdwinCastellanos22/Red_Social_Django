from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
# Create your models here.


class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    image= models.ImageField(default='profile.png', upload_to= 'profile/')
    create_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

class Chat(models.Model):
    users= models.ManyToManyField(User)

    

class Message(models.Model):
    mr_id= models.AutoField(primary_key=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    sender= models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    content= models.TextField()
    timestap= models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}->{self.sender.username} : {self.content}"
    

      
    
class Post(models.Model):
    post_id= models.AutoField(primary_key=True)
    image= models.ImageField(default= 'post.png', upload_to= 'post/')
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    title= models.CharField(max_length=200)
    content= models.TextField()
    likes= models.ManyToManyField(User, related_name='post_like', blank=True)
    dislikes= models.ManyToManyField(User, related_name='post_dislike', blank=True)
    timestap = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} :: {self.title}"

    class Meta:
        ordering= ['-timestap']
    
class Comment(models.Model):
    post= models.ForeignKey(Post, on_delete= models.CASCADE, related_name='comment')
    author= models.ForeignKey(User, on_delete= models.CASCADE, related_name='comment')
    content= models.TextField(max_length=200, null=True)
    timestap= models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author.username
    
    class Meta:
        ordering= ['-timestap']