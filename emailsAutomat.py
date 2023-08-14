import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(mailDestinatario):
    # Configuración del servidor SMTP y credenciales
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    mi_correo = 'usafyabot2.4@gmail.com'
    password = 'mfoubsxgpnovkjbx'

    # Crear objeto para el correo electrónico
    msg = MIMEMultipart()
    msg['From'] = mi_correo
    msg['To'] = mailDestinatario
    msg['Subject'] = 'Asunto del correo'

    # Cuerpo del correo
    mensaje = "Este es el contenido del correo."
    msg.attach(MIMEText(mensaje, 'plain'))

    # Establecer conexión con el servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(mi_correo, password)

    # Enviar el correo electrónico
    server.sendmail(mi_correo, mailDestinatario, msg.as_string())

    # Cerrar la conexión
    server.quit()

sendEmail('franmartos11@gmail.com')


