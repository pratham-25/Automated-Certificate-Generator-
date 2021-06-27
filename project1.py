from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
df = pd.read_csv('data.csv')
font = ImageFont.truetype('arial.ttf',60)
for index,j in df.iterrows():
    img = Image.open('image.jpeg')
    draw = ImageDraw.Draw(img)
    draw.text(xy=(371,330),text='{}'.format(j['name']),fill=(0,0,0),font=font)
    img.save('pictures/{}.jpeg'.format(j['name']))
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv

mail_content = '''We congratulate you on your grand success in the National Cricket Championship. 
Please find your Certificate of appreciation attached below.
                                  Thank You
'''
#The mail addresses and password
sender_address = 'edummy610@gmail.com'
sender_pass = 'dummy_1234'
with open('data.csv',encoding = 'utf-8') as file:
    reader = csv.reader(file)
    emails = []
    names = []

    for row in reader:
        emails.append(row[1])
        names.append(row[0])
del emails[0]
del names[0]
print(names)
print(emails)
receiver_address = ''
#Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'Congratulations'

message.attach(MIMEText(mail_content, 'plain'))

session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
session.starttls() #enable security

for i in range(len(names)):
    attach_file_name = 'pictures/' + names[i] + '.jpeg'
    attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
    payload = MIMEBase('image', 'jpeg')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # encode the attachment
    # add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    attach_file_name = ' '
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, emails[i], text)
    payload.set_payload((attach_file).close())
    attach_file_name = ' '
session.quit()

print('Mail Sent')