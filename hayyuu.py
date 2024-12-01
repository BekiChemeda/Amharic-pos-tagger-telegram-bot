import telebot
import re
import pickle

# Bot API token
API_TOKEN = "7745731112:AAH5-WuM8wptW-VbsDkf4WU9eBaMq5eR5L0"
bot = telebot.TeleBot(API_TOKEN)

# Load the CRF model
with open("tuned_crf_pos_tagger.pkl", "rb") as model_file:
    crf_model = pickle.load(model_file)


# Special Amharic Tokenizer
def amharic_tokenizer(text):
    amharic_punctuation = "፥፤፡።፣!?፨፠።፡፣፤"
    tokens = re.findall(rf'[\w]+|[{amharic_punctuation}]', text)
    return tokens


# Define feature extraction functions
def word_features(sent, i):
    word = sent[i]

    prevword = sent[i - 1] if i > 0 else '<START>'
    prev2word = sent[i - 2] if i > 1 else '<START>'
    nextword = sent[i + 1] if i < len(sent) - 1 else '<END>'

    return {
        'word': word,
        'prevword': prevword,
        'nextword': nextword,
        'prev2word': prev2word
    }


def sent2features(sent):
    return [word_features(sent, i) for i in range(len(sent))]




# Check if user has joined the channel
def is_user_in_channel(user_id):
    try:
        member_status = bot.get_chat_member("@Bright_Codes", user_id)
        return member_status.status in ["member", "administrator", "creator"]
    except:
        return False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not is_user_in_channel(message.from_user.id):
        bot.reply_to(message, "Please join @Bright_Codes to use this bot. when you're done send /start again.")
        return
    bot.reply_to(message,
                 """Welcome to Hayyuu Amharic POS Tagger Bot! 🎉

 This bot tags parts of speech for Amharic & other Ethiopian languages using a Conditional Random Fields (CRF) model.

 📜 To get started, send an Amharic sentence, and I will tag the words with their parts of speech.

Send /help for Help Page

 Stay tuned for future updates!
 Follow @Bright_codes for more information. 🚀""")


# Handle /about command
@bot.message_handler(commands=['about'])
def send_about(message):
    if not is_user_in_channel(message.from_user.id):
        bot.reply_to(message, "Please join @Bright_Codes to use this bot.")
        return
    about_text = (
        "🤖 **Bot Name**: Hayyuu Amharic POS Tagger Bot (v1.0)\n\n"

        "Hayyuu is an Afaan Oromoo word, meaning **ምሁር** in Amharic and translating to 'scholar' or 'wise one' in English. "
        "So why did  [my developer](https://t.me/bek_i), call me Hayyuu? Well, because I’m designed to help you understand the parts of speech "
        "in Amharic words! Now, full transparency—I’m still learning, so I’m not perfect just yet. Right now, I can only help with words we use in daily life. "
        "I’m not 100% accurate, but the good news is, I’m continuously learning. 😊\n\n"

        "Do you want to help me improve? [ My developer](https://t.me/bek_i), is planning to introduce a special /teach command. "
        "Selected users will be able to guide my learning with new data. Although it’s ‘coming soon’ for now, I’m excited to get even better at helping you!\n\n"

        "📊 **Amharic Data Information**:\n\n"
        "[My Developer](https://t.me/BEK_I) fed me a lot of data to make sure I’m well-trained in Amharic! Here’s a quick summary:\n"
        "\n- **Training Set**: 67.9k unique words\n"
        "- **Validation Set**: 9,436 unique words\n"
        "- **Test Set**: 9,496 unique words\n\n"

        "Altogether, that’s a total of **86,832 unique words**! Isn’t that impressive? Try it out for yourself by sending some Amharic text!\n\n"

        "🔔 **Current Version**: v1.0\n\n"
        "To be upfront, there are a few little quirks in this version. For instance, if you send me a message entirely in English, I’ll remind you to use GEEZ letters, "
        "but if you mix English with Amharic, I might try tagging everything—even the English! Let’s just say, I’ll do my best, but I’m still a work in progress when it comes to mixed languages. 😉 "
        "you know why did I tell you this? because I don't want you struggle with mixed language datas."
    )

    if len(about_text) > 4000:
        bot.reply_to(message, "📜 Response is too long! Please try breaking down your question.")
    else:
        bot.reply_to(message, about_text, parse_mode="Markdown", disable_web_page_preview=True)


