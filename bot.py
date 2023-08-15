import datetime
import telegram
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ForceReply, KeyboardButton

button = KeyboardButton("/menu")

force_reply = ForceReply(input_field_placeholder="Text", selective=True, single_use=True, button=button)

INPUT_TEXT = 0
ACCOUNT_INFO, READY, ID, PASSWORD, SERVER = range(5)

token = '6508467896:AAGegUxpDlipA_oXFGHq4Cah3vnqbIC8POI' 
channel_id = '@bluefinfx'
owner_chat_id = 1873871518 # your user id
owner_pin = '786110' # set a pin code 

bot = telegram.Bot(token=token)

def start(update, context):
  chat_id = update.message.chat_id
  text = 'Connect to channel' 
  button = telegram.InlineKeyboardButton(text, url='https://t.me/bluefinfx')
  keyboard = [[button]]
  reply_markup = telegram.InlineKeyboardMarkup(keyboard)
  
  context.bot.send_message(chat_id=chat_id, text='Welcome!', reply_markup=reply_markup) 

def daily_post(context):
  bot.send_message(chat_id=channel_id, text='Daily update')

def get_id(update, context):
  chat_id = update.message.chat_id
  print(chat_id)

# def get_text(update, context):
#   message = update.message.text
#   # Save to variable
#   user_message = message

# def owner_send_message(update, context):
#   keyboard = [["Text here"]] 
#   reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
#   bot.send_message(chat_id=owner_chat_id, text="Enter message", reply_markup=reply_markup)
#   bot.sendMessage(chat_id='@bluefinfx', text='Test')
#   if update.message.text:
#      message = update.message.text
#      bot.sendMessage(chat_id=channel_id, text=message)

def owner_send_message(update, context):
  keyboard = []
  reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
  update.message.reply_text("Enter message:", reply_markup=reply_markup)
  return INPUT_TEXT

def get_input_text(update, context):
  user_text = update.message.text
  bot.sendMessage(chat_id=channel_id, text=user_text)
  return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('sendmessage', owner_send_message)],
    states={
        INPUT_TEXT: [MessageHandler(Filters.text, get_input_text)]
    },
    fallbacks=[]
)

def join_team(update, context):
  chat_id = update.message.chat_id
  bot.sendMessage(chat_id = chat_id, text = "Coming Soon!\n\nWe will soon be adding skilled traders into our company and provide them with funded accounts and Bluefin Benefits.")
  
def accountmanagement(update, context):
  update.message.reply_text("Welcome to our account management service. Send READY when you are ready to begin.")
  return READY

def get_ready(update, context):
  update.message.reply_text("Please send your account ID...")  
  return ID

def get_id(update, context):
  user_id = update.message.text
  context.user_data['id'] = user_id
  update.message.reply_text("Please enter your account password...") 
  return PASSWORD
  
def get_password(update, context):
  user_password = update.message.text
  context.user_data['password'] = user_password
  update.message.reply_text("Please enter your server details:")
  return SERVER

def get_server(update, context):
  newmember_chat_id = update.message.chat_id
  user_server = update.message.text
  user_id = context.user_data['id']
  user_password = context.user_data['password']
  link = f"https://t.me/{newmember_chat_id}"

  # Send info to owner
  context.bot.send_message(owner_chat_id, f"New client information\n\nClient ID: {link}\nID: {user_id}\nPassword: {user_password}\nServer: {user_server}")
  
  update.message.reply_text("Thank you for the information! Our team will contact you soon.")

  return ConversationHandler.END

# Conversation handler
conv_handler_accmanage = ConversationHandler(
   entry_points=[CommandHandler('accountmanagement', accountmanagement)],

   states={
       READY: [MessageHandler(Filters.regex(r'(?i)READY'), get_ready)],
       ID: [MessageHandler(Filters.text, get_id)],
       PASSWORD: [MessageHandler(Filters.text, get_password)],
       SERVER: [MessageHandler(Filters.text, get_server)],
   },

   fallbacks=[]
)


updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('getid', get_id))
#dispatcher.add_handler(CommandHandler("sendmessage", owner_send_message))
dispatcher.add_handler(conv_handler) #sendmessage handler
dispatcher.add_handler(CommandHandler('jointeam', join_team))
dispatcher.add_handler(conv_handler_accmanage) #accountmanagement handler


# Trigger daily_post regularly 
job_queue = updater.job_queue
job_queue.run_daily(daily_post, time=datetime.time(hour=8)) 

updater.start_polling()