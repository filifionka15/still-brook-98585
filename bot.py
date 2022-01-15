import threading
from TelebotFunctions  import *
from BotTypes import *
import psycopg2
import WebNewsParser


def main():
    bot.delete_webhook()
    threading.Thread(target = bot.infinity_polling).start()
    threading.Thread(target = WebNewsParser.WebNewsParser).start()

    while True:
        from_main_thread_blocking()


if __name__ == "__main__":
    main()
    