from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task
import os


@shared_task
def attach_reference_file(msg, reference):
    if not reference:
        return
    try:
        if isinstance(reference, str):
            if os.path.exists(reference):
                msg.attach_file(reference)
            return

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


@shared_task
def contact_us_notification_mail(name, contact, idea, subject, reference):
    email_subject = f"New Contact Us Submission: {subject}"
    to_email = settings.EMAIL_HOST_USER
    from_email = settings.DEFAULT_FROM_EMAIL
    ref_name = os.path.basename(reference) if isinstance(reference, str) else getattr(reference, 'name', str(reference)) if reference else 'None'
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Contact Us Submission</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f3f4f6; font-family:Arial, Helvetica, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f3f4f6; padding:40px 15px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px; width:100%; background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08);">
                        <tr>
                            <td style="background:#1e3a8a; padding:30px 35px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td>
                                            <div style="display:inline-block; background:#3b82f6; color:#ffffff; font-size:12px; font-weight:bold; padding:6px 12px; border-radius:20px; margin-bottom:12px;">CONTACT ENQUIRY</div>
                                            <h1 style="margin:0; color:#ffffff; font-size:26px; line-height:1.3;">New Contact Us Submission</h1>
                                            <p style="margin:8px 0 0; color:#93c5fd; font-size:14px;">A new contact message has been received.</p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:35px;">
                                <h2 style="margin:0 0 20px; color:#111827; font-size:18px;">Submission Details</h2>
                                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                    <tr>
                                        <td style="padding:14px 0; border-bottom:1px solid #e5e7eb;">
                                            <div style="color:#6b7280; font-size:12px; margin-bottom:5px; text-transform:uppercase; letter-spacing:0.5px;">Name</div>
                                            <div style="color:#111827; font-size:15px; font-weight:600;">{name}</div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding:14px 0; border-bottom:1px solid #e5e7eb;">
                                            <div style="color:#6b7280; font-size:12px; margin-bottom:5px; text-transform:uppercase; letter-spacing:0.5px;">Contact</div>
                                            <div style="color:#111827; font-size:15px; font-weight:600;">{contact}</div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding:14px 0; border-bottom:1px solid #e5e7eb;">
                                            <div style="color:#6b7280; font-size:12px; margin-bottom:5px; text-transform:uppercase; letter-spacing:0.5px;">Subject</div>
                                            <div style="color:#111827; font-size:15px; font-weight:600;">{subject}</div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding:14px 0;">
                                            <div style="color:#6b7280; font-size:12px; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.5px;">Idea / Message</div>
                                            <div style="color:#374151; font-size:14px; line-height:1.6;">{idea}</div>
                                        </td>
                                    </tr>
                                </table>
                                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:25px; background:#eff6ff; border:1px solid #bfdbfe; border-radius:10px;">
                                    <tr>
                                        <td style="padding:18px 20px;">
                                            <table width="100%" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td width="45">
                                                        <div style="width:38px; height:38px; line-height:38px; text-align:center; background:#3b82f6; color:#ffffff; border-radius:8px; font-size:18px;">📎</div>
                                                    </td>
                                                    <td style="padding-left:12px;">
                                                        <div style="color:#6b7280; font-size:12px; margin-bottom:4px;">REFERENCE FILE</div>
                                                        <div style="color:#1e3a8a; font-size:14px; font-weight:bold; word-break:break-word;">{ref_name}</div>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style="background:#f9fafb; border-top:1px solid #e5e7eb; padding:22px 35px; text-align:center;">
                                <p style="margin:0; color:#6b7280; font-size:12px; line-height:1.6;">This is an automated notification from the Contact System.</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
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
    
@shared_task
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
    </head>
    <body style="margin:0; padding:0; background-color:#f3f4f6; font-family:Arial, Helvetica, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f3f4f6; padding:40px 15px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px; width:100%; background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08);">
                        <tr>
                            <td style="background:#0f766e; padding:30px 35px; text-align:center;">
                                <div style="display:inline-block; background:#14b8a6; color:#ffffff; font-size:12px; font-weight:bold; padding:6px 12px; border-radius:20px; margin-bottom:12px;">REQUEST RECEIVED</div>
                                <h1 style="margin:0; color:#ffffff; font-size:26px; line-height:1.3;">Thank You for Contacting Us</h1>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:35px; color:#374151; font-size:15px; line-height:1.6;">
                                <p style="margin:0 0 15px;">Hello <strong style="color:#111827;">{name}</strong>,</p>
                                <p style="margin:0 0 15px;">Thank you for reaching out to us regarding <strong style="color:#111827;">"{subject}"</strong>.</p>
                                <p style="margin:0 0 15px;">We have successfully received your request and our team is currently reviewing it. We will connect with you shortly with a response.</p>
                                <p style="margin:0;">Best Regards,<br><strong>Our Team</strong></p>
                            </td>
                        </tr>
                        <tr>
                            <td style="background:#f9fafb; border-top:1px solid #e5e7eb; padding:22px 35px; text-align:center;">
                                <p style="margin:0; color:#6b7280; font-size:12px; line-height:1.6;">This is an automated confirmation email. Please do not reply directly to this message.</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
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

