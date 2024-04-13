import requests
from scrapers.campus import Campus
from constants import TELEGRAM_API_URL, USER_CHAT_ID
from dotenv import load_dotenv

load_dotenv()


def get_courses():
    campus = Campus()
    campus.get_courses()

def get_news():
    campus = Campus()
    return campus.get_unreaded_posts()


def get_updates():
    response = requests.post(
        TELEGRAM_API_URL+"/getUpdates",
        headers={'Content_type': 'Application/json'},
        data={
            'chat_id': USER_CHAT_ID,
            'limit': 1,
            'timeout': 5
        }
    )
    print(response.content)

def send_message(content: str, format=''):
    response = requests.post(
        TELEGRAM_API_URL+"/sendMessage",
        headers={'Content_type': 'Application/json'},
        data={
            'chat_id': '6290970561',
            'text': content,
            'parse_mode':format
        }
    )
    print(response.content)

course_email_title = "❗️❗️❗️ De {0} hay varios mensajes"

course_email_message = "{0}"

without_messages = """🎉 No hay mensajes del curso {0}"""



def send_unread_emails():
    campus = Campus()
    messages = campus.read_courses_email()
    for course in messages: 
        if messages[course] and len(messages[course]):
            send_message(course_email_title.format(course))
            for message in messages[course]:
                send_message(course_email_message.format(message))
            # send_message("Mensages Leidos: \n\nCurso: {c} \n\n {m}".format(c=i, m='\n\n '.join(messages[i]) if messages[i] else ""))
        else:
            send_message(without_messages.format(course))

send_unread_emails()
# send_message()
# def job():
#     # send_message()
#     get_news()
#     print(BOT_API_KEY)

# schedule.every(12).hour.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)