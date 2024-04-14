from dotenv import load_dotenv

from services.bot import CampusBot

load_dotenv()

def main():
    bot = CampusBot()
    bot.send_unread_emails()

if __name__ == "__main__":
    main()

# send_unread_emails()
# send_message()
# def job():
#     # send_message()
#     get_news()
#     print(BOT_API_KEY)

# schedule.every(12).hour.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)