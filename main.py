import objc
import pyttsx3
import speech_recognition as sr
import pyaudio
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia


# opciones de voz/idioma
id1 = "com.apple.speech.synthesis.voice.diego"
id2 = "com.apple.speech.synthesis.voice.jorge"
id3 = "com.apple.speech.synthesis.voice.karen"


# Escuchar nuestro micrófono y devolver el audio como texto
def transforma_audio_en_texto():
    # almacenar recognizer en una variable
    r = sr.Recognizer()

    # configurar el micrófono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzó la grabación
        print("Ya puedes hablar")

        # guardar lo que escuché como audio
        audio = r.listen(origen)

        try:
            # buscar en Google
            pedido = r.recognize_google(audio, language="es-ar")

            # prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # devolver pedido
            return pedido

        # en caso de que no comprenda audio
        except sr.UnknownValueError:
            # prueba de que no comprendió el audio
            print("Ups, no entendí")

            # devolver error
            return "Sigo esperando"

        # en caso de no resolver el pedido
        except sr.RequestError:
            # prueba de que no hay servicio
            print("Ups, no hay servicio")

            # devolver pedido
            return "Sigo esperando"

        # error inesperado
        except Exception as e:
            print(f"Ups, algo ha salido mal: {e}")
            # devolver pedido
            return "Sigo esperando"


# Función para que el asistente pueda ser escuchado
def hablar(mensaje):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    #engine.setProperty('voice', id1)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# Informar el día de la semana
def pedir_dia():
    # crear variable con dato de hoy
    dia = datetime.date.today()

    # crear variable para el día de la semana
    dia_semana = dia.weekday()

    # diccionario con nombres de días
    calendario = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}

    # decir día de la semana en voz alta
    hablar(f"Hoy es {calendario[dia_semana]}")


# Informar hora
def pedir_hora():
        # obtener la hora actual
        hora_actual = datetime.datetime.now()

        # formatear la hora como una cadena legible
        hora_legible = hora_actual.strftime("%H:%M")

        # imprimir la hora en la consola
        print("Hora actual:", hora_legible)

        # decir la hora en voz alta
        hablar(f"La hora actual es {hora_legible}")

pedir_hora()


# Función saludo inicial
def saludo_inicial():
    # crear variable con la hora
    hora = datetime.datetime.now()
    if 6 <= hora.hour < 13:
        momento = "Buen día"
    elif 13 <= hora.hour < 20:
        momento = "Buenas tardes"
    else:
        momento = "Buenas noches"

    # decir el saludo
    hablar(f"{momento} Micaela, soy Anna, tu asistente personal. ¿En qué te puedo ayudar?")


# Función central del asistente
def pedir_cosas():
    # activar saludo inicial

    saludo_inicial()

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:
        # activar el micrófono y guardar el pedido en un string
        pedido = transforma_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com/')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy en eso')
            webbrowser.open('https://www.google.com/')
            continue
        elif 'que día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'que hora es' in pedido:
            pedir_hora()
            continue
        elif 'buscar en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'AAPL', 'amazon': 'AMZN', 'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f"La encontré, el precio de {accion} es {precio_actual}")
                continue
            except:
                hablar("Perdón, pero no la he encontrado")
                continue
        elif 'adiós' in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas")
            break


pedir_cosas()