@shared_task
def get_career_enquiry_mail(name, contact, job_profile, education, skills, resume):
    email_subject = f"New Career Enquiry: {job_profile} - {name}"
    to_email = settings.EMAIL_HOST_USER
    from_email = settings.DEFAULT_FROM_EMAIL
    resume_name = os.path.basename(resume) if isinstance(resume, str) else getattr(resume, 'name', str(resume)) if resume else 'None'
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Career Enquiry</title>
    </head>
    
    <body style="margin:0; padding:0; background-color:#f3f4f6; font-family:Arial, Helvetica, sans-serif;">
    
        <table width="100%" cellpadding="0" cellspacing="0" border="0"
               style="background-color:#f3f4f6; padding:40px 15px;">
            <tr>
                <td align="center">
    
                    <!-- Main Card -->
                    <table width="600" cellpadding="0" cellspacing="0" border="0"
                           style="max-width:600px; width:100%; background:#ffffff;
                                  border-radius:12px; overflow:hidden;
                                  box-shadow:0 4px 20px rgba(0,0,0,0.08);">
    
                        <!-- Header -->
                        <tr>
                            <td style="background:#111827; padding:30px 35px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td>
                                            <div style="
                                                display:inline-block;
                                                background:#6366f1;
                                                color:#ffffff;
                                                font-size:12px;
                                                font-weight:bold;
                                                padding:6px 12px;
                                                border-radius:20px;
                                                margin-bottom:12px;
                                            ">
                                                CAREER ENQUIRY
                                            </div>
    
                                            <h1 style="
                                                margin:0;
                                                color:#ffffff;
                                                font-size:26px;
                                                line-height:1.3;
                                            ">
                                                New Career Enquiry
                                            </h1>
    
                                            <p style="
                                                margin:8px 0 0;
                                                color:#9ca3af;
                                                font-size:14px;
                                            ">
                                                A new candidate has submitted a career enquiry.
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
    
                        <!-- Content -->
                        <tr>
                            <td style="padding:35px;">
    
                                <!-- Candidate Information -->
                                <h2 style="
                                    margin:0 0 20px;
                                    color:#111827;
                                    font-size:18px;
                                ">
                                    Candidate Information
                                </h2>
    
                                <table width="100%" cellpadding="0" cellspacing="0" border="0">
    
                                    <!-- Name -->
                                    <tr>
                                        <td style="
                                            padding:14px 0;
                                            border-bottom:1px solid #e5e7eb;
                                        ">
                                            <div style="
                                                color:#6b7280;
                                                font-size:12px;
                                                margin-bottom:5px;
                                                text-transform:uppercase;
                                                letter-spacing:0.5px;
                                            ">
                                                Name
                                            </div>
    
                                            <div style="
                                                color:#111827;
                                                font-size:15px;
                                                font-weight:600;
                                            ">
                                                {name}
                                            </div>
                                        </td>
                                    </tr>
    
                                    <!-- Contact -->
                                    <tr>
                                        <td style="
                                            padding:14px 0;
                                            border-bottom:1px solid #e5e7eb;
                                        ">
                                            <div style="
                                                color:#6b7280;
                                                font-size:12px;
                                                margin-bottom:5px;
                                                text-transform:uppercase;
                                                letter-spacing:0.5px;
                                            ">
                                                Contact
                                            </div>
    
                                            <div style="
                                                color:#111827;
                                                font-size:15px;
                                                font-weight:600;
                                            ">
                                                {contact}
                                            </div>
                                        </td>
                                    </tr>
    
                                    <!-- Job Profile -->
                                    <tr>
                                        <td style="
                                            padding:14px 0;
                                            border-bottom:1px solid #e5e7eb;
                                        ">
                                            <div style="
                                                color:#6b7280;
                                                font-size:12px;
                                                margin-bottom:5px;
                                                text-transform:uppercase;
                                                letter-spacing:0.5px;
                                            ">
                                                Job Profile
                                            </div>
    
                                            <div style="
                                                color:#111827;
                                                font-size:15px;
                                                font-weight:600;
                                            ">
                                                {job_profile}
                                            </div>
                                        </td>
                                    </tr>
    
                                    <!-- Education -->
                                    <tr>
                                        <td style="
                                            padding:14px 0;
                                            border-bottom:1px solid #e5e7eb;
                                        ">
                                            <div style="
                                                color:#6b7280;
                                                font-size:12px;
                                                margin-bottom:5px;
                                                text-transform:uppercase;
                                                letter-spacing:0.5px;
                                            ">
                                                Education
                                            </div>
    
                                            <div style="
                                                color:#111827;
                                                font-size:15px;
                                                font-weight:600;
                                            ">
                                                {education}
                                            </div>
                                        </td>
                                    </tr>
    
                                    <!-- Skills -->
                                    <tr>
                                        <td style="padding:14px 0;">
                                            <div style="
                                                color:#6b7280;
                                                font-size:12px;
                                                margin-bottom:8px;
                                                text-transform:uppercase;
                                                letter-spacing:0.5px;
                                            ">
                                                Skills
                                            </div>
    
                                            <div style="
                                                color:#374151;
                                                font-size:14px;
                                                line-height:1.6;
                                            ">
                                                {skills}
                                            </div>
                                        </td>
                                    </tr>
    
                                </table>
    
                                <!-- Resume Box -->
                                <table width="100%" cellpadding="0" cellspacing="0" border="0"
                                       style="
                                           margin-top:25px;
                                           background:#f5f3ff;
                                           border:1px solid #ddd6fe;
                                           border-radius:10px;
                                       ">
                                    <tr>
                                        <td style="padding:18px 20px;">
    
                                            <table width="100%" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td width="45">
                                                        <div style="
                                                            width:38px;
                                                            height:38px;
                                                            line-height:38px;
                                                            text-align:center;
                                                            background:#6366f1;
                                                            color:#ffffff;
                                                            border-radius:8px;
                                                            font-size:18px;
                                                        ">
                                                            📄
                                                        </div>
                                                    </td>
    
                                                    <td style="padding-left:12px;">
                                                        <div style="
                                                            color:#6b7280;
                                                            font-size:12px;
                                                            margin-bottom:4px;
                                                        ">
                                                            RESUME
                                                        </div>
    
                                                        <div style="
                                                            color:#312e81;
                                                            font-size:14px;
                                                            font-weight:bold;
                                                            word-break:break-word;
                                                        ">
                                                            {resume_name}
                                                        </div>
                                                    </td>
                                                </tr>
                                            </table>
    
                                        </td>
                                    </tr>
                                </table>
    
                            </td>
                        </tr>
    
                        <!-- Footer -->
                        <tr>
                            <td style="
                                background:#f9fafb;
                                border-top:1px solid #e5e7eb;
                                padding:22px 35px;
                                text-align:center;
                            ">
    
                                <p style="
                                    margin:0;
                                    color:#6b7280;
                                    font-size:12px;
                                    line-height:1.6;
                                ">
                                    This is an automated notification from the
                                    Career Enquiry System.
                                </p>
    
                                <p style="
                                    margin:6px 0 0;
                                    color:#9ca3af;
                                    font-size:11px;
                                ">
                                    Please review the candidate details and attached resume.
                                </p>
    
                            </td>
                        </tr>
    
                    </table>
    
                </td>
            </tr>
        </table>
    
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

