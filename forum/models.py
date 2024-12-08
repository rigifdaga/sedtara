from django.db import models

class Questions(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    question_attachment = models.CharField(max_length=1024, blank=True, null=True)
    asker = models.ForeignKey('users.StudentDetails', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'questions'

class Answers(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question = models.ForeignKey('Questions', models.DO_NOTHING)
    student = models.ForeignKey('users.StudentDetails', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    answer_text = models.TextField()
    answer_attachment = models.CharField(max_length=1024, blank=True, null=True)
    is_best_answer = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'answers'