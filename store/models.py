from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Box(models.Model):
    length = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    area = models.IntegerField(default=0)
    volume = models.IntegerField(default=0)
    createdBy = models.ForeignKey(User,related_name ="createdBy",on_delete=models.CASCADE)
    createdOn = models.DateTimeField(default=datetime.now)
    updatedOn = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return str(self.pk)

    def get_area(self):
        l = self.length
        w = self.width
        h = self.height
        return 2*( (l * w) + (l * h) + (w * h) )

    def get_volume(self):
        l = self.length
        w = self.width
        h = self.height
        return (l * w * h)
    
    def save(self, *args, **kwargs):
        self.area = self.get_area()
        self.volume = self.get_volume()
        self.updatedOn = datetime.now()
        super(Box, self).save(*args, **kwargs)


    
    