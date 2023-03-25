# Quiz Bot
## A Telegram and Vkontakte quiz bot.

### Features
* /start command to start the game
* "New question" button to get a new question
* "Give up" button to skip a question
* "My score" button to display your score
### Installation
To use this bot, you will need to install the following dependencies:

* pyTelegramBotAPI==4.10.0
* redis[hiredis]==4.5.3

You can install them using pip:

```
pip install pyTelegramBotAPI==4.10.0 redis[hiredis]==4.5.3
```

You will also need to create a .env file in the root directory of your project and insert your Telegram and Vkontakte bot tokens:

```
TG_BOT_TOKEN=thisisyourtgtoken
VK_BOT_TOKEN=thisisyourvktoken
```

### Usage

To start the telegram bot, simply run the bot.py file:
```python tg_bot.py```

To start the vk bot, simply run the bot.py file:
```python vk_bot.py```

Once the bot is running, you can use the following commands and buttons:

* /start - start the game
* "New question" - get a new question
* "Give up" - skip a question
* "My score" - display your score
