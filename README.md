# creepertext-bot
  Self-written Telegram bot, which parses creepy-pastas from Mrakopedia to Telegraph and stores it in PostrgeSQL db. 
  
  Bot takes Telegram, Telegraph and PostgreSQL url from env vars, so to launch bot you need to add DATABASE_URL, TELEGRAM_TOKEN 
  and TELEGRAPH_TOKEN to env vars like this: <br>
![Снимок экрана 2022-08-05 в 2 36 55](https://user-images.githubusercontent.com/52624425/182964363-2bc11b0d-331d-4f7b-ae76-66e0f741efb6.png)

Available bot commands:
- /random - send random pasta from db
- /top - send top ten pastas
- /count - send total number of pastas

Architecture of bot directed to simplification of command adding using decorators 
