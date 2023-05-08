import smtplib
import base64
import hashlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def sign_message(message, private_key_path):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    hash_obj = hashlib.sha256(message.encode('utf-8'))
    hash = hash_obj.digest()

    signature = private_key.sign(
        hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature)

def send_signed_email(smtp_server, email_from, email_to, email_subject, email_body, private_key_path, email_password):
    msg = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = email_subject

    message_body = MIMEText(email_body, "plain")
    msg.attach(message_body)
    
    signature = sign_message(email_body, private_key_path)
    
    signature_attachment = MIMEBase("application", "octet-stream")
    signature_attachment.set_payload(signature)
    encoders.encode_base64(signature_attachment)
    signature_attachment.add_header("Content-Disposition", "attachment; filename=signature.sig")
    msg.attach(signature_attachment)

    try:
        with smtplib.SMTP_SSL(smtp_server) as server:
            server.login(email_from, email_password)
            server.sendmail(email_from, email_to, msg.as_string())
        return 'Письмо успешно отправлено'
    except e as Exception:
        return 'Письмо не отправлено, проверьте данные'
    
if __name__ == "__main__":
    smtp_server = "smtp.yandex.ru"
    email_from = "mail@yandex.ru"
    email_password = 'password'
    email_to = "mail2@yandex.ru"
    email_subject = "Письмо с подписью"
    email_body = "Текст письма с подписью."
    private_key_path = "key.pem"
    
    run = True

    while run:
        out_menu = int(input('''Выберите необходимое действие:        
            1 - Залогиниться в почтовом ящике
            2 - Ввести сообщение
            3 - Выбрать файл с ключами
            4 - Выбрать получателя письма
            5 - Просмотреть введенную информацию
            6 - Отправить письмо адресату
            7 - Exit
            Ваш вариант: '''))
        match out_menu:
            case 1:
                email_from = input('Логин: ')
                email_password = input('Пароль: ')
            case 2:
                email_body = input('Введите текст письма: ')
            case 3:
                private_key_path = input('Укажите полный путь до файла с ключами: ')
            case 4:
                email_to = input('Введите адрес электронной почты адресата: ')
            case 5:
                print(f'Логин: {email_from}\nПароль: {email_password}\nТекст письма: {email_body}\nАдресат: {email_to}\nПуть до ключа: {private_key_path}')
            case 6:
                print(send_signed_email(smtp_server, email_from, email_to, email_subject, email_body, private_key_path, email_password))
            case 7:
                run = False
                print('Выходим...')
