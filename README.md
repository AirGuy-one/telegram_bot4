# Quiz Bot
## A Telegram and Vkontakte quiz bot.

### Features
* /start command to start the game
* "New question" button to get a new question
* "Give up" button to skip a question
* "My score" button to display your score
### Installation

You can install the necessary dependencies using pip:

```
pip install requirements.txt
```

You will also need to create a .env file in the root directory of your project and insert your Telegram and Vkontakte bot tokens:

```
TG_BOT_TOKEN=thisisyourtgtoken
VK_BOT_TOKEN=thisisyourvktoken
```

Afterward, you need to create the 'questions_data' folder and insert the '1vs1200.txt' file here, which will store the data about questions and answers according to the example file:

```
Вопрос 1:
С одним советским туристом в Марселе произошел такой случай. Спустившись
из своего номера на первый этаж, он вспомнил, что забыл закрутить кран в
ванной. Когда он поднялся, вода уже затопила комнату. Он вызвал
горничную, та попросила его обождать внизу. В страхе он ожидал расплаты
за свою оплошность. Но администрация его не ругала, а, напротив,
извинилась сама перед ним. За что?

Ответ:
За то, что не объяснила ему правила пользования кранами.

Автор:
Максим Поташев


Вопрос 2:
В своем первоначально узком значении это слово произошло от французского
глагола, означающего "бить". Сейчас же оно может означать любое
объединение в систему нескольких однотипных элементов. Назовите это
слово.

Ответ:
Батарея (от battre).

Источник:
СЭС

Автор:
Вадим Карлинский
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
