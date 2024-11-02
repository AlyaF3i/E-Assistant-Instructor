from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from email.mime.image import MIMEImage
import os
from pathlib import Path

def send_quiz_assignment(email: str, params: dict = {}):
    subject = f"{params['EXAM_OR_ASSIGNMENT']} لطالب {params['STUDENT_NAME']}"
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]  # Ensure that email is passed as a list

    # Load the HTML content from the file
    template_path = settings.BASE_DIR / 'templates' / 'images' / 'index.html'
    with open(template_path, 'r', encoding='UTF-8') as fp:
        html_content = fp.read()
        for key, value in params.items():
            html_content = html_content.replace(f"%%{key.upper()}%%", value)

    # Create a plain-text version of the HTML email (if needed)
    text_content = strip_tags(html_content)

    # Create the email message object
    email_msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)  # Pass `to_email` as a list

    # Attach the HTML version
    email_msg.attach_alternative(html_content, "text/html")

    # Define the path to images and attach them with a Content-ID
    images_root_path = settings.BASE_DIR / 'templates' / 'images'
    image_paths = [os.path.join(images_root_path, img) for img in os.listdir(images_root_path) if not img.endswith(".html")]

    # Attach images with CID for embedding in the email body
    for img_index, image_path in enumerate(image_paths, 1):
        with open(image_path, 'rb') as img_file:
            mime_image = MIMEImage(img_file.read())
            image_name = Path(image_path).name
            cid = f'image{img_index}'  # Generate a Content-ID like 'image1', 'image2', etc.
            mime_image.add_header('Content-ID', f'<{cid}>')  # Add CID for referencing in HTML
            mime_image.add_header('Content-Disposition', 'inline', filename=image_name)  # Inline attachment
            email_msg.attach(mime_image)

    # Send the email
    email_msg.send()
