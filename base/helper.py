from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from django.conf import settings
import uuid
from django.core.mail import EmailMessage
from accounts.models import Cart, CartItem

def convert_invoice_to_pdf(params:dict):
    template = get_template("pdf/invoice_2.html")
    html = template.render(params)
    file_name = f'Invoice_{uuid.uuid4()}.pdf'
    pdf = None
    try:
        with open(str(settings.BASE_DIR)+ f'\public\static\pdfs\invoices\{file_name}', 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), output)
            print(pdf)
    except Exception as e:
        print(e)

    return file_name, output

def send_invoice_mail(cart:Cart):
    context = {"customer": str(cart.user), "cart_items":CartItem.objects.filter(cart= cart).all() }
    email = cart.user.username
    subject = "Order Receipt from EShop"
    body = "Dear customer, please find attached the receipt for youexir order. Thank you for choosing EShop."
    file_name, file_buffer = convert_invoice_to_pdf({})
    with open(str(settings.BASE_DIR)+ f'\public\static\pdfs\invoices\{file_name}', 'rb') as file:
        file_content = file.read()
    attachment = [file_name, file_content, "application/pdf"]
    attachment = tuple(attachment)
    email = EmailMessage(subject=subject, body=body,attachments=[attachment], to=[email])
    email.send()

