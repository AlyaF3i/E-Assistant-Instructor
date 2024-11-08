# Function to get Watsonx credentials
import requests
import os
from requests.exceptions import RequestException
import re
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from duckduckgo_search import DDGS, AsyncDDGS
import asyncio

class ArabicTextToDict:
    def __init__(self):
        self.llm = ChatOllama(model='llama3', format="json", temperature=0)
        self.prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert in text processing.
            You will be given an Arabic text and an example dictionary format.
            Your task is to convert the Arabic text into a JSON object following the provided dictionary structure.
            The result should have the same structure as the example dictionary, and should adhere to the extra notes if exists
            Only return the JSON object and no explanations.\n
            Here is the text: {content}\n
            Example dictionary: {example_dict}
            Extra Notes: {extra_notes} \n<|eot_id|><|start_header_id|>assistant<|end_header_id|>
            """,
            input_variables=["content", "example_dict", "extra_notes"],
        )

        self.agent = self.prompt | self.llm | JsonOutputParser()

    def __call__(self, arabic_text, example_dict, extra_notes = "No Extra Notes"):
        output = self.agent.invoke(
            {"content": arabic_text, "example_dict": example_dict, "extra_notes": extra_notes}
        )
        return output

PROJECT_ID = os.getenv('PROJECT_ID')
MODEL_NAME = 'sdaia/allam-1-13b-instruct'
API_KEY = os.getenv('WATSON_API_KEY', 'O1ZRniRDHlcM3d-xg9Fxb_lQeE4EAfKTN6hZWmY7n6Q4')
def get_watsonx_credentials():
    return {
        "url": "https://eu-de.ml.cloud.ibm.com",
        "apikey": os.getenv('API_KEY')  # Replace with your IBM Watsonx API key
    }


def get_access_token(api_key = API_KEY):
    token_url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    
    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]
    except RequestException as e:
        print(f"Error obtaining access token: {str(e)}")
        return None
def call_llm(prompt, max_new_tokens=900, temperature: float = 0.7):
    url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

    body = {
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": max_new_tokens,
            "repetition_penalty": 1,
            "temperature" : temperature
        },
        "model_id": "sdaia/allam-1-13b-instruct",
        "project_id": "11a9f435-324b-4654-a317-348fbf26c592"
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_access_token()}"
    }

    try:
        # Make the request to the LLM API
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        # print(f"LLM Response Data: {data}")  # Log the response data
        
        # Return the generated text
        return data['results'][0]['generated_text'].strip()
    
    except RequestException as e:
        print(f"Error calling LLM: {str(e)}")
        return None

def read_txt(grade_level, subject, base_path="educational_resources"):
    """
    Generate path from grade level and subject, then read and return PDF content.
    
    Args:
        grade_level (str): The grade level (e.g., "grade1", "grade2")
        subject (str): The subject name (e.g., "math", "science")
        base_path (str): Base directory for educational resources (default: "educational_resources")
    
    Returns:
        str: Extracted text from the PDF or error message
    """
    try:
        # Clean and standardize inputs
        grade_level = str(grade_level).lower().strip()
        subject = subject.lower().strip()
        
        # Generate file path
        file_name = f"{subject}.txt"
        file_path = os.path.join(base_path, grade_level, file_name)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return f"TXT file not found at: {file_path}"
        grade_number = int(grade_level.replace("grade", ''))
        with open(file_path, 'r') as fp:
            topics = [f"الصف {grade_number} الصف {a.stirp(' .')}" for a in fp.readlines() if a.strip(' .')]
        
        return topics
    
    except Exception as e:
        return f"Error processing txt: {str(e)}"

async def search_topic_async(search_engine, topic):
    # Perform the search asynchronously using AsyncDDGS
    results = await search_engine.atext(topic, max_results=2, region='xa-ar')
    return f"{topic} " + " ".join([res['body'] + " " for res in results])


async def search_web(topics):
    output = list()
    search_engine = AsyncDDGS()
    tasks = [search_topic_async(search_engine, topic) for topic in topics]
    results = await asyncio.gather(*tasks)
    output.extend(results)
    return output
 
def get_sections(data: dict) -> list[dict]:
    level = data['Level']
    if data['Disability'].lower() == 'no':
        disability_prompt = ''
    else:
        disability_prompt = f" الذين لديهم صعوبة بالتعلم"
    subject = data['Subject']
    num_of_sections = data['NumOfSections']
    # details = data['Remark']
    topics = read_txt(level, subject)
    loop = asyncio.get_event_loop()
    details = loop.run_until_complete(search_web(topics))
    content = '\n'.join(details)
    prompt = f"<s> [INST] {content}بأستخدام الدروس الذي سبقت قم بإنشاء {num_of_sections} أقسام تعليمية مع شرح تفصيلي لكل قسم متعلقة بموضوع {subject} لطلاب {level}{disability_prompt}.[/INST]"
    resp = call_llm(prompt, temperature = 0.2)
    
    
    example_dict = {
            "data" : [
                {
                    "Topic": "<topic 1>",
                    "Description": "<description 1>"
                },
                {
                    "Topic": "<topic 2>",
                    "Description": "<description 2>"
                }
            ]
        }
    arabic_processor = ArabicTextToDict()

    output_dict = arabic_processor(resp, example_dict, f"The number of items inside the data list should be {num_of_sections}")
    print(output_dict)
    return output_dict['data']
    

        
""" RESPONSE OUTPUT
{'model_id': 'sdaia/allam-1-13b-instruct',
 'created_at': '2024-09-15T13:46:15.041Z',
 'results': [{'generated_text': ' Title: Exploring the Wonders of Mathematics: A Comprehensive Guide for Students and Learners\n\nIntroduction:\nMathematics is a fundamental subject that plays a crucial role in our daily lives, from simple calculations to complex problem-solving. It is the language of science, technology, engineering, and finance, among many other fields. In this educational content, we will dive into various aspects of mathematics, from basic arithmetic to advanced topics, to help students and learners develop a strong foundation and appreciation for this fascinating subject.\n\n1. Arithmetic Fundamentals:\n   a. Whole Numbers\n   b. Integers\n   c. Fractions, Decimals, and Percentages\n   d. Operations: Addition, Subtraction, Multiplication, and Division\n   e. Order of Operations (PEMDAS/BODMAS)\n\n2. Algebra:\n   a. Variables and Expressions\n   b. Equations and Inequalities\n   c. Linear and Quadratic Functions\n   d. Polynomials\n   e. Factoring and Solving Equations\n\n3. Geometry:\n   a. Points, Lines, and Angles\n   b. Triangles, Quadrilaterals, and Polygons\n   c. Circles and Spheres\n   d. Area and Volume\n   e. Coordinate Geometry\n\n4. Trigonometry:\n   a. Trigonometric Functions (Sine, Cosine, Tangent)\n   b. Right Triangles and Pythagorean Theorem\n   c. Trigonometric Identities\n   d. Applications of Trigonometry (e.g., navigation, physics)\n\n5. Calculus:\n   a. Limits and Continuity\n   b. Derivatives and Rates of Change\n   c. Applications of Derivatives (e.g., optimization, motion)\n   d. Integrals and Area Under Curves\n   e. The Fundamental Theorem of Calculus\n\n6. Probability and Statistics:\n   a. Probability Concepts\n   b. Random Variables and Expectations\n   c. Discrete and Continuous Probability Distributions\n   d. Central Limit Theorem\n   e. Inferential Statistics and Hypothesis Testing\n\n7. Advanced Topics:\n   a. Number Theory\n   b. Combinatorics\n   c. Linear Algebra\n   d. Differential Equations\n   e. Game Theory\n\nConclusion:\nMathematics is a vast and fascinating subject that offers numerous opportunities for growth and understanding. By exploring the topics outlined above, students and learners can develop a strong foundation in mathematics, which will not only help them excel in their academic pursuits but also enable them to tackle real-world problems with confidence and precision. Remember, practice is key to mastering mathematics, so keep challenging yourself and enjoy the journey of discovery! ',
   'generated_token_count': 671,
   'input_token_count': 18,
   'stop_reason': 'eos_token'}],
 'system': {'warnings': [{'message': 'This model is a Non-IBM Product governed by a third-party license that may impose use restrictions and other obligations. By using this model you agree to its terms as identified in the following URL.',
    'id': 'disclaimer_warning',
    'more_info': 'https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models.html?context=wx'}]}}
