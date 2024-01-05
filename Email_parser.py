# import imaplib
# import re
# import email
# from email import policy
# from email.parser import BytesParser
# from flask import Flask, render_template
# import nltk
# from nltk import pos_tag
# from nltk.tokenize import word_tokenize
# import spacy

# app = Flask(__name__, template_folder='/home/dheeraj/Downloads/carbb/')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nlp = spacy.load("en_core_web_sm")

# def fetch_emails(username, password, server="imap.gmail.com", port=993, folder="inbox"):
#     mail = imaplib.IMAP4_SSL(server, port)
#     mail.login(username, password)
#     mail.select(folder)
    
#     status, messages = mail.search(None, "ALL")
#     messages = messages[0].split()
    
#     email_results = []

#     for msg_id in messages:
#         _, msg_data = mail.fetch(msg_id, "(RFC822)")
#         email_content = msg_data[0][1]
#         parsed_data = parse_email(email_content)
        
#         subject_pattern = re.compile(r'Welcome')
#         if subject_pattern.search(parsed_data["subject"]):
#             email_results.append(parsed_data)  

#     mail.logout()

#     return email_results

# def parse_email(email_content):
#     msg = BytesParser(policy=policy.default).parsebytes(email_content)
#     subject = msg.get("subject", "No Subject")
#     sender = msg.get("from", "No Sender")
#     date_sent = msg.get("date", "No Date")    
#     body = extract_body(msg)

#     doc = nlp(body)
#     pos_tags = [(token.text, token.pos_) for token in doc]
#     dep_parses = [(token.text, token.dep_, token.head.text) for token in doc]

#     return {
#         "subject": subject,
#         "sender": sender,
#         "date_sent": date_sent,
#         "body": body,
#         "pos_tags": pos_tags,
#         "dep_parses": dep_parses,
#     }

# def extract_body(msg):
#     def decode_payload(part):
#         payload = part.get_payload(decode=True)
#         if payload is not None:
#             return payload.decode("utf-8", "ignore")
#         return ""

#     if msg.is_multipart():
#         return "\n".join(decode_payload(part) for part in msg.walk())
#     else:
#         return decode_payload(msg)

# @app.route('/')
# def fetch_and_display_emails():
#     email_username = "edupur2020@gmail.com"
#     email_password = "yiupzfgodgsxment"

#     email_results = fetch_emails(email_username, email_password)

#     return render_template('email_results.html', email_results=email_results)

# if __name__ == "__main__":
#     app.run(debug=True)


import imaplib
import re
import email
from email import policy
from email.parser import BytesParser
from flask import Flask, render_template
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import spacy

app = Flask(__name__, template_folder='/home/dheeraj/Downloads/carbb/')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nlp = spacy.load("en_core_web_sm")

def fetch_emails(username, password, server="imap.gmail.com", port=993, folder="inbox"):
    mail = imaplib.IMAP4_SSL(server, port)
    mail.login(username, password)
    mail.select(folder)
    
    status, messages = mail.search(None, "ALL")
    messages = messages[0].split()
    
    email_results = []

    for msg_id in messages:
        _, msg_data = mail.fetch(msg_id, "(RFC822)")
        email_content = msg_data[0][1]
        parsed_data = parse_email(email_content)
        email_results.append(parsed_data)

    mail.logout()

    return email_results

def parse_email(email_content):
    msg = BytesParser(policy=policy.default).parsebytes(email_content)
    subject = msg.get("subject", "No Subject")
    sender = msg.get("from", "No Sender")
    date_sent = msg.get("date", "No Date")    
    body = extract_body(msg)

    doc = nlp(body)
    pos_tags = [(token.text, token.pos_) for token in doc]
    dep_parses = [(token.text, token.dep_, token.head.text) for token in doc]

    return {
        "subject": subject,
        "sender": sender,
        "date_sent": date_sent,
        "body": body,
        "pos_tags": pos_tags,
        "dep_parses": dep_parses,
    }

def extract_body(msg):
    def decode_payload(part):
        payload = part.get_payload(decode=True)
        if payload is not None:
            return payload.decode("utf-8", "ignore")
        return ""

    if msg.is_multipart():
        return "\n".join(decode_payload(part) for part in msg.walk())
    else:
        return decode_payload(msg)

@app.route('/')
def fetch_and_display_emails():
    email_username = "edupur2020@gmail.com"
    email_password = "yiupzfgodgsxment"

    email_results = fetch_emails(email_username, email_password)

    return render_template('email_results.html', email_results=email_results)

if __name__ == "__main__":
    app.run(debug=True)
