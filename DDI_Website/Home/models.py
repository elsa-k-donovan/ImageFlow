from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class UserExtensionModel(models.Model):
    """
    This extends the User Model, with just one addition

    arrayTasksCompleted holds an array of the task numbers the specific user has queried,
    so that when i show the results in twitter, I only get the user specific searches
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    arrayTasksCompleted = ArrayField(base_field = models.IntegerField())

    class Meta: # Name in PostgreSQL database
            db_table = "user_extension_model"
        

