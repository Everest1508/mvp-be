from django.db import models

class MainEvent(models.Model):
    title = models.CharField(max_length=500,null=True)
    image = models.ImageField(upload_to='main_event_images',null=True)

class SubEvent(models.Model):
    title = models.CharField(max_length=500)
    # game = models.ForeignKey(Games, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True)
    rules = models.TextField(null=True)
    main_event = models.OneToOneField(MainEvent,on_delete=models.CASCADE)
