import subprocess

from telegram.ext import CommandHandler

from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage


def shell(update, context):
    LOGGER.info('User: {} [{}]'.format(
        update.message.from_user.first_name, update.message.from_user.id))
    message = update.effective_message
    cmd = message.text.split(' ', 1)
    if len(cmd) == 1:
        LOGGER.info("Shell: None")
        return sendMessage('Send a command to execute', context.bot, update)
    cmd = cmd[1]
    process = subprocess.run(cmd, capture_output=True, shell=True)
    reply = ''
    stderr = process.stderr.decode('utf-8')
    stdout = process.stdout.decode('utf-8')
    if len(stdout) != 0:
        reply += f"<b>Stdout</b>\n<code>{stdout}</code>\n"
        LOGGER.info(f"Shell: {cmd}")
    if len(stderr) != 0:
        reply += f"<b>Stderr</b>\n<code>{stderr}</code>\n"
        LOGGER.error(f"Shell: {cmd}")
    if len(reply) > 3000:
        with open('shell_output.txt', 'w') as file:
            file.write(reply)
        with open('shell_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        sendMessage(reply, context.bot, update)
    else:
        sendMessage('No Reply', context.bot, update)


shell_handler = CommandHandler(BotCommands.ShellCommand, shell,
                               filters=CustomFilters.owner_filter, run_async=True)
dispatcher.add_handler(shell_handler)
