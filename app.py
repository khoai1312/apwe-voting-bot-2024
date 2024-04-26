from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from collections import defaultdict

# Dictionary to store polls and their responses
polls = defaultdict(lambda: defaultdict(int))


# Display a welcome message
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to APWE Poll Bot! Use /newpoll <question> <option 1> <option 2> to create a new poll.")


# Create a new poll with question and options
def new_poll(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    message = update.message.text
    questionAndOptions = message.split("/newpoll ", 1)[1].split("?")[1]
    options = [option.strip() for option in questionAndOptions.split(',')]
    polls[chat_id]["question"] = questionAndOptions[0:questionAndOptions.find("?") + 1]
    polls[chat_id]["options"] = {option: 0 for option in options}
    context.bot.send_message(chat_id=chat_id, text="Poll created successfully!")


# Allow users to vote for an option in the current poll
def vote(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    message = update.message.text
    option = message.split("/vote ", 1)[1]
    if option in polls[chat_id]["options"]:
        polls[chat_id]["options"][option] += 1
        update.message.reply_text("Your vote has been counted!")
    else:
        update.message.reply_text("Invalid option!")


# Show result of the current poll
def view_results(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if "question" in polls[chat_id]:
        question = polls[chat_id]["question"]
        options = polls[chat_id]["options"]
        results = "\n".join([f"{option}: {votes}" for option, votes in options.items()])
        update.message.reply_text(f"<b>{question}</b>\n\n{results}", parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text("No poll created yet.")


def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Sorry, I didn't understand that command.")


def main() -> None:
    updater = Updater("7012006521:AAGmswXXX_kTubQ7CowIzM5JJvMYg34_znU")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("newpoll", new_poll))
    dispatcher.add_handler(CommandHandler("viewresults", view_results))
    dispatcher.add_handler(CommandHandler("vote", vote))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
