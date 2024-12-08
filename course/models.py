from django.db import models

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    teacher = models.ForeignKey('users.Users', models.DO_NOTHING)
    token = models.CharField(max_length=6)
    visibility = models.BooleanField()
    course_image = models.TextField(blank=True, null=True)
    course_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'

class CourseStudent(models.Model):
    course = models.OneToOneField(Course, models.DO_NOTHING, primary_key=True)  # The composite primary key (course_id, student_id) found, that is not supported. The first column is selected.
    student = models.ForeignKey('users.StudentDetails', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'course_student'
        unique_together = (('course', 'student'),)

class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, models.DO_NOTHING)
    module_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'module'

class Materials(models.Model):
    material_id = models.AutoField(primary_key=True)
    module = models.ForeignKey('Module', models.DO_NOTHING)
    material_title = models.CharField(max_length=255)
    material_attachment = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'materials'

class Assignments(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    module = models.ForeignKey('Module', models.DO_NOTHING)
    assignment_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assignment_attachment = models.CharField(max_length=1024, blank=True, null=True)
    deadline = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'assignments'