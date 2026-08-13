from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def attach_reference_file(msg, reference):
    if not reference:
        return
    try:
        if hasattr(reference, 'path'):
            try:
                msg.attach_file(reference.path)
                return
            except (NotImplementedError, AttributeError, ValueError):
                pass
        if hasattr(reference, 'read'):
            if hasattr(reference, 'seek'):
                reference.seek(0)
            content = reference.read()
            filename = getattr(reference, 'name', 'attachment')
            content_type = getattr(reference, 'content_type', None)
            msg.attach(filename, content, content_type)
    except Exception as e:
        print(f"Error attaching reference file: {e}")


def contact_us_notification_mail(name, contact, idea, subject, reference):
    email_subject = f"New Contact Us Submission: {subject}"
    to_email = settings.EMAIL_HOST_USER
    from_email = settings.DEFAULT_FROM_EMAIL
    ref_name = getattr(reference, 'name', str(reference)) if reference else 'None'
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Contact Us Submission</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #f5f5f5;
                padding: 20px;
                text-align: center;
            }}
            .content {{
                padding: 20px;
            }}
            .footer {{
                background-color: #f5f5f5;
                padding: 20px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>New Contact Us Submission</h1>
            </div>
            <div class="content">
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Contact:</strong> {contact}</p>
                <p><strong>Idea:</strong> {idea}</p>
                <p><strong>Subject:</strong> {subject}</p>
                <p><strong>Reference:</strong> {ref_name}</p>
            </div>
            <div class="footer">
                <p>This is an automated email. Please do not reply.</p>
            </div>
        </div>
    </body>
    </html>
    """
    msg = EmailMultiAlternatives(
        email_subject,
        html_content,
        from_email,
        [to_email],
    )
    msg.content_subtype = "html"
    attach_reference_file(msg, reference)
    msg.send()
    
# the contact is an email
def contact_replay_mail(name, contact, idea, subject, reference):
    email_subject = f"Thank you for contacting us: {subject}"
    to_email = contact
    from_email = settings.DEFAULT_FROM_EMAIL
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Thank You for Contacting Us</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .header {{
                background-color: #2c3e50;
                color: #ffffff;
                padding: 25px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                padding: 30px;
                color: #333333;
                line-height: 1.6;
            }}
            .footer {{
                background-color: #f5f5f5;
                padding: 20px;
                text-align: center;
                color: #777777;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Thank You for Contacting Us</h1>
            </div>
            <div class="content">
                <p>Hello <strong>{name}</strong>,</p>
                <p>Thank you for reaching out to us regarding <strong>"{subject}"</strong>.</p>
                <p>We have received your request and our team will connect with you shortly.</p>
                <p>Thank you!</p>
            </div>
            <div class="footer">
                <p>This is an automated confirmation email. Please do not reply directly to this message.</p>
            </div>
        </div>
    </body>
    </html>
    """
    msg = EmailMultiAlternatives(
        email_subject,
        html_content,
        from_email,
        [to_email],
    )
    msg.content_subtype = "html"
    attach_reference_file(msg, reference)
    msg.send()

def get_career_enquiry_mail(name, contact, job_profile, education, skills, resume):
    email_subject = f"New Career Enquiry: {job_profile} - {name}"
    to_email = settings.EMAIL_HOST_USER
    from_email = settings.DEFAULT_FROM_EMAIL
    resume_name = getattr(resume, 'name', str(resume)) if resume else 'None'
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Career Enquiry</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #f5f5f5;
                padding: 20px;
                text-align: center;
            }}
            .content {{
                padding: 20px;
            }}
            .footer {{
                background-color: #f5f5f5;
                padding: 20px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>New Career Enquiry</h1>
            </div>
            <div class="content">
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Contact:</strong> {contact}</p>
                <p><strong>Job Profile:</strong> {job_profile}</p>
                <p><strong>Education:</strong> {education}</p>
                <p><strong>Skills:</strong> {skills}</p>
                <p><strong>Resume:</strong> {resume_name}</p>
            </div>
            <div class="footer">
                <p>This is an automated email. Please do not reply.</p>
            </div>
        </div>
    </body>
    </html>
    """
    msg = EmailMultiAlternatives(
        email_subject,
        html_content,
        from_email,
        [to_email],
    )
    msg.content_subtype = "html"
    attach_reference_file(msg, resume)
    msg.send()


def career_replay_mail(name, contact, job_profile, education, skills, resume):
    email_subject = f"Thank you for applying: {job_profile}"
    to_email = contact
    from_email = settings.DEFAULT_FROM_EMAIL
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Application Received</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .header {{
                background-color: #2c3e50;
                color: #ffffff;
                padding: 25px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                padding: 30px;
                color: #333333;
                line-height: 1.6;
            }}
            .footer {{
                background-color: #f5f5f5;
                padding: 20px;
                text-align: center;
                color: #777777;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Thank You for Applying</h1>
            </div>
            <div class="content">
                <p>Hello <strong>{name}</strong>,</p>
                <p>Thank you for submitting your application for the <strong>"{job_profile}"</strong> position.</p>
                <p>We have received your application and resume. Our recruitment team will review your profile and connect with you shortly.</p>
                <p>Thank you!</p>
            </div>
            <div class="footer">
                <p>This is an automated confirmation email. Please do not reply directly to this message.</p>
            </div>
        </div>
    </body>
    </html>
    """
    msg = EmailMultiAlternatives(
        email_subject,
        html_content,
        from_email,
        [to_email],
    )
    msg.content_subtype = "html"
    attach_reference_file(msg, resume)
    msg.send()