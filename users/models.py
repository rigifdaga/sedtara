from django.db import models

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    email = models.CharField(unique=True, max_length=255)
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'

class StudentDetails(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    education_level = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'student_details'