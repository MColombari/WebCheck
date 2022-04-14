""" BotName = 'MC_Web_Check_bot' """

# SQLite imports
from sqlite3 import Error
from interaction import LDB

# Bot Imports
import logging
from urllib.error import URLError, HTTPError
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Web check import
import hashlib
from urllib.request import urlopen, Request

# Time import

# Bot key import
from botKey import TOKEN

# Constant values
TIME_BETWEEN_CHEK = 1800

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def checking(context: CallbackContext):
    """
    try:
        job = context.job
        i = 0
        if job.context in urls.keys():
            for [urlString, hashValue] in urls[job.context]:
                url = Request(urlString, headers={'User-Agent': 'Mozilla/5.0'})
                response = urlopen(url).read()
                if hashValue != hashlib.sha224(response).hexdigest():
                    context.bot.send_message(job.context, text="[{}]\t'{}' has updated.".format(
                        datetime.now().strftime(" %Y/%m/%d %H:%M:%S "), urlString))
                    urls[job.context][i][1] = hashlib.sha224(response).hexdigest()
                i += 1

    except HTTPError as e:
        # Fix this and like this in all code.
        context.bot.send_message(job.context, text="Usage: /add <url>\n'{}' doesn't exists.")
    except URLError as e:
        context.bot.send_message(job.context, text="Usage: /add <url>\n'{}' is not valid website.")
    except Exception as e:
        context.bot.send_message(job.context, text="Unusual exception catched '{}'".format(e))
    """

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""
    Command List:
    \t/start      -- Bot starting.
    \t/help       -- Show command list.
    \t/add <url> -- Add url to check.
    \t/stop       -- Stop checking website.
    \t/isChecking -- Checking state.
    \t/check     -- Force cheking all website.
    \t/showUrl -- Show all website is checking.
    \t/removeByIndex <Index> -- Remove url by index (shown in /showUrl).""")


def add(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    try:
        # Check Website
        if (context.args.__len__() == 0) or (not isinstance(context.args[0], str)):
            update.message.reply_text('Usage: /add <url>')
            return
        url = Request(context.args[0], headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(url).read()
        hash_value = hashlib.sha224(response).hexdigest()

        # Update Database
        local_db = LDB()
        query_result = local_db.query('SELECT COUNT(*) FROM chat WHERE id=?', (chat_id,))
        if query_result[0][0][0] == 0:
            local_db.query('INSERT INTO chat(id) VALUES (?)', (chat_id,))
        query_result = local_db.query('SELECT COUNT(*) FROM record WHERE chat_id=? AND url=?', (chat_id,context.args[0]))
        if query_result[0][0][0] == 0:
            local_db.query('INSERT INTO record(chat_id, url, hash) VALUES (?,?,?)', (chat_id, context.args[0], hash_value))
            update.message.reply_text("'{}'\nWill be che checked.".format(context.args[0]))
        else:
            update.message.reply_text("'{}'\nIt was already added to the list of website.".format(context.args[0]))

        # Start Checking for the user whom call the command 'add'
        current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        if not current_jobs:
            context.job_queue.run_repeating(checking, TIME_BETWEEN_CHEK, context=chat_id, name=str(chat_id))

    except ValueError as e:
        update.message.reply_text("\'{}\'\nIs not a valid website.".format('<None>' if (len(context.args) == 0) else context.args[0]))
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))
    except (HTTPError, URLError) as e:
        update.message.reply_text("Unexpected Error with the website.")
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))
    except Error as e:
        update.message.reply_text("Unexpected Error with the database.")
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))
    except Exception as e:
        update.message.reply_text("Unusual exception caught.")
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))


def stop(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if not current_jobs:
        update.message.reply_text("Cheking was already stopped.")
        return
    for job in current_jobs:
        job.schedule_removal()
        update.message.reply_text("Stop cheking.")


def isChecking(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if not current_jobs:
        update.message.reply_text("Is Checking = False.")
        return
    update.message.reply_text("Is Checking = True.")


"""
def check(update: Update, context: CallbackContext):
    try:
        update.message.reply_text("Start checking...")
        for [urlString, hashValue] in urls[update.message.chat_id]:
            url = Request(urlString, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(url).read()
            if hashValue != hashlib.sha224(response).hexdigest():
                update.message.reply_text(
                    "[{}]\t'{}' has updated.".format(datetime.now().strftime(" %Y/%m/%d %H:%M:%S "), urlString))
            else:
                update.message.reply_text(
                    "[{}]\t'{}' hasn't updated.".format(datetime.now().strftime(" %Y/%m/%d %H:%M:%S "), urlString))
        update.message.reply_text("All Website are checked")
    except HTTPError as e:
        update.message.reply_text("Usage: /add <url>\n'{}' doesn't exists.")
    except URLError as e:
        update.message.reply_text("Usage: /add <url>\n'{}' is not valid website.")
    except Exception as e:
        update.message.reply_text("Unusual exception catched '{}'".format(e))
"""

"""
def showUrl(update: Update, context: CallbackContext):
    out = 'Website saved:'
    if update.message.chat_id not in urls.keys():
        urls[update.message.chat_id] = list()
    if len(urls[update.message.chat_id]) == 0:
        update.message.reply_text("No website saved.")
        return
    for i in range(0, len(urls[update.message.chat_id])):
        out += '\n\t' + str(i) + ') ' + urls[update.message.chat_id][int(i)][0]
    update.message.reply_text(out)
"""

"""
def removeByIndex(update: Update, context: CallbackContext):
    try:
        i = int(context.args[0])
        if (i >= len(urls[update.message.chat_id])) | (i < 0):
            update.message.reply_text("'{}', invalid number.".format(i))
            return
        urlString = urls[update.message.chat_id].pop(i)[0]
        update.message.reply_text("'{}', removed.".format(urlString))
    except ValueError as e:
        update.message.reply_text("Value exception '{}' is not a integer\n[{}]".format(i, e))
    except IndexError as e:
        update.message.reply_text("Index exception '{}'".format(e))
    except Exception as e:
        update.message.reply_text("Unusual exception catched '{}'".format(e))
"""

def nonCommand(update: Update, context: CallbackContext):
    update.message.reply_text("Da frick are ya doing?")


def error(update: Update, context: CallbackContext):
    update.message.reply_text('Error, Caused error {}'.format(context.error))
    logger.warning('Error, Caused error {}'.format(context.error))


def main():
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("add", add))
    # dp.add_handler(CommandHandler("check", check))
    # dp.add_handler(CommandHandler("showUrl", showUrl))
    # dp.add_handler(CommandHandler("removeByIndex", removeByIndex))
    # dp.add_handler(CommandHandler("removeByUrl", removeByIndex))

    # on non command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, nonCommand))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Blocks until one of the signals are received and stops the updater.
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
