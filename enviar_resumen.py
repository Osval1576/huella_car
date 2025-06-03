# enviar_resumen.py


import smtplib
from email.message import EmailMessage

EMAIL_EMISOR = "osval12.nogal@gmail.com"
EMAIL_PASSWORD = "ysnykkbpeqwfduxy"  # SIN espacios

def enviar_datos_calculados(medio, distancia, huella):
    msg = EmailMessage()
    msg.set_content(f"Medio: {medio}, Distancia: {distancia}, Huella: {huella}")
    msg["Subject"] = "Resumen de Huella de Carbono"
    msg["From"] = EMAIL_EMISOR
    msg["To"] = "phineas.ferd31@gmail.com"  # puedes poner el mismo emisor para prueba

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_EMISOR, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("Correo enviado correctamente.")
