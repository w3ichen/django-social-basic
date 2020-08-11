from django.db import models
from django.utils import timezone               # used to get current time
from django.contrib.auth.models import User     # used to get user of post
class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	date_posted = models.DateTimeField(default=timezone.now)

class Post(models.Model):
	content = models.TextField(blank=False, null=False)
	date_posted = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	likes_count = models.DecimalField(decimal_places=0, max_digits=1000, default=0)
	likes = models.ManyToManyField(User, related_name="blog_likes")
	comments = models.ManyToManyField(Comment, related_name='comments')
	comments_count = models.DecimalField(decimal_places=0, max_digits=1000, default=0)