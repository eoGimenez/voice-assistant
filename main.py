import webbrowser
import datetime
import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import wikipedia

# escuchar mic y devolver el audio como texto.


def transform_aud_in_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as origen:
        # delay de espera.
        recognizer.pause_threshold = .8
        print("Ya estoy escuchando...")
        audio = recognizer.listen(origen)
        try:
            # buscar en google
            pedido = recognizer.recognize_google(audio, language="es-ar")
            # print(f'Dijiste: "{pedido}"')
            return pedido
        except sr.UnknownValueError:
            print("Lo lamento, no te entendí")
            return "Waitting.."
        except sr.RequestError:
            print("No hay servicio..")
            return "Waitting.."
        except Exception as error:
            print(f"Algo ha salido mal {error}")
            return "Waitting..."


# transform_aud_in_text()

def talk(message):
    engine = pyttsx3.init()
    # engine.setProperty('voice', variable_en_la_que_guardes_la_id_de_la_voz)
    engine.say(message)
    engine.runAndWait()

# para ver los idiomas que tengas instalados
# engine = pyttsx3.init()
# for voice in engine.getProperty('voices'):
#     print(voice)


def ask_day():
    day = datetime.date.today()
    week_day = day.weekday()
    week_tuple = ('Lunes', 'Martes', 'Miércoles',
                  'Jueves', 'Viernes', 'Sábado', 'Domingo')

    talk(f'Hoy es {week_tuple[week_day]}')


def ask_time():
    hour = datetime.datetime.now()
    talk(f'Son las{hour.strftime("%H")} horas y {hour.strftime("%M")} minutos')


def welcome():
    hour = datetime.datetime.now()
    if hour.hour < 6 or hour.hour > 20:
        greeting = 'Buenas noches'
    elif 6 <= hour.hour < 13:
        greeting = 'Buen día'
    else:
        greeting = 'Buenas tardes'
    talk(f'{greeting} soy Helena, tu asistente personal. Por favor dime con que te puedo ayudar')
    talk('Si quieres que deje de escuchar, solo dí cerrar conversación')


def ask_things():
    welcome()
    while True:
        query = transform_aud_in_text().lower()
        if 'cerrar conversación' in query:
            talk('Hasta luego !')
            break
        if 'abrir youtube' in query:
            talk('Con Gusto, abriré YouTube')
            webbrowser.open('https://www.youtube.com')
            continue
        if 'abrir navegador' in query:
            talk('Ahora mismo!')
            webbrowser.open('https://www.google.com')
            continue
        if 'qué día es hoy' in query:
            ask_day()
            continue
        if 'qué hora es' in query:
            ask_time()
            continue
        if 'busca en wikipedia' in query:
            talk('Buscando en Wikipedia')
            query = query.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            result = wikipedia.summary(query, sentences=1)
            talk('Encontré lo siguiente en wikipedia:')
            talk(result)
            continue
        if 'busca en internet' in query:
            talk('Ya mismo estoy en ello')
            query = query.replace('busca en internet', '')
            pywhatkit.search(query)
            talk('Esto es lo que he encontrado')
            continue
        if 'reproducir' in query:
            talk('Muy bien ! Ya empiezo a repdroducirlo')
            query = query.replace('reproducir', '')
            pywhatkit.playonyt(query)
            continue
        if 'broma' in query:
            talk(pyjokes.get_joke('es'))
            continue
        if 'precio de las acciones' in query:
            accion = query.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_searched = cartera[accion]
                accion_searched = yf.Ticker(accion_searched)
                actual_price = accion_searched.info['regularMarketPrice']
                talk(f'La encontré, el precio de {accion} es {actual_price}')
                continue
            except:
                talk('Lo lamento, no la he encontrado.')


ask_things()