# Handle /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    if not is_user_in_channel(message.from_user.id):
        bot.reply_to(message, "Please join @Bright_Codes to use this bot.")
        return
    help_text = (
        "🆘 Welcome to <b> Hayyuu POS Tagger Bot </b> Help!\n\n"
        "Here’s a quick guide to help you use my features:\n\n"
        "1. /start Refresh The Bot\n"
        "2. /about Learn About Me\n"
        "3. /info Learn About NLP\n"
        "4. /help Gethelp page like this 😁\n\n"


        "Feel free to ask me anything at @BEK_I and have fun tagging!"
    )
    if len(help_text) > 4000:
        bot.reply_to(message, "📜 Response is too long! Try breaking down your question, please.")
    else:
        bot.reply_to(message, help_text, parse_mode="html")

# Handle /teach command
@bot.message_handler(commands=['teach'])
def send_teach(message):
    if not is_user_in_channel(message.from_user.id):
        bot.reply_to(message, "Please join @Bright_Codes to use this bot.")
        return
    teach_text = (
        "📚 **Teach Mode** - Coming Soon!\n\n"
        "Soon, special users will have the opportunity to help me learn by training me on new data! "
        "This will make me even smarter and better at handling more complex sentences.\n\n"

        "Stay tuned, and follow [@bek_i](https://t.me/bek_i) for updates on when the /teach command will be live!"
    )
    if len(teach_text) > 4000:
        bot.reply_to(message, "📜 Response is too long! Try breaking down your question, please.")
    else:
        bot.reply_to(message, teach_text, parse_mode="Markdown")

@bot.message_handler(commands=['info'])
def handle_info(message):
    bot.reply_to(message, """
    <b>What is NLP?</b>
    Natural Language Processing - or NLP in short - is the subfield of AI studying computers' interaction with human language. It allows machines to understand, interpret, and generate human language in useful and meaningful ways. This is what allows us to have AI that speaks with us, reads to us, and even writes like us.


    <b>Our Vision</b>
    If it is God's will, soon you will see me, Hayyuu AI, talking to you like GPT, Gemini, and other high-end models. It's our dream to present solutions that enable people to communicate with technology in their mother tongues, thereby reducing gaps in communication and knowledge.

    <b>POS Tagging: The Very First Step</b>
    Part of that journey to more advanced models of AI begins with what is called POS, or Part of Speech, tagging. This is a very important part in the development of the AI understanding the structure of sentences—what makes up a sentence: nouns, verbs, adjectives, and so on and so forth. First small yet important step toward building large powerful AI models

    <b>About CRF and Our Tagging Focus</b>
    The system I use in our POS tagging is called CRF, or Conditional Random Fields—a statistical model which helps predict the most likely sequence of tags for words in a sentence. In tagging, I am mostly concerned with the two previous and two next words since this gives a clearer view about the meaning of the word that is in context and the role it plays in the sentence. Context is everything in a language, and this technique helps me get closer to accuracy for better results.

    <b>General Approach</b>
    The strategy followed is one of continuous improvement of the system by learning from data and giving more accurate results. As we go further ahead, our AI will learn not just words, but construct responses that are in harmony with the expectations and nuances of human beings.

    <b>Stay Tuned</b>
    Follow us at @Bright_codes for more information and updates. 🙏
    Stay tuned for more as we embark on a journey to bring powerful AI to your fingertips.
    """, parse_mode="html")

# Universal handler for all user messages
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Check if the user is a member of @Bright_Codes channel
    user_status = bot.get_chat_member("@Bright_Codes", message.from_user.id).status
    if user_status == "left":
        bot.reply_to(message, "🚫 Please join @Bright_Codes to use this feature.")
        return

    sentence = message.text.strip()
    if re.search(r'[a-zA-Z]', sentence):
        bot.reply_to(message, "🚫 Please use Amharic (GEEZ) letters for tagging.")
        return

    tokens = amharic_tokenizer(sentence)
    if not tokens:
        bot.reply_to(message, "😕 I couldn't find any Amharic words to tag. Please check your input.")
        return

    # Prepare features for prediction
    features = sent2features(tokens)
    try:
        pos_tags = crf_model.predict([features])[0]
        tagged_sentence = "".join([f"{token}: {tag}\n" for token, tag in zip(tokens, pos_tags)])

        response = tagged_sentence if len(
            tagged_sentence) < 4000 else "📜 Response is too long! Try a shorter sentence."
        bot.reply_to(message, response)
    except Exception as e:
        bot.send_message(1263404935, f"Error occurred: {str(e)}")
        bot.reply_to(message, "❗ An error occurred while tagging. Please try again.")

# Run the bot
def run_bot():
    while True:
        try:
            print("Bot is running...")
            bot.infinity_polling()  # Start the bot polling loop
        except Exception as e:
            print(f"Error occurred: {e}")
            print("Reconnecting in 10 seconds...")
            time.sleep(10)  # Wait for 10 seconds before retrying

# Run the bot with automatic retries
run_bot()