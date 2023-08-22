import random
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(mailDestinatario,subject,message):
    # Configuración del servidor SMTP y credenciales
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    mi_correo = 'usafyabot2.4@gmail.com'
    password = 'mfoubsxgpnovkjbx'

    # Crear objeto para el correo electrónico
    msg = MIMEMultipart()
    msg['From'] = mi_correo
    msg['To'] = mailDestinatario
    msg['Subject'] = subject

    # Cuerpo del correo
    msg.attach(MIMEText(message, 'plain'))

    # Establecer conexión con el servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(mi_correo, password)

    # Enviar el correo electrónico
    server.sendmail(mi_correo, mailDestinatario, msg.as_string())

    # Cerrar la conexión
    server.quit()

#sendEmail('franmartos11@gmail.com')

def cleanEmailFormat(array):
    cleanArray = []
    for mail in array:
        cleanArray.append(mail.replace('mailto:', ''))
    return cleanArray

def sendEmailsToEverione(arrayMails):

    subject = input('Ingrese el asunto del mail que desea enviar : ')
    message = input('Ingrese el mensaje que desea enviar a todos los mails : ')

    # limpio formato de mails obtenidos
    cleanArray = cleanEmailFormat(arrayMails)

    #recorro el array enviando mails con tiempo de espera random
    count = 1
    for mail in cleanArray:
        sendEmail(mail, subject, message)
        print(f'Email numero {count} de {len(cleanArray)} ')
        print(f'Email a {mail} se envio correctamente.')
        print(' ')
        count += 1
        time.sleep(random.randint(30, 90))

#arr = ['franmartos11@gmail.com','mailto:usafyabot2.3@gmail.com','usafyabot2.4@gmail.com']
#sendEmailsToEverione(arr)