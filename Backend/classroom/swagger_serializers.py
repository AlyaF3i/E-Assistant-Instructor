from drf_yasg import openapi

add_student_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'classroom_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the classroom', example=1),
        'student_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the student', example='John Doe'),
        'student_email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email of the student', example='johndoe@example.com')
    },
    required=['classroom_id', 'student_name', 'student_email']
)

# 200 OK response schema
add_student_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message', example='Student added to classroom'),
        'student_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the added student', example=101)
    }
)

# 404 Not Found response schema
add_student_404_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message', example='Not found.')
    }
)




generate_support_content_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'SectionId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the section', example=1),
        'AssessmentType': openapi.Schema(type=openapi.TYPE_STRING, description='Type of assessment (e.g., Quiz or Assignment)', example='Quiz')
    },
    required=['SectionId', 'AssessmentType']
)

# 200 OK response schema
generate_support_content_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message', example='Support content has been generated and emailed to students.')
    }
)

# 404 Not Found response schema
generate_support_content_404_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message if no assignment found for the section', example='No Quiz for the following Section Algebra')
    }
)


# 200 OK response schema
get_assessment_results_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'StudentsAssignmentMark': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="Student's email", example="johndoe@example.com"),
                    'mark': openapi.Schema(type=openapi.TYPE_INTEGER, description="Student's mark for the assignment", example=85)
                }
            ),
            description="List of students' assignment marks"
        ),
        'StudentsQuizMark': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="Student's email", example="janedoe@example.com"),
                    'mark': openapi.Schema(type=openapi.TYPE_INTEGER, description="Student's mark for the quiz", example=90)
                }
            ),
            description="List of students' quiz marks"
        ),
        'NumberOfSubmittedAssessment': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="Total number of students who submitted the assessment",
            example=25
        ),
        'NumberOfTotalStudents': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="Total number of students in the classroom",
            example=30
        ),
    }
)

# 404 Not Found response schema
get_assessment_results_404_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message if section or assessment is not found', example='Not found.')
    }
)



submit_quiz_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'answers': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            additional_properties=openapi.Schema(type=openapi.TYPE_INTEGER, description="Selected option index", example=2),
            description="Dictionary of answers with question IDs as keys and selected option indexes as values"
        )
    },
    required=['answers']
)

submit_quiz_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message', example='Answers submitted successfully!')
    }
)




get_quiz_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'questions': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Question ID", example=101),
                    'text': openapi.Schema(type=openapi.TYPE_STRING, description="Question text", example="What is 2 + 2?"),
                    'options': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                        description="Answer options",
                        example=["2", "3", "4", "5"]
                    )
                }
            ),
            description="List of questions in the quiz"
        )
    }
)


quiz_assignment_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'SectionId': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the section", example=1),
        'QuizAssignmentName': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the quiz/assignment", example="Math Quiz"),
        'NumQuestions': openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of questions to generate", example=5),
        'Type': openapi.Schema(type=openapi.TYPE_STRING, description="Type of assessment (Quiz/Assignment)", example="Quiz")
    },
    required=['SectionId', 'QuizAssignmentName', 'Type']
)

# Response schema for quiz_assignment
quiz_assignment_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message', example='تم إنشاء Quiz مع 5 سؤالًا لـ Math Quiz')
    }
)



get_classroom_student_response_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'StudentId': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the student", example=1),
            'StudentName': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the student", example="John Doe"),
            'StudentEmail': openapi.Schema(type=openapi.TYPE_STRING, description="Email of the student", example="john.doe@example.com"),
            'Weakness': openapi.Schema(type=openapi.TYPE_STRING, description="Weakness of the student", example="Math")
        }
    )
)

get_section_data_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'SectionId': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the section", example=1),
        'SectionName': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the section", example="Mathematics"),
        'HasQuiz': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indicates if a quiz exists for this section", example=True),
        'HasAssignment': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indicates if an assignment exists for this section", example=False),
        'ClassRoomId': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the associated classroom", example=2)
    }
)

create_content_or_mindmap_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'SectionId': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the section", example=1),
        'ContentType': openapi.Schema(type=openapi.TYPE_STRING, description="Type of content to create", example="MindMap"),
        'alignment': openapi.Schema(type=openapi.TYPE_STRING, description="Alignment for PDF content", example="right")
    },
    required=['SectionId', 'ContentType']
)

# Response schema for create_content_or_mindmap
create_content_or_mindmap_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'generated_content': openapi.Schema(type=openapi.TYPE_STRING, description='Generated content', example='This is the educational content for the section.')
    }
)


create_classroom_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, description="Success message", example="Classroom and sections have been created successfully."),
        'classroom_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the created classroom", example=1)
    }
)

get_classrooms_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'ClassRoomName': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="List of classroom names"),
        'ClassRoomId': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER), description="List of classroom IDs"),
        'StudentNumbers': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER), description="Number of students in each classroom")
    }
)

get_classroom_details_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'ClassRoomName': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the classroom", example="Math 101"),
        'Level': openapi.Schema(type=openapi.TYPE_STRING, description="Level of the classroom", example="Beginner"),
        'Disability': openapi.Schema(type=openapi.TYPE_STRING, description="Disability status", example="None"),
        'UserName': openapi.Schema(type=openapi.TYPE_STRING, description="Username of the teacher", example="teacher_username"),
        'Subject': openapi.Schema(type=openapi.TYPE_STRING, description="Subject taught in the classroom", example="Mathematics"),
        'students': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="List of student emails"),
        'sections': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'SectionId': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the section", example=1),
                    'Index': openapi.Schema(type=openapi.TYPE_INTEGER, description="Index of the section", example=1),
                    'Title': openapi.Schema(type=openapi.TYPE_STRING, description="Title of the section", example="Algebra"),
                    'Description': openapi.Schema(type=openapi.TYPE_STRING, description="Description of the section", example="Introduction to Algebra")
                }
            ),
            description="List of sections in the classroom"
        )
    }
)


get_assessment_results_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'SectionId': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="The ID of the section"
        ),
        'AssessmentType': openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Either Quiz or Assignment"
        )
    },
    required=['SectionId', 'AssessmentType']
)