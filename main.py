""" BotName = 'MC_Web_Check_bot' """

# SQLite imports
from datetime import datetime
from sqlite3 import Error
from interaction import LocalDB

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
    chat_id = context.job.context
    try:
        query_result = LocalDB.query('SELECT url, hash FROM record WHERE chat_id=?', (chat_id,))
        for row in query_result[0]:
            url_string = row[0]
            hash_value = row[1]

            url = Request(url_string, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(url).read()
            if hash_value != hashlib.sha224(response).hexdigest():
                text = "[{}]\t'{}' has updated.".format(datetime.now().strftime(" %Y/%m/%d %H:%M:%S "), url_string)
                context.bot.send_message(chat_id, text)
                new_hash = hashlib.sha224(response).hexdigest()
                LocalDB.query('UPDATE record SET hash=? WHERE chat_id=? AND url=?', (new_hash, chat_id, url_string))

    except HTTPError as e:
        context.bot.send_message(chat_id, "\'{}\'Can't be found.".format(context.args[0]))
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))
    except Error as e:
        context.bot.send_message(chat_id, "Unexpected Error with the database.")
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))
    except Exception as e:
        context.bot.send_message(chat_id, "Unusual exception caught.")
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""
    Command List:
    \t/start      -- Bot welcome message.
    \t/help       -- Show command list.
    \t/add <url> -- Add url to check.
    \t/showUrl -- Show all website is checking.
    \t/removeByUrl <url> -- Remove url by index (shown in /showUrl).""")


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
        query_result = LocalDB.query('SELECT COUNT(*) FROM chat WHERE id=?', (chat_id,))
        if query_result[0][0][0] == 0:
            LocalDB.query('INSERT INTO chat(id) VALUES (?)', (chat_id,))
        query_result = LocalDB.query('SELECT COUNT(*) FROM record WHERE chat_id=? AND url=?',
                                     (chat_id, context.args[0]))
        if query_result[0][0][0] == 0:
            LocalDB.query('INSERT INTO record(chat_id, url, hash) VALUES (?,?,?)',
                          (chat_id, context.args[0], hash_value))
            update.message.reply_text("'{}'\nWill be che checked.".format(context.args[0]))
        else:
            update.message.reply_text("'{}'\nIt was already added to the list of website.".format(context.args[0]))

        # Start Checking for the user whom call the command 'add'
        current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        if not current_jobs:
            context.job_queue.run_repeating(checking, TIME_BETWEEN_CHEK, context=chat_id, name=str(chat_id))

    except (ValueError, URLError) as e:
        update.message.reply_text(
            "\'{}\'\nIs not a valid website.".format('<None>' if (len(context.args) == 0) else context.args[0]))
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))
    except HTTPError as e:
        update.message.reply_text("\'{}\'Can't be found.".format(context.args[0]))
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))
    except Error as e:
        update.message.reply_text("Unexpected Error with the database.")
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))
    except Exception as e:
        update.message.reply_text("Unusual exception caught.")
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))


def removeByUrl(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    try:
        if (context.args.__len__() == 0) or (not isinstance(context.args[0], str)):
            update.message.reply_text('Usage: \'/add <url>\'.')
            return

        for url in context.args:
            LocalDB.query("DELETE FROM record WHERE chat_id=? AND url=?", (chat_id, url))
        update.message.reply_text('Website removed form the list.')
    except Error as e:
        update.message.reply_text("Unexpected Error with the database.")
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))
    except Exception as e:
        update.message.reply_text("Unusual exception caught.")
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))


def showUrl(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    try:
        if LocalDB.query("SELECT COUNT(*) FROM record WHERE chat_id=?", (chat_id,)) == 0:
            update.message.reply_text("No website saved.")
        query_result = LocalDB.query("SELECT url FROM record WHERE chat_id=?", (chat_id,))
        out = 'Website saved:'
        i = 1
        for row in query_result[0]:
            out += '\n\t\t{}) \'{}\'.'.format(i, row[0])
            i += 1
        update.message.reply_text(out)
    except Error as e:
        update.message.reply_text("Unexpected Error with the database.")
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))
    except Exception as e:
        update.message.reply_text("Unusual exception caught.")
        print("Exception type:\'{}\'\nDescription:\'{}\'".format(type(e), e))


def start(update: Update, context: CallbackContext):
    update.message.reply_text(      "-------------------------------------------------------------\n\n" +
                                    "                            Welcome!                     \n\n" +
                                    "This is the Web Check bot, is a bot\n " +
                                    "designed to periodically check a list\n" +
                                    "a website and notify the user about\n" +
                                    "any changes.\n" +
                                    "Yuo can learn more here:\n" +
                                    "https://github.com/MattiaColombari/WebCheck\n\n" +
                                    "-------------------------------------------------------------")


def nonCommand(update: Update, context: CallbackContext):
    update.message.reply_text("Unexpected command, use /help to se all the command available.")


def error(update: Update, context: CallbackContext):
    print(context.error)
    # update.message.reply_text('Error, Caused error {}'.format(context.error))


# Start the job queue once the bot was started
def restartBot(updater):
    try:
        query_result = LocalDB.query('SELECT id FROM chat')
        for row in query_result[0]:
            chat_id = row[0]
            current_jobs = updater.job_queue.get_jobs_by_name(str(chat_id))
            if not current_jobs:
                updater.job_queue.run_repeating(checking, TIME_BETWEEN_CHEK, context=chat_id, name=str(chat_id))
    except Exception as e:
        print('Bot failed to launch do to this exception:\n{}'.format(e))


def main():
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("showUrl", showUrl))
    dp.add_handler(CommandHandler("removeByUrl", removeByUrl))

    # on non command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, nonCommand))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    restartBot(updater)

    # Blocks until one of the signals are received and stops the updater.
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
