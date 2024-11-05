from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Student, Content, Section, Profile, Classroom, QuizAssignment, StudentAssessment, Question, StudentAnswer, SupportContent
from .watsonx_utils import call_llm, get_sections, get_questions
from .mind_map import MindMapGenerator
from .powerpoint import PowerPointGenerator
from .email_utils import send_quiz_assignment
from threading import Thread
from rest_framework import status
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from arabic_reshaper import reshape
import io
from uuid import uuid4
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from .swagger_serializers import (
    add_student_response_schema,
    add_student_request_schema,
    add_student_404_response_schema,
    generate_support_content_request_schema,
    generate_support_content_response_schema,
    generate_support_content_404_response_schema,
    get_assessment_results_response_schema,
    get_assessment_results_404_response_schema,
    get_quiz_response_schema,
    submit_quiz_response_schema,
    submit_quiz_request_schema,
    quiz_assignment_response_schema,
    quiz_assignment_request_schema,
    get_classroom_student_response_schema,
    get_section_data_response_schema,
    create_content_or_mindmap_request_schema,
    create_content_or_mindmap_response_schema,
    create_classroom_response_schema,
    get_classrooms_response_schema,
    get_classroom_details_response_schema,
    get_assessment_results_request_schema
)
from drf_yasg import openapi


EXAM_URL = 'http://localhost:3000/quiz/'

@api_view(['POST'])
def register(request):
    data = request.data
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    Profile.objects.create(user=user, role=data['role'])  
    return Response({"message": "User created successfully"})


@api_view(['POST'])
def login(request):
    data = request.data
    user = authenticate(username=data['username'], password=data['password'])
    if user is not None:
        # Return a token (JWT or session token) upon successful login
        return Response({"token": "your_generated_token_here"})
    else:
        return Response({"error": "Invalid credentials"}, status=400)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ClassRoomName': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the classroom", example="Math 101"),
            'Level': openapi.Schema(type=openapi.TYPE_STRING, description="Level of the classroom", example="Beginner"),
            'Disability': openapi.Schema(type=openapi.TYPE_STRING, description="Disability status", example="None"),
            'StudentEmail': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'Name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the student", example="John Doe"),
                        'Email': openapi.Schema(type=openapi.TYPE_STRING, description="Email of the student", example="johndoe@example.com")
                    }
                ),
                description="List of students"
            ),
            'Subject': openapi.Schema(type=openapi.TYPE_STRING, description="Subject of the classroom", example="Mathematics"),
            # 'Remark': openapi.Schema(type=openapi.TYPE_STRING, description="Remarks about the classroom", example="This is an introductory class"),
            'NumOfSections': openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of sections in the classroom", example=3)
        },
        required=['ClassRoomName', 'Level', 'Disability', 'StudentEmail', 'Subject', 'NumOfSections']
    ),
    responses={
        status.HTTP_201_CREATED: create_classroom_response_schema,
        status.HTTP_400_BAD_REQUEST: 'Invalid input'
    }
)
@api_view(['POST'])
def create_classroom_and_studyplan(request):
    teacher = User.objects.get(pk=1) # assuming defult teacher have id pk1
    # teacher = request.user
    # ['ClassRoomName', 'Level', 'Disability', 'StudentEmail', 'Subject', 'Remark', 'Period', 'NumOfSections']

    classroom = Classroom.objects.create(
        name = request.data['ClassRoomName'],
        subject=request.data['Subject'],
        level=request.data['Level'],
        disability=request.data['Disability'],
        extra = "",
        num_of_sections = request.data['NumOfSections'],
        teacher=teacher
    )
    sections = get_sections(request.data)

    for index, section in enumerate(sections, 1):
        title = section['Topic']
        description = section['Description']
        Section.objects.create(
            classroom=classroom,
            index = index,
            title=title,  
            description=description 
        )
    students = request.data['StudentEmail']
    for student in students:
        name = student['Name']
        email = student['Email']
        Student.objects.create(
            name = name,
            email = email,
            classroom = classroom
        )
    # students = request.data['StudentEmail']
    return Response({
        "message": "Classroom and sections has been created successfully",
        "classroom_id": classroom.id
    })