"""

def get_questions(title: str, description: str, num_questions: int = 5):
    prompt = (
        f"<s> [INST] قم بإنشاء {num_questions} أسئلة بناءً على القسم التالي:\n"
        f"العنوان: {title}\n"
        f"الوصف: {description}\n"
        "يرجى إنشاء الأسئلة بحيث تكون لكل سؤال أربعة اختيارات والجواب الصحيح مع ذكره. [/INST]"
    )
    text = call_llm(prompt, temperature=0)
    example_dict = {
            "data" : [
                {
                    "Q" : "<question 1>",
                    "A1" : "<option_1>",
                    "A2" : "<option_2>",
                    "A3" : "<option_3>",
                    "A4" : "<option_4>",
                    "Correct" : "<answer_index>"
                },
                {
                    "Q" : "<question 2>",
                    "A1" : "<option_1>",
                    "A2" : "<option_2>",
                    "A3" : "<option_3>",
                    "A4" : "<option_4>",
                    "Correct" : "<answer_index>"
                },
            ]
        }
    arabic_processor = ArabicTextToDict()

    output_dict = arabic_processor(text, example_dict, f"The number of items inside the data list should be {num_questions}, and the <answer_index> should be either 0,1,2,3 depending on which answer is the correct answer, Also make sure all of the options are not empty in case any are empty you can make up one")
    return output_dict['data']