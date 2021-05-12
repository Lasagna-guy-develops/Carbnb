from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from smtplib import SMTP
class enviar():
    def accion(correo, nombre, numero):

        mensaje =MIMEMultipart("plain")
        mensaje["From"]= "carbnbeia@gmail.com"
        mensaje["To"]= correo
        str="Factura de compra número "+numero+" - VaporBlack"
        mensaje["subject"]= (str)
        adjunto= MIMEBase("application","octect-stream")
        adjunto.set_payload(open(nombre,"rb").read())
        adjunto.set_charset("lolazo")
        adjunto.add_header("content-Disposition",'attachment; filename='+nombre)
        mensaje.attach(adjunto)
        smtp= SMTP("smtp.gmail.com")
        smtp.starttls()
        smtp.login("fixparty.comprobante@gmail.com","FixParty0115")

        smtp.sendmail("fixparty.comprobante@gmail.com",correo,mensaje.as_string())
        smtp.quit()
        print("enviado correctamente")

    def codigo(correo,codigo):
        mensaje = MIMEMultipart("plain")
        mensaje["From"] = "carbnbeia@gmail.com"
        mensaje["To"] = correo
        mensaje["subject"] = "Recuperar contraseña - Carbnb"
        body = ("Por favor ingresar el código: " + str(codigo) + " en la aplicación para acceder al cambio de contraseña")
        mensaje.attach(MIMEText(body, 'plain'))
        smtp = SMTP("smtp.gmail.com")
        smtp.starttls()
        smtp.login("carbnbeia@gmail.com", "JuanfeEsMarica")

        smtp.sendmail("carbnbeia@gmail.com", correo, mensaje.as_string())
        smtp.quit()
        print("enviado correctamente")

    # codigo("juan220142@gmail.com","1234835")