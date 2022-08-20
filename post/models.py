from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=512, null=True, blank=True)
    description = RichTextField(blank=True, null=True)
    liked_by = models.ManyToManyField(User, null=True, blank=True)
    image = models.ImageField(upload_to ='uploads/')
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name='post_created_by',null=True)
    updated_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name='post_updated_by',null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id}--{self.title}"
class Followed(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE,null=True,blank=True)
	friends = models.ManyToManyField(User,null=True, blank=True,related_name='friends_user')
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.user.username} Followed"
