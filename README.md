# Telegram Defender

<img src="./images/telegram_defender_wide.png" width="100%" height="">

Telegram Defender can be added to any channel or group. It will automatically scan links that get posted for malware, and will remove them if detected. It can also tell you more about the media source (look in settings for more information). Feel free to submit any ideas or code contributions!

<img src="./images/telegram-defender-example.gif" width="100%" height="">


<img src="./images/td_hrule.png" width="100%" height="">

## Set up a secure server
The fastest way to set up Telegram Defender is through [Digital Ocean](https://www.digitalocean.com/).
> Everything was built and tested on Ubuntu 18

<img src="./images/td_hrule.png" width="100%" height="">

#### Set up your bot with the Botfather
<img src="./images/botfather.jpg" width="25%" height="">

1. In Telegram, start a conversation with the @botfather.
> More information can be found [here](https://core.telegram.org/bots).

2. Enter `/newbot`
3. Name your bot

If succesful, it will look something like this

```
Done! Congratulations on your new bot. You will find it at t.me/teledefconbot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
98379:AAHaFDqDrnW6lgzXxLftk6cnU1733yaYhP9yyUQ (*note: this is a fake key)
Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
```

### Create an Avira URL Safety Cloud scanner:
1. Go here: `https://aws.amazon.com/marketplace/pp/Avira-Avira-URL-Safety-Cloud/B079C6B7LL`
2. You'll need to subscribe to this service via AWS.
3. Once that's complete, go here `https://developer.protection-services.avira.com/apis`
    - You should see: **Avira URL Safety Cloud** Entrypoint: `https://nihh1mvy78.execute-api.eu-central-1.amazonaws.com/prod/url-query`
    Save this URL for later.
    - Click `show api key` to get your api key. Save that for later too.


### AllSides Media Bias Ratings
1. AllSides Media Bias rankings are not publicly available. These bias ratings are [publicly available at AllSides.com](https://www.allsides.com/media-bias/media-bias-ratings). To request this data as CSV or JSON [contact them](https://www.allsides.com/contact).

    - In exchange for access to their data, we have include a module that allows them to know that a user came to their site via the Telegram Defender bot. It is not a cookie, will not track you, or disclose anything else. You may notice the following code at the end of linkes that take you to [AllSides](https://www.allsides.com/)  

        `?utm_source=Live+Partner+Network&utm_medium=Media+Bias+Ratings&utm_campaign=Telegram+Defender`  

    - More information can be found in their [privacy policy which you can read by clicking here](https://www.allsides.com/privacy-policy)
    - TLDR; [AllSides.com](https://www.allsides.com/) actually has a great Privacy Policy that respects your rights and appears to be fully compliant with best practices and regulations.


<img src="./images/td_hrule.png" width="100%" height="">

## Bot Settings
There are two main JSON files that contain your settings and tokens to deploy the bot.

### Settings.json
This contains some of the text responses for your bot. It must be in the **same** folders as `bot.py`

- **"messages:"** - array of possible messages
- **"welcome:"** Message that bot sends when someone joins chat
- **"help:"** Message that bot sends when someone sends '/help' command
- **"start:"** Message taht bot sends when someone sends '/start' command to start bot in private chat
- **"malware_detected:"** Message that bot sends when found malicious link
- **"allsides_no_stats:"** Message that bot sends when link was found, but website was not in the list or was not rated. 
    - **{url}** - parameter where found url is listed
- **"allsides_found:"** - Message that bot sends when link was found and listed. 
    - **{side}** - parameter that is changes depending on websites side, 
    - **{allsides_url}** - allsides URL of listed website
- **"something_wrong- "** - If any unknown error appears bot will send this message to the chat.
- **"images_base_dir"** - base directory for images. If images listed in the same directory that bot.py is just leave blank.



### Token.json
This file contains the API tokens for TelegramBotAPI and Avira URL Safety Cloud API. 
**WARNING: NEVER SHARE YOUR TOKENS!**

# Deployment
> Here are steps to get your own private Telegram Defender online

## Configure your bot on Telegram

 1. Create a new Channel.
    - Give it a name
    - Public vs Private
    - Admins
    - Add "TelegramDefender" bot

2. To set the user pic, start a chat with @Botfather
    - Enter `/setuserpic`
    - Select the name of your bot
    - Send the photo


## Deploying your bot to a server
3. Create a new server that's running Ubuntu 18.04.3 LTS
    - run `sudo add-apt-repository ppa:deadsnakes/ppa`
    - run `sudo apt-get update`
    - run `sudo apt-get install`
    - run `sudo apt-get install python3-setuptools`
    - run `sudo apt-get install python3-pip`
    - run `sudo apt-get install python3.8`
    - run `sudo apt install python3.8-venv python3.8-dev`


4. Go to your root directory
    - `git clone https://github.com/yalefox/telegram-defender.git`
    

5. Set Python 3.8 as default
    - Go to your root folder with `cd ~`
    - Create a new directory with `mkdir venvs`
    - Open it with `cd venvs`
    - Run `python3.8 -m venv tdenv`
    - Run `source tdenv/bin/activate`


6. Install dependencies
    - enter `cd ~/telegram-defender/bot`
    - run `pip3 install -r requirements.txt`
        - you may see this warning, but it's okay to ignore it. 
```
WARNING: You are using pip version 19.2.3, however version 19.3.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```

7. Update your tokens
    - enter `nano ~/telegram-defender/bot/json/token.json` to create a new file
    - Replace the API keys below with the ones you got earlier. The URL should be the same. 
    - Press `Ctrl + X` to save and exit.

```
{
    "bot_token": "XXXXXXXX",
    "avira_token": "XXXXXXXX",
    "avira_url": "https://nihh1mvy78.execute-api.eu-central-1.amazonaws.com/prod/url-query"
}
```


8. Now we need to update the service
    - run `apt-get install systemd`
    > This will restart the bot if it goes down.
    - enter `cd /etc/systemd/system`
    - enter `nano bot.service`

9. Copy the following code and enter `Ctrl + X` to exit and save.
 
```
[Unit]
Description=TelegramDefender
After=syslog.target
After=network.target
[Service]
Type=simple
User=root
WorkingDirectory=/root/telegram-defender/bot
ExecStart=/root/venvs/tdenv/bin/python /root/telegram-defender/bot/bot.py
RestartSec=10
Restart=always
[Install]
WantedBy=multi-user.target
```

10. Run this 4 command to deploy the bot.
    - run `systemctl daemon-reload` 
    - run `systemctl enable bot`
    - run `systemctl start bot`
    - run `systemctl status bot`

If succesful, you should see something that looks like this:
```
● bot.service - TelegramDefender
        Loaded: loaded (/etc/systemd/system/bot.service; enabled; vendor preset: enabled)
        Active: active (running) since Wed 2019-09-11 14:18:54 UTC; 3s ago
    Main PID: 8345 (python3)
        Tasks: 4 (limit: 1152)
        CGroup: /system.slice/bot.service
                └─8345 /usr/bin/python3 /root/telegram-defender/bot/bot.py
```

That's it! You're ready to go!

<img src="./images/td_hrule.png" width="100%" height="">

# Add Telegram Defender to a Channel
> Note that in a channel, it will not answer to /start or /help commands.

1. Add your bot to a channel.
2. Set it as admin
    - In a new group ➜ info ➜ administators ➜admin  
    
    
# Add Telegram Defender to a Group
> In a group (or private chat), the bot will respond to anyone

1. Add your bot (or ours, @tdef_bot)
2. Edit gorup settings ➜ Administrators ➜ Add Admin ➜ Telegram Defender
2. Type `/start` or `/help` in the chat


<img src="./images/td_hrule.png" width="100%" height="">


### Attributions

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img style="margin-top: 5px; margin-bottom: 5px;" alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />
<p><a xmlns:dct="http://purl.org/dc/terms/" href="https://www.allsides.com/media-bias/media-bias-ratings" rel="dct:source"><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Dataset" property="dct:title" rel="dct:type">AllSides Media Bias Ratings</span></a> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://www.allsides.com/unbiased-balanced-news" property="cc:attributionName" rel="cc:attributionURL">AllSides.com</a> are licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>. You may use this data for research or noncommercial purposes provided you include this attribution.</p>
