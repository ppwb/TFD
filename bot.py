#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 12:03:00 2018
@author: mparvin
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import configparser
from os import path
from os import makedirs

config = configparser.ConfigParser()
config.read('config')
### Get admin chat_id from config file
### For more security replies only send to admin chat_id
adminCID  = config['SecretConfig']['adminCID']
videoPath = config['SecretConfig']['videoDirectoryPath']
photoPath = config['SecretConfig']['photoDirectoryPath']
musicPath = config['SecretConfig']['musicDirectoryPath']
if not path.isdir(videoPath):
	makedirs(videoPath)
if not path.isdir(photoPath):
	makedirs(photoPath)
if not path.isdir(musicPath):
	makedirs(musicPath)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello, This bot is private!!!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('This bot download any file, video or images that recieved.\n To use this bot, send file or forward the post!')


def isValidUser(chat_id):
	usersChatID = config['SecretConfig']['usersChatID'].split(',')
	if chat_id not in usersChatID:
		return True
	else:
		return False


def allCheck(bot, update):
	chat_id = update.message.chat_id
	if not isValidUser(chat_id):
		errorMessage = """You cannot use this bot, this is a private bot!!!!\n\n
						To use this bot contact @{}""".format(config['SecretConfig']['supportUser'])
		update.message.reply_text(errorMessage)
	else:
	    update.message.reply_text("Downloading file, Please wait")

	    print(update.message)
	    return
	    if update.message.audio:
	    	fileID = update.message.audio.file_id
    		fileExtension = '.mp3'
	    	storeFolder = musicPath
	    elif update.message.video:
	    	fileID = update.message.video.file_id
    		fileExtension = '.mp4'
	    	storeFolder = videoPath
	    elif update.message.photo:
	    	fileID = update.message.photo[-1].file_id
	    	fileExtension = '.jpg'
	    	storeFolder = photoPath
	    else:
	    	update.message.reply_text("Only send Video or Photo or Audio ;)")
	    	return

	    filePath = storeFolder + str(int(time.time())) + fileExtension
    	dlFile = bot.getFile(fileID)
    	dlFile.download(filePath)
	    


def error(bot, update, error):
    """Log Errors caused by Updates."""
    errorMessage = """Update {} caused error {}""".format(update, error)
    ### Logging errors
    logger.warning()
    ### Send error to admin
    bot.sendMessage(text=errorMessage, chat_id=adminCID)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config['SecretConfig']['Token'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - Download files
    dp.add_handler(MessageHandler([Filters.photo, Filters.video, Filters.audio], allCheck))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
	main() 