@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: get_classrooms_response_schema
    }
)
@api_view(['GET'])
def get_classrooms(request):
    # teacher = get_object_or_404(User, username=request.query_params.get('UserName'))
    classrooms = Classroom.objects.all() # we need to add this filter

    return Response({
        "ClassRoomName": [classroom.subject for classroom in classrooms],
        "ClassRoomId": [classroom.id for classroom in classrooms],
        "StudentNumbers": [classroom.students.count() for classroom in classrooms]
    })
    


@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: get_classroom_details_response_schema,
        status.HTTP_404_NOT_FOUND: 'Classroom not found'
    }
)
@api_view(['GET'])
def get_classroom_details(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    students = classroom.students.all()
    sections = Section.objects.filter(classroom_id = classroom_id).values('id', 'index', 'title', 'description')
    data = {
        "ClassRoomName": classroom.subject,
        "Level": classroom.level,
        "Disability": classroom.disability,
        "UserName": classroom.teacher.username,
        "Subject": classroom.subject,
        "students": [student.email for student in students],
        "sections": [
            {
                "SectionId": s['id'],
                "Index" : s['index'],
                "Title" : s['title'],
                "Description" : s['description']
            }
            for s in sections
        ],
    }
    
    return Response(data)



@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: get_classroom_student_response_schema,
        status.HTTP_404_NOT_FOUND: 'Classroom not found'
    }
)
@api_view(['GET'])
def get_classroom_student(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    students_data = []

    for student in classroom.students.all():
        students_data.append({
            "StudentId": student.id,
            "StudentName": student.username,
            "StudentEmail": student.email,
            "Weakness": student.profile.weakness
        })

    return Response(students_data)


@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: get_section_data_response_schema,
        status.HTTP_404_NOT_FOUND: 'Section not found'
    }
)
@api_view(['GET'])
def get_section_data(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    has_quiz = QuizAssignment.objects.filter(section=section, type='Quiz').exists()
    has_assignment = QuizAssignment.objects.filter(section=section, type='Assignment').exists()

    return Response({
        "SectionId": section.id,
        "SectionName": section.title,
        "HasQuiz": has_quiz,
        "HasAssignment": has_assignment,
        "ClassRoomId": section.classroom.pk
    })



@swagger_auto_schema(
    method='post',
    request_body=create_content_or_mindmap_request_schema,
    responses={
        status.HTTP_200_OK: create_content_or_mindmap_response_schema,
        status.HTTP_400_BAD_REQUEST: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message', example='Invalid content_type. Must be \'MindMap\', \'Content\', or \'PDF\'.')}),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message', example='MindMap generation failed.')}),
        status.HTTP_404_NOT_FOUND: 'Section not found'
    }
)
@api_view(['POST'])
def create_content_or_mindmap(request):
    # classroom_id = request.data.get('classroom_id')  
    section_id = request.data.get('SectionId')
    content_type = request.data.get('ContentType')
    alignment = request.data.get('alignment', 'right')  # Default to right alignment

    # if not classroom_id or not section_id or not content_type:
    #     return Response({"error": "'classroom_id', 'section_id', and 'content_type' are required"}, status=400)

    # classroom = get_object_or_404(Classroom, id=classroom_id)
    # , classroom=classroom
    section = get_object_or_404(Section, id=section_id)

    if content_type == 'MindMap':
        generator = MindMapGenerator(section.title)
        png_image = generator()
        try:
            return FileResponse(
                open(png_image, 'rb'),
                as_attachment=True,
                filename=f'mind_map_{section.title}.png',
                content_type='image/png'
            )
        except FileNotFoundError:
            return Response({"error": "MindMap generation failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif content_type == 'PowerPoint':
        generator = PowerPointGenerator(section.title, section.description)
        pptx_file = generator()
        try:
            return FileResponse(
                open(pptx_file, 'rb'),
                as_attachment=True,
                filename=f'mind_map_{section.title}.pptx',
                content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
            )
        except FileNotFoundError:
            return Response({"error": "Powerpoint generation failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif content_type == 'Content':
        prompt = f"Generate educational content for the section: {section.title}."
        generated_text = call_llm(prompt)
        Content.objects.create(section=section, content_type=content_type, generated_content=generated_text)
        return JsonResponse({"generated_content": generated_text}, json_dumps_params={'ensure_ascii': False})

    elif content_type == 'PDF':
         prompt = f"Generate educational content for the section: {section.title}."
         generated_text = call_llm(prompt)
         alignment = request.data.get('alignment', 'right')  # Default to right alignment
         pdf_file = generate_pdf_arabic(generated_text, section.title, alignment)

         response = HttpResponse(pdf_file, content_type='application/pdf')
         response['Content-Disposition'] = f'attachment; filename="content_{section.title}.pdf"'
         return response


    else:
        return Response({"error": "Invalid content_type. Must be 'MindMap', 'Content', or 'PDF'."}, status=400)

def generate_pdf_arabic(content, title, alignment='right'):
    buffer = io.BytesIO()

    # Create a PDF object
    p = canvas.Canvas(buffer, pagesize=A4)

    # Set up Arabic font
    pdfmetrics.registerFont(TTFont('Arabic', 'classroom/fonts/NotoSansArabic-VariableFont_wdth,wght.ttf'))
    p.setFont("Arabic", 14)

    # Reshape the Arabic content for proper display and handle right-to-left text
    reshaped_text = reshape(content)
    bidi_text = get_display(reshaped_text)

    # Define the text wrapping width (for a standard A4 page, with some padding)
    page_width, page_height = A4
    margin = 40
    text_width_limit = page_width - 2 * margin

    # Starting y-position (top of the page with some padding)
    y_position = page_height - 80

    # Split the content into lines
    lines = bidi_text.split('\n')

    # Function to wrap text manually
    def wrap_text(line, max_width):
        words = line.split(' ')
        wrapped_lines = []
        current_line = ""

        for word in words:
            if p.stringWidth(current_line + word, "Arabic", 14) < max_width:
                current_line += word + " "
            else:
                wrapped_lines.append(current_line.strip())
                current_line = word + " "
        
        wrapped_lines.append(current_line.strip())
        return wrapped_lines

    # Iterate over each line and wrap the text within the text width
    for line in lines:
        wrapped_lines = wrap_text(line, text_width_limit)  # Wrap the text manually
        for wrapped_line in wrapped_lines:
            if alignment == 'right':
                # Calculate the width of the text to align it to the right
                text_width_actual = p.stringWidth(wrapped_line, "Arabic", 14)
                x_position = page_width - margin - text_width_actual  # Align right
            else:
                x_position = margin  # Left alignment

            # Draw the text line
            p.drawString(x_position, y_position, wrapped_line)

            # Move to the next line (adjust y-position)
            y_position -= 20  # Line height

            # Stop if we exceed the page height
            if y_position < margin:
                p.showPage()
                y_position = page_height - 80

    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()

    return pdf


@swagger_auto_schema(
    method='post',
    request_body=quiz_assignment_request_schema,
    responses={
        status.HTTP_200_OK: quiz_assignment_response_schema,
        status.HTTP_400_BAD_REQUEST: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message', example='فشل في إنشاء الأسئلة.')}),
        status.HTTP_404_NOT_FOUND: 'Section not found'
    }
)
@api_view(['POST'])
def quiz_assignment(request):
    # classroom_id = request.data.get('ClassroomId')
    section = get_object_or_404(Section, id=request.data['SectionId'])
    quiz_name = request.data['QuizAssignmentName']
    num_questions = request.data.get('NumQuestions', 3)  # Default to 3 questions
    quiz_type = request.data['Type'].title()  # Either "Quiz" or "Assignment"

    # Create the quiz/assignment
    quiz_assignment = QuizAssignment.objects.create(
        section=section,
        type=quiz_type
    )

    # Call Allam (or another LLM service) to generate questions
    generated_questions = get_questions(
        section.title,
        section.description,
        num_questions
    )

    # Check if generated_questions is a list
    if not isinstance(generated_questions, list):
        return Response({"error": "فشل في إنشاء الأسئلة."}, status=400)

    # Parse and save generated questions
    for question_data in generated_questions:
        Question.objects.create(
            assessment=quiz_assignment,
            question_text=question_data.get('Q', ''),
            option_1=question_data.get('A1', ''),
            option_2=question_data.get('A2', ''),
            option_3=question_data.get('A3', ''),
            option_4=question_data.get('A4', ''),
            correct_answer=int(question_data.get('Correct', 1))  # Ensure correct_answer is an integer
        )

    # Create StudentAssessment records for each student and send unique quiz link
    students = section.classroom.students.all()
    for student in students:
        student_assessment = StudentAssessment.objects.create(
            student=student,
            quiz_assignment=quiz_assignment,
            uuid = str(uuid4())
        )
        unique_link = f"{EXAM_URL}{student_assessment.uuid}"  # Adjust for your domain

        # Send quiz link via email to each student
        send_quiz_link_to_students(student, quiz_assignment, unique_link)

    return Response({"message": f"تم إنشاء {quiz_type} مع {num_questions} سؤالًا لـ {quiz_name}"})

def send_quiz_link_to_students(student, quiz_assignment, unique_link):
    params = {
        "EXAM_OR_ASSIGNMENT": quiz_assignment.type,
        "STUDENT_NAME": student.name,
        "ASSESSMENT_URL": unique_link,
    }
    send_emails_in_background(student.email, params)

@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: get_quiz_response_schema,
        status.HTTP_404_NOT_FOUND: 'Quiz not found'
    }
)
@api_view(['GET'])
def get_quiz(request, quiz_uuid):
    quiz = get_object_or_404(StudentAssessment, uuid=str(quiz_uuid))
    questions = Question.objects.filter(assessment = quiz.quiz_assignment)
    # questions = quiz.questions.all()  # Assuming the relationship exists in your model
    serialized_questions = [
        {
            'id': q.id,
            'text': q.question_text,
            'options': [q.option_1, q.option_2, q.option_3, q.option_4]  # Assuming 4 options exist
        }
        for q in questions
    ]
    return Response({'questions': serialized_questions})


@swagger_auto_schema(
    method='post',
    request_body=submit_quiz_request_schema,
    responses={
        status.HTTP_200_OK: submit_quiz_response_schema,
        status.HTTP_404_NOT_FOUND: 'Quiz not found'
    }
)
@api_view(['POST'])
def submit_quiz(request, quiz_uuid):
    # student_id = request.data.get('student_id')  # Get student ID from request
    answers = request.data.get('answers')  # Expecting answers as a dictionary {question_id: selected_option}

    # Fetch the quiz assignment
    quiz = get_object_or_404(StudentAssessment, uuid=quiz_uuid)
    questions = Question.objects.filter(assessment = quiz.quiz_assignment)
    question_map = {str(q.pk) : q for q in questions}
    total_questions = len(question_map)
    correct_answer = 0 
    for answer_k in answers:
        is_correct = answers[answer_k] == question_map[answer_k].correct_answer
        StudentAnswer.objects.create(
            student_assessment = quiz,
            question = question_map[answer_k],
            selected_answer = answers[answer_k],
            is_correct = is_correct
        )
        correct_answer += is_correct
    quiz.marks = round(correct_answer / total_questions,3)
    quiz.save()
    return Response({"message": "Answers submitted successfully!"})


@swagger_auto_schema( 
    method='post', 
    request_body=get_assessment_results_request_schema,
    responses={
        status.HTTP_200_OK: get_assessment_results_response_schema,
        status.HTTP_404_NOT_FOUND: get_assessment_results_404_response_schema
    }
)
@api_view(['POST'])
def get_assessment_results(request):
    section_id = request.data.get('SectionId')
    assessment_type = request.data.get('AssessmentType').title()
    section = get_object_or_404(Section, id=section_id)
    classroom = section.classroom
    assessment = QuizAssignment.objects.filter(section_id = section_id, type = assessment_type).first()
    output = {
        "StudentsQuizMark": [
                {
                    "email": assessment.student.email,
                    "mark": assessment.marks
                }
                for assessment in StudentAssessment.objects.filter(quiz_assignment = assessment)
            ],
        "NumberOfSubmittedAssessment": StudentAssessment.objects.filter(quiz_assignment = assessment).count(),
        "NumberOfTotalStudents": Student.objects.filter(classroom = classroom).count(),
    }
    return Response(output)


@swagger_auto_schema(
    method='post',
    request_body=generate_support_content_request_schema,
    responses={
        status.HTTP_200_OK: generate_support_content_response_schema,
        status.HTTP_404_NOT_FOUND: generate_support_content_404_response_schema
    }
)
@api_view(['POST'])
def generate_and_send_support_content(request):
    # quiz_assignment_id = request.data.get('QuizAssignmentId')
    section_id = request.data.get('SectionId')
    assessment_type = request.data.get('AssessmentType').title()
    section = get_object_or_404(Section, id=section_id)
    quiz_assignment = QuizAssignment.objects.filter(section=section, type = assessment_type).first()
    # has_quiz = QuizAssignment.objects.filter(section=section, type='Quiz').exists()
    # has_assignment = QuizAssignment.objects.filter(section=section, type='Assignment').exists()

    # Get the quiz assignment
    # quiz_assignment = get_object_or_404(QuizAssignment, id=quiz_assignment_id)
    if not quiz_assignment:
        return Response({"message": f"No {assessment_type} for the following Section {section.title}"})
    assessments = StudentAssessment.objects.filter(quiz_assignment=quiz_assignment)

    for assessment in assessments:
        # Get the student's answers for this quiz assignment
        wrong_answers = StudentAnswer.objects.filter(student_assessment=assessment, is_correct=False)

        if not wrong_answers.exists():
            continue  # Skip students with no wrong answers

        # Prepare the prompt for generating support content
        support_prompt = f"<s> [INST] Generate educational content for the following {len(wrong_answers)} questions that the student answered incorrectly:\n"
        for i,  answer in enumerate(wrong_answers, 1):
            question = answer.question
            answers = [question.option_1, question.option_2, question.option_3, question.option_4]
            support_prompt += f"{i}- Question was {question.question_text} and the correct answer is : {answers[question.correct_answer]} but the student answered with: {answers[answer.selected_answer]}\n\n"
        support_prompt += " [/INST]"
        # Call the Allam API to generate support content based on the wrong answers
        support_content = call_llm(support_prompt)

        # Store the support content in the database
        SupportContent.objects.create(
            student=assessment.student,
            quiz_assignment=quiz_assignment,
            content=support_content
        )

        # Send the support content to the student via email
        send_email_to_student(assessment.student.name, assessment.student.email, support_content)

    return Response({"message": "Support content has been generated and emailed to students."})

def send_email_to_student(student_name, student_email, support_content):
    subject = "Your Personalized Support Content"
    message = f"Dear {student_name},\n\nHere is some personalized support content based on the questions you answered incorrectly:\n\n{support_content}\n\nBest regards,\nYour Professor"
    email_from = "alyaf3i1118@gmail.com"  # Add a valid email address here
    recipient_list = [student_email]

    send_mail(subject, message, email_from, recipient_list)


@swagger_auto_schema(
    method='post',
    request_body=add_student_request_schema,
    responses={
        status.HTTP_200_OK: add_student_response_schema,
        status.HTTP_404_NOT_FOUND: add_student_404_response_schema
    }
)
@api_view(['POST'])
def add_student(request):
    classroom = get_object_or_404(Classroom, id=request.data['classroom_id'])
    student = Student.objects.create(
        name=request.data['student_name'],
        email=request.data['student_email'],
        classroom=classroom
    )

    return Response({"message": "Student added to classroom", "student_id": student.id})

def send_emails_in_background(student_emails, content):
    thread = Thread(target=send_quiz_assignment, args=(student_emails, content))
    thread.start()
