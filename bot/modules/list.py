from telegram.ext import CommandHandler

from bot import LOGGER, dispatcher
from bot.helper.drive_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage


def list_drive(update, context):
    LOGGER.info('User: {} [{}]'.format(
        update.message.from_user.first_name, update.message.from_user.id))
    try:
        search = update.message.text.split(' ', maxsplit=1)[1]
    except IndexError:
        sendMessage('Send a search query along with command',
                    context.bot, update)
        LOGGER.info("Query: None")
        return
    reply = sendMessage('Searching...', context.bot, update)
    LOGGER.info(f"Query: {search}")
    google_drive = GoogleDriveHelper(None)
    try:
        msg, button = google_drive.drive_list(search)
    except Exception as e:
        msg, button = "There was an error", None
        LOGGER.exception(e)
    editMessage(msg, reply, button)


list_handler = CommandHandler(BotCommands.ListCommand, list_drive,
                              filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(list_handler)
