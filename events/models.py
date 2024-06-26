from django.db import models
from accounts.models import User
class MainEvent(models.Model):
    title = models.CharField(max_length=500,null=True)
    image = models.ImageField(upload_to='main_event_images',null=True)
    
    def __str__(self):
        return self.title
    

class SubEvent(models.Model):
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to='sub_event_images',null=True)
    game = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True)
    rules = models.TextField(null=True)
    main_event = models.ForeignKey(MainEvent,on_delete=models.CASCADE)
    college = models.CharField(max_length=500, null=True, blank=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.title
    
class College(models.Model):
    name = models.CharField(max_length=200)
    