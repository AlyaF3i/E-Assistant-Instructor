from django.urls import path
from . import views

urlpatterns = [
    # User and Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    # Classroom-related URLs
    path('classroom/create/', views.create_classroom_and_studyplan, name='create_classroom_and_studyplan'),  # Merged with study plan
    path('classroom/<int:classroom_id>/', views.get_classroom_details, name='get_classroom_details'),
    path('classrooms/', views.get_classrooms, name='get_classrooms'),

    # Sections
    path('section/<int:section_id>/', views.get_section_data, name='get_section_data'),

    # Content, Mindmap, and Assignments (merged)
    path('content-or-mindmap/', views.create_content_or_mindmap, name='create_content_or_mindmap'),

    # URL to create quiz assignment
    path('quiz/create-assignment/', views.quiz_assignment, name='create_quiz_assignment'),

    # URL to get quiz or assessment results
    path('quiz/assessment-results/', views.get_assessment_results, name='get_assessment_results'),

    # URL to add student answers (used when a student submits quiz answers)
    # path('quiz/student-answer/', views.add_student_answer, name='add_student_answer'),
    path('api/quiz/<uuid:quiz_uuid>/', views.get_quiz, name='get_quiz'),
    path('quiz/<uuid:quiz_uuid>/submit/', views.submit_quiz, name='submit_quiz'),

    # URL to get student marks for a classroom
    # path('quiz/student-mark/<int:classroom_id>/', views.get_student_mark, name='get_student_mark'),
    
    # Generate and send support content URL
    path('quiz/support-content/', views.generate_and_send_support_content, name='generate_and_send_support_content'),

    # Student-related URLs
    path('add-student/', views.add_student, name='add_student'),  # Added endpoint for adding students
    path('classroom-student/<int:classroom_id>/', views.get_classroom_student, name='get_classroom_student'),

]
