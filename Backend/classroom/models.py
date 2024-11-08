from django.db import models
from django.contrib.auth.models import User
import uuid

# User Model extension
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

# Classroom model
class Classroom(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    level = models.CharField(max_length=50)
    disability = models.CharField(max_length=100, blank=True, null=True)
    extra = models.TextField(blank=True, null=True) # remark
    num_of_sections = models.IntegerField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classrooms")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_student_count(self):
        return self.students.count()
    
    def __str__(self):
        return f"{self.subject} - {self.level}"

class Section(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    # section_type = models.CharField(max_length=255)  # Lecture, Quiz, Assignment, etc.
    index = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.section_name} ({self.section_type})"
    def get_student_count(self):
        return self.classroom.students.count()

# Content model to generate lesson content
class Content(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=255)  # E.g., "PDF", "Presentation"
    generated_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Content for {self.section.section_name} ({self.content_type})"

# Student model
class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="students")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Quizzes and Assignments Model
class QuizAssignment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)  # Quiz or Assignment
    is_support_content_created = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f"{self.type} for {self.section.title}"  # Assuming section has a title attribute

# Question Model
class Question(models.Model):
    assessment = models.ForeignKey(QuizAssignment, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_answer = models.IntegerField()  # Use 0-3 to represent answer options (1-based index)

    def __str__(self):
        return f"Question for {self.assessment.type}: {self.question_text}"
# Student Assessment Model
class StudentAssessment(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Unique identifier
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="assessments")
    quiz_assignment = models.ForeignKey(QuizAssignment, on_delete=models.CASCADE)  # No default value needed
    marks = models.DecimalField(max_digits=5, decimal_places=2, default=-1)  # Default -1 indicates not graded
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name}'s assessment for {self.quiz_assignment.type}"
    
class StudentAnswer(models.Model):
    student_assessment = models.ForeignKey(StudentAssessment, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.IntegerField()  # Storing selected answer index (0-3)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer for {self.student_assessment.student.name} on {self.question.question_text}"

# Support content for students based on quiz or assignment performance
class SupportContent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz_assignment = models.ForeignKey(QuizAssignment, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support content for {self.student.name} on {self.quiz_assignment}"
