import csv
from datetime import datetime, timedelta
from flask import Flask, render_template, request, session
from enviar_resumen import enviar_datos_calculados  # Asegúrate de tener este archivo

app = Flask(__name__)
app.secret_key = 'carbono123'
app.permanent_session_lifetime = timedelta(minutes=60)

FACTORES = {
    'auto': 0.21,
    'moto': 0.12,
    'autobus': 0.05,
    'metro': 0.04,
    'avion': 0.285,
    'bicicleta': 0.0,
    'caminar': 0.0
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'historial' not in session:
        session['historial'] = []

    resultado = None
    recomendaciones = []

    if request.method == 'POST':
        medio = request.form['medio']
        distancia = float(request.form['distancia'])

        if medio in FACTORES:
            factor = FACTORES[medio]
            huella = distancia * factor
            resultado = round(huella, 2)

            # Guardar en CSV
            with open("datos_usuarios.csv", mode="a", newline="") as archivo:
                writer = csv.writer(archivo)
                writer.writerow([datetime.now(), medio, distancia, huella])

            # Enviar correo automático
            enviar_datos_calculados(medio, distancia, huella)

            # Historial y recomendaciones
            session['historial'].append({'medio': medio, 'distancia': distancia, 'huella': resultado})
            session.modified = True

            if resultado > 20:
                recomendaciones.append("Considera reducir el uso de transporte con alta emisión de CO₂ como el avión o auto.")
            if medio in ['auto', 'moto', 'avion']:
                recomendaciones.append("Podrías usar transporte público o bicicleta para trayectos cortos.")
            if medio in ['bicicleta', 'caminar']:
                recomendaciones.append("¡Excelente! Estos medios no generan emisiones de CO₂.")

    return render_template('index.html',
                           resultado=resultado,
                           historial=session['historial'],
                           recomendaciones=recomendaciones,
                           factores=FACTORES)

if __name__ == '__main__':
    app.run(debug=True)
