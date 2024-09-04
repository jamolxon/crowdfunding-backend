from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_restore_password(*args, **kwargs):
    """
    Send email verification code to the User
    """
    subject, from_email, to = (
        "Password reset code from Crowdfunding.",
        settings.EMAIL_HOST_USER,
        kwargs["email"],
    )

    code = [digit for digit in kwargs["code"]]

    html_content = render_to_string(
        "email-restore.html",
        context={
            "code": code,
            "domain": kwargs["domain"],
            # "uid": kwargs["uid"],
            "token": kwargs["uid"] + kwargs["token"],
            # "appstore": "http://drive.google.com/uc?export=view&id=1bWbRSOTH1Uc-Cp-MxCIRzoDsJeo7-ryU",
            # "googleplay": "http://drive.google.com/uc?export=view&id=1X4HFmhohK23dQxgoLn5Y-fJMRGNlByNR",
            # "facebook": "http://drive.google.com/uc?export=view&id=1Ub76oDKLOTI0KMmN8a2moO7IyljSoJOm",
            # "instagram": "http://drive.google.com/uc?export=view&id=1yATbPpxTeVHeoIfOBy5gr_Pjr4rNo3Hh",
            # "telegram": "http://drive.google.com/uc?export=view&id=1CnjgFrZypij2_XPxDRPdpMyuQXLVUT2q",
            # "smile": "http://drive.google.com/uc?export=view&id=1K3NffoLe__esOIZwQSrm1XSdd99_e7kM",
            # "lock": "http://drive.google.com/uc?export=view&id=1y5E5lh0AcdKOwUyg0vksHyW7NgwBpxMK",
            # "templatephones": "http://drive.google.com/uc?export=view&id=1kG0aQJPFLaMp4c4VRmKyNNXVMwUBCVGj",
            # "lenta": "http://drive.google.com/uc?export=view&id=1nGg2_jkn7Q__dR0CebYDR2C-A9Wi3hTk",
            # #    "bgleft": "http://drive.google.com/uc?export=view&id=1rkWivUYyRQ2vxGlZjdNzVlo_HW6cKC-l",
            # "bgright": "http://drive.google.com/uc?export=view&id=1bxFfMTuLj05Lzopl44fSZ7HBABJ-0bNo",
            # "leftimgbg": "http://drive.google.com/uc?export=view&id=14GdERRSd9fjMyMRDuxQyjuZ0v7RIrO9G",
            # "emailock": "http://drive.google.com/uc?export=view&id=1dlbm3L9_NBS4ktTERJ27spzWK3UFNC8N",
        },
    )  # render with dynamic value
    text_content = strip_tags(
        html_content
    )  # Strip the html tag. So people can see the pure text at least.
    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_email_confirmation(*args, **kwargs):
    """
    Send email restore password code to the User
    """
    subject, from_email, to = (
        "Registration confirmation code from Crowdfunding",
        settings.EMAIL_HOST_USER,
        kwargs["email"],
    )

    code = [digit for digit in kwargs["code"]]

    html_content = render_to_string(
        "email-confirmation.html",
        context={
            "code": code,
            "domain": kwargs["domain"],
            # "uid": kwargs["uid"],
            "token": kwargs["uid"] + kwargs["token"],
            # "appstore": "http://drive.google.com/uc?export=view&id=1bWbRSOTH1Uc-Cp-MxCIRzoDsJeo7-ryU",
            # "googleplay": "http://drive.google.com/uc?export=view&id=1X4HFmhohK23dQxgoLn5Y-fJMRGNlByNR",
            # "facebook": "http://drive.google.com/uc?export=view&id=1Ub76oDKLOTI0KMmN8a2moO7IyljSoJOm",
            # "instagram": "http://drive.google.com/uc?export=view&id=1yATbPpxTeVHeoIfOBy5gr_Pjr4rNo3Hh",
            # "telegram": "http://drive.google.com/uc?export=view&id=1CnjgFrZypij2_XPxDRPdpMyuQXLVUT2q",
            # "smile": "http://drive.google.com/uc?export=view&id=1K3NffoLe__esOIZwQSrm1XSdd99_e7kM",
            # "lock": "http://drive.google.com/uc?export=view&id=1y5E5lh0AcdKOwUyg0vksHyW7NgwBpxMK",
            # "templatephones": "http://drive.google.com/uc?export=view&id=1kG0aQJPFLaMp4c4VRmKyNNXVMwUBCVGj",
            # "lenta": "http://drive.google.com/uc?export=view&id=1nGg2_jkn7Q__dR0CebYDR2C-A9Wi3hTk",
            # #    "bgleft": "http://drive.google.com/uc?export=view&id=1rkWivUYyRQ2vxGlZjdNzVlo_HW6cKC-l",
            # "bgright": "http://drive.google.com/uc?export=view&id=1bxFfMTuLj05Lzopl44fSZ7HBABJ-0bNo",
            # "leftimgbg": "http://drive.google.com/uc?export=view&id=14GdERRSd9fjMyMRDuxQyjuZ0v7RIrO9G",
            # "emailicon": "http://drive.google.com/uc?export=view&id=1KrbJLRB8U_gQXyaSna1_0RKcgvaqKqPd",
        },
    )  # render with dynamic value
    text_content = strip_tags(
        html_content
    )  # Strip the html tag. So people can see the pure text at least.
    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def render_template(request):
    host = settings.HOST
    context = {"host": host}
    return render(request, "email-restore.html", context)
