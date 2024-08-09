from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters
from datetime import datetime
import pytz

# Replace 'YOUR_TOKEN_HERE' with your bot's token
TOKEN = '6569505220:AAGtDNRAbGOVD9rdB_EA2_HNsPbaSwA5m1g'

# Dictionary to keep track of attendance per chat
attendance_data = {}

# Timezone for IST
IST = pytz.timezone('Asia/Kolkata')

# Command to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in attendance_data:
        attendance_data[chat_id] = {
            'present_members': {},
            'absent_members': {}
        }
    await update.message.reply_text("Hello! Use /list to get the list of present and absent members.")

# Function to handle messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.lower()
    user = update.message.from_user.username or update.message.from_user.first_name
    chat_id = update.effective_chat.id

    if chat_id not in attendance_data:
        attendance_data[chat_id] = {
            'present_members': {},
            'absent_members': {}
        }

    now = datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')
    
    if 'boost' in text:
        attendance_data[chat_id]['present_members'][user] = now
        attendance_data[chat_id]['absent_members'].pop(user, None)
        await update.message.reply_text(f"{user} marked as present at {now}.")

# Command to list present and absent members
async def list_attendance(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    if chat_id not in attendance_data:
        await update.message.reply_text("No attendance data found for this group.")
        return

    present_list = "\n".join(f"{user} at {time}" for user, time in attendance_data[chat_id]['present_members'].items()) if attendance_data[chat_id]['present_members'] else "No one is marked present."
    absent_list = "\n".join(f"{user} at {time}" for user, time in attendance_data[chat_id]['absent_members'].items()) if attendance_data[chat_id]['absent_members'] else "No one is marked absent."

    response = f"Present Members:\n{present_list}\n\nAbsent Members:\n{absent_list}"
    await update.message.reply_text(response)

# Command to reset attendance data
async def reset_attendance(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Fetch list of chat administrators
    try:
        chat_administrators = await context.bot.get_chat_administrators(chat_id)
    except Exception as e:
        await update.message.reply_text("Failed to retrieve administrators. Please try again later.")
        return

    # Check if the user issuing the command is an admin
    is_admin = any(admin.user.id == user_id for admin in chat_administrators)
    
    if not is_admin:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    if chat_id not in attendance_data:
        await update.message.reply_text("No attendance data found for this group.")
        return

    attendance_data[chat_id]['present_members'].clear()
    attendance_data[chat_id]['absent_members'].clear()
    await update.message.reply_text("Attendance data has been reset.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("list", list_attendance))
    application.add_handler(CommandHandler("reset", reset_attendance))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
