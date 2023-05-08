import imaplib
import email
import base64
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import sys

output_folder = ''

def login_to_email(username, password):
    mail = imaplib.IMAP4_SSL("imap.yandex.com")
    mail.login(username, password)
    return mail

def get_emails(mail, n=10):
    mail.select("inbox")
    _, message_numbers_raw = mail.search(None, "ALL")
    message_numbers = message_numbers_raw[0].split()[-n:]

    for message_number in message_numbers:
        _, msg_data = mail.fetch(message_number, "(BODY[HEADER.FIELDS (SUBJECT FROM DATE)])")
        msg = email.message_from_bytes(msg_data[0][1])
        print(f"{int(message_number)}: From:", msg["From"], "\nSubject:", msg["Subject"], "\nDate:", msg['Date'], "\n")

def open_email(mail, message_number):
    _, msg_data = mail.fetch(message_number, "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])
    return msg

def select_public_key_cert(file_path):
    with open(file_path, "rb") as cert_file:
        private_key = serialization.load_pem_private_key(
            cert_file.read(),
            password=None,
            backend=default_backend()
        )
        public_key = private_key.public_key()
    return public_key

def verify_signature(msg, cert, message_number, name_file):
    email_body = ''

    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            email_body = part.get_payload(decode=True)
        elif part.get_filename() == name_file:
            sig = part.get_payload(decode=True)
            break
    else:
        print("No signature found")
        return
    
    #signature_file = os.path.join(output_folder, name_file)
    #with open(signature_file, 'rb') as signature_file:
    #        signature_b64 = signature_file.read()

    signature = base64.b64decode(sig)

    hash_object = hashlib.sha256(email_body)
    hash = hash_object.digest()

    try:
        cert.verify(signature, hash, 
                    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                          hashes.SHA256())
        print("Подпись действительна")
    except Exception as e:
        print("Подпись не действительна. Ошибка: ")

if __name__ == "__main__":
    username = input("Введите ваш email: ")
    password = input("Введите пароль: ")

    mail = login_to_email(username, password)
    get_emails(mail)

    message_number = input("Укажите номер письма: ")
    name_file = input("Укажите имя sig-файла: ")
    msg = open_email(mail, message_number)

    public_key_file = input("Укажите публичный ключ pem: ")
    try:
        cert = select_public_key_cert(public_key_file)
    except:
        print('Подпись не действительна! Проверьте данные')
        sys.exit()

    verify_signature(msg, cert, message_number, name_file)

    mail.logout()
