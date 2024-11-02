from django.contrib import admin
from .models import Profile, Classroom, Section, Content, Student, StudentAssessment, QuizAssignment, SupportContent, Question

# Register all models in the admin panel
admin.site.register(Profile)
admin.site.register(Classroom)
admin.site.register(Section)
admin.site.register(Content)
admin.site.register(Student)
admin.site.register(StudentAssessment)
admin.site.register(QuizAssignment)
admin.site.register(SupportContent)
admin.site.register(Question)
