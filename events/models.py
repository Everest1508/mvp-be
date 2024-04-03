from django.db import models

class MainEvent(models.Model):
    title = models.CharField(max_length=500,null=True)
    image = models.ImageField(upload_to='main_event_images',null=True)
    
    def __str__(self):
        return self.title
    

class SubEvent(models.Model):
    title = models.CharField(max_length=500)
    game = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True)
    rules = models.TextField(null=True)
    main_event = models.ForeignKey(MainEvent,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    