@shared_task
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
    </head>
    <body style="margin:0; padding:0; background-color:#f3f4f6; font-family:Arial, Helvetica, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f3f4f6; padding:40px 15px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px; width:100%; background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08);">
                        <tr>
                            <td style="background:#065f46; padding:30px 35px; text-align:center;">
                                <div style="display:inline-block; background:#10b981; color:#ffffff; font-size:12px; font-weight:bold; padding:6px 12px; border-radius:20px; margin-bottom:12px;">APPLICATION RECEIVED</div>
                                <h1 style="margin:0; color:#ffffff; font-size:26px; line-height:1.3;">Thank You for Applying</h1>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:35px; color:#374151; font-size:15px; line-height:1.6;">
                                <p style="margin:0 0 15px;">Hello <strong style="color:#111827;">{name}</strong>,</p>
                                <p style="margin:0 0 15px;">Thank you for submitting your application for the <strong style="color:#111827;">"{job_profile}"</strong> position.</p>
                                <p style="margin:0 0 15px;">We have successfully received your application and resume. Our recruitment team will review your profile to see if it matches our current needs and will connect with you shortly regarding the next steps.</p>
                                <p style="margin:0;">Best Regards,<br><strong>Our Recruitment Team</strong></p>
                            </td>
                        </tr>
                        <tr>
                            <td style="background:#f9fafb; border-top:1px solid #e5e7eb; padding:22px 35px; text-align:center;">
                                <p style="margin:0; color:#6b7280; font-size:12px; line-height:1.6;">This is an automated confirmation email. Please do not reply directly to this message.</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
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