import os
import logging
from dotenv import load_dotenv

# Import the core RAG logic
from rag_logic import rag_query

# Import the Telegram bot library
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Load environment variables from a .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Set up logging for a clean output
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dictionary to store conversation history for each user.
# The keys will be the chat IDs. This simulates session memory for Telegram.
user_history = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    await update.message.reply_text("Hello! I'm TechCorp's AI assistant. Ask me a question about our documents.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user text messages and calls the RAG pipeline."""
    user_query = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"User query from chat_id {chat_id}: {user_query}")

    # Get the history for the current chat_id, or an empty list if it doesn't exist.
    history = user_history.get(chat_id, [])

    # Call the shared RAG function to get the response
    response = rag_query(user_query, history) 

    # Update the in-memory history
    history.append({"user": user_query, "ai": response})
    user_history[chat_id] = history

    # Send the response back to the user
    await update.message.reply_text(response)
    
async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /clear command to reset a user's conversation history."""
    chat_id = update.effective_chat.id
    if chat_id in user_history:
        del user_history[chat_id]
        await update.message.reply_text("Your conversation history has been cleared.")
    else:
        await update.message.reply_text("There is no history to clear.")

def main() -> None:
    """Starts the Telegram bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in .env file. Please add it.")
        return

    # Create the Application and pass your bot's token.
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers for /start and /clear
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear_history))

    # Add a message handler for all text messages that are not commands
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
