import telebot
import re
import pickle
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Load CRF model
with open("tuned_crf_pos_tagger.pkl", "rb") as model_file:
    crf_model = pickle.load(model_file)


# Special Amharic Tokenizer
def amharic_tokenizer(text):
    amharic_punctuation = "፥፤፡።፣!?፨፠።፡፣፤"
    tokens = re.findall(rf'[\w]+|[{amharic_punctuation}]', text)
    return tokens


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


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 """Welcome to Hayyuu Amharic POS Tagger Bot! 🎉

This bot tags parts of speech for Amharic & other Ethiopian languages using a Conditional Random Fields (CRF) model.

📜 To get started, send an Amharic sentence.

Send /help for Help Page.
""")


@bot.message_handler(commands=['about'])
def send_about(message):
    about_text = (
        "🤖 **Bot Name**: Hayyuu Amharic POS Tagger Bot (v1.0)\n\n"

        "Hayyuu is an Afaan Oromoo word meaning ምሁር. "
        "I tag parts of speech using a CRF model.\n\n"

        "📊 **Amharic Data**:\n"
        "- Training: 67.9k words\n"
        "- Validation: 9,436 words\n"
       "- Test: 9,496 words\n\n"
        "Total: **86,832 unique words**!\n"
    )

    bot.reply_to(message, about_text, parse_mode="Markdown", disable_web_page_preview=True)


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "🆘 <b>Hayyuu POS Tagger Bot Help</b>\n\n"
        "Commands:\n"
        "1. /start - Restart bot\n"
        "2. /about - About the bot\n"
        "3. /info - NLP info\n"
        "4. /help - Help page\n"
    )

    bot.reply_to(message, help_text, parse_mode="html")


@bot.message_handler(commands=['teach'])
def send_teach(message):
    teach_text = (
        "📚 **Teach Mode** - Coming Soon!\n\n"
        "Soon, selected users will help add new training data."
    )
    bot.reply_to(message, teach_text, parse_mode="Markdown")


@bot.message_handler(commands=['info'])
def handle_info(message):
    bot.reply_to(message, """
<b>What is NLP?</b>
NLP allows computers to understand human language.

<b>POS Tagging</b>
This bot uses CRF to tag each word based on context.

<b>Vision</b>
Future versions aim to reach GPT-like abilities in Ethiopian languages.
""", parse_mode="html")


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    sentence = message.text.strip()

    if re.search(r'[a-zA-Z]', sentence):
        bot.reply_to(message, "🚫 Please use Amharic (GEEZ) letters for tagging.")
        return

    tokens = amharic_tokenizer(sentence)
    if not tokens:
        bot.reply_to(message, "😕 I couldn't find any Amharic words. Please check your input.")
        return

    features = sent2features(tokens)

    try:
        pos_tags = crf_model.predict([features])[0]
        tagged_sentence = "".join([f"{token}: {tag}\n" for token, tag in zip(tokens, pos_tags)])

        response = tagged_sentence if len(tagged_sentence) < 4000 else "📜 Response is too long!"
        bot.reply_to(message, response)

    except Exception as e:
        bot.send_message(1263404935, f"Error: {str(e)}")
        bot.reply_to(message, "❗ Error occurred while tagging.")


def run_bot():
    while True:
        try:
            print("Bot running...")
            bot.infinity_polling()
        except Exception as e:
            print(f"Error: {e}")
            print("Reconnecting in 10 seconds...")
            time.sleep(10)


run_bot()