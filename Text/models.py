from django.db import models
#from mongoengine import *

# Create your models here.


class API(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField()
    

    class Meta:
        ordering = ('created',)

'''
class API_Mongo(DynamicDocument):
    content = StringField( required=True)

'''    
    

    
