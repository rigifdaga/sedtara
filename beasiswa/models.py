from django.db import models

class Scholarship(models.Model):
    scholarship_id = models.AutoField(primary_key=True)
    education_level = models.CharField(max_length=255)
    scholarship_name = models.CharField(max_length=255)
    description = models.TextField()
    end_date = models.DateField(null=True, blank=True)
    provider = models.CharField(max_length=255, null=True, blank=True)
    benefit = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'scholarship'
