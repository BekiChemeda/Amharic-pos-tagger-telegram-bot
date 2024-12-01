
# Hayyuu Amharic POS Tagger Bot

Hayyuu is a Telegram bot designed to perform Part-of-Speech (POS) tagging for Amharic and other Ethiopian languages using a Conditional Random Fields (CRF) model.


## Features

- **POS Tagging**: Analyzes Amharic sentences and tags each word with its part of speech.
- **Custom Tokenizer**: Specifically designed for Amharic, handling special characters and punctuation.
- **Telegram Bot Commands**:
  - `/start`: Start the bot and get a welcome message.
  - `/about`: Learn about the bot and its development.
  - `/help`: Get a guide on how to use the bot.
  - `/info`: Understand more about NLP and POS tagging.
  - `/teach`: (Coming soon) Help the bot learn new data.


## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Hayyuu-POS-Bot.git
   cd Hayyuu-POS-Bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your channel**:
   - Update the channel username in the code:
     - Open `bot.py` and replace `@Bright_Codes` with your own Telegram channel username.
   - Make the bot an **administrator** in your channel:
     - Go to your Telegram channel settings and add your bot as an admin. Ensure it has the necessary permissions to check user membership.

4. **Set your API token**:
   - Replace the placeholder `API_TOKEN` in `bot.py` with your Telegram bot API token.

5. **Run the bot**:
   ```bash
   python bot.py
   ```


## How to Use

1. **Start the bot**:
   - Open Telegram and start a chat with your bot.
   - Send `/start` to initialize.

2. **Interact with the bot**:
   - Use commands like `/help`, `/about`, and `/info`.
   - Send an Amharic sentence to see POS tagging in action.


## Requirements

Ensure you have Python 3.8 or higher installed. Install the dependencies from `requirements.txt` to set up the environment.


## Model Information

The bot uses a CRF model trained on Amharic data. The model file `tuned_crf_pos_tagger.pkl` is included in the repository and pre-loaded by the bot. If you want to retrain or update the model, see the training script provided.


## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.


## License

This project is licensed under the MIT License. See the LICENSE file for details.
