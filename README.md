### SendBird Slash Command Bot Example
This is a a basic chat bot written to integration with SendBird's Bot Interface  (https://docs.sendbird.com/platform/bot_interface)
### What do this bot do?
The bot will respond depending on the slash command which user requested in a group channel.
### What functions did this application use from the Bot Interface API?
- [Receiving messages from the channel](https://docs.sendbird.com/platform/bot_interface#2_bot_interface)
- [Sending messages to the channel](https://docs.sendbird.com/platform/bot_interface#3_send_message_from_bot)
### Tutorial / How to Run
Refer to the [Slash Command Bot Tutorial: InfoBot](https://docs.google.com/document/d/1SkNtrdWeiPTWBXNZOB5dHMpfbXPIUpV6C0PHLiYn_2g/edit?usp=sharing). This tutorial covers deploying this bot to DigitalOcean so that it can integrate with SendBird's Bot Interface and respond to slash command requests.


### What needs to be changed.
In app.py the following changes are needed:
 - Change **host** to match the SendBird endpoint for your application (Found in the SendBird Dashboard).
 - Change **api_token** to match your SendBird Application's API Token.
 - Change **bot_id** to match your SendBird Application's Bot ID that you will create in the tutorial.
 
## Code Overview 

### app.py
This file contains the flask and server code
### config.py
Configuration options including the api_token, SendBird app endpoint to target and bot_id.
### routes.py
Routing the bot event/webhook received from SendBird to the correct action from the bot. In this case there is only one action which is to respond to a ping message.
### message_functions.py
Contains the logic to actually send a message back to SendBird. 
### How To Deploy Flask Applications with Gunicorn and Nginx on Ubuntu 18.04
Create a virtual environment to store your Flask project’s Python requirements by typing:

#### Installation
<code>python3.6 -m venv myprojectenv</code>

Activate env source env/bin/activate

<code>source env/bin/activate</code>

Install required libraries

<code>pip install -r requirements.txt</code>

Install Flask and Gunicorn:

<code>pip install gunicorn flask</code>

## Configuring Gunicorn

Create a unit file ending in .service within the /etc/systemd/system directory to begin:

```
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=bek
Group=www-data
WorkingDirectory=/home/bek/myproject
Environment="PATH=/home/bek/myproject/env/bin"
ExecStart=/home/bek/myproject/env/bin/gunicorn --workers 3 --bind unix:app.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

We can now start the Gunicorn service we created and enable it so that it starts at boot:

```
sudo systemctl start myproject
sudo systemctl enable myproject
```


