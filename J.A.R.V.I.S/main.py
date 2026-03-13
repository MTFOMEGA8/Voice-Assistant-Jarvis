import speech_recognition as sr
from groq import Groq
import pyttsx3
import sys
import os
from dotenv import load_dotenv
from logger_config import setup_logger 

log = setup_logger()

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    log.info("Токен успешно загружен из .env")
else:
    log.error("Ошибка: Токен не найден! Проверьте файл .env")

def process_voice_command(text):
    log.info(f"Пользователь сказал: {text}")
    try:
        pass
    except Exception as e:
        log.error(f"Произошла ошибка при обработке команды: {e}")

os.environ["PYTHONIOENCODING"] = "utf-8"

client = Groq(api_key=GROQ_API_KEY)

def speak(text):
    """Принудительная озвучка с перезапуском движка для каждой фразы"""
    if not text: return
    try:
        print(f"Джарвис: {text}")
        engine = pyttsx3.init()
        engine.setProperty('rate', 180) # Скорость Джарвиса
        
        # Выбор голоса (обычно voices[0] - мужской)
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
            
        engine.say(text)
        engine.runAndWait()
        engine.stop() # Обязательно освобождаем ресурс
    except Exception as e:
        print(f"Ошибка аудио-модуля: {e}")

def get_ai_response(prompt):
    """Запрос к разуму Groq (Llama 3)"""
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Ты - Джарвис, вежливый ИИ Тони Старка. Отвечай кратко на русском, называй меня 'сэр'."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Сэр, возникла заминка в канале Groq: {str(e)}"

def listen():
    """Слух Джарвиса, адаптированный под фоновое общение в Discord"""
    recognizer = sr.Recognizer()
    
    recognizer.dynamic_energy_threshold = False 
    recognizer.energy_threshold = 3500 
    recognizer.pause_threshold = 0.4 
    recognizer.non_speaking_duration = 0.2
    
    with sr.Microphone() as source:
        print("\n[Анализ вашего голоса...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        
        try:
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=4)
            text = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Вы: {text}")
            return text.lower()
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return ""
        except Exception as e:
            return ""
        
if __name__ == "__main__":
    speak("Протокол номер один точка два запущен. Голос и слух синхронизированы, сэр.")
    
    while True:
        voice_input = listen()
        
        # Проверка на ключевое имя
        if "джарвис" in voice_input:
            query = voice_input.replace("джарвис", "").strip()
            
            if not query:
                speak("Слушаю вас, сэр.")
                query = listen()
            
            if query:
                answer = get_ai_response(query)
                speak(answer)
        
        # Экстренное завершение
        if "отключись" in voice_input or "выключись" in voice_input:
            speak("Системы переходят в режим сна. Хорошего отдыха, сэр.")
            sys.exit()