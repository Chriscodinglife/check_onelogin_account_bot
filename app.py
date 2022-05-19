#!/usr/bin/env python3

import os
import re
from urllib import response
import onelogin_bot
from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
slack_app_token=os.environ.get("APP_LEVEL_TOKEN")

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

@app.command("/check")
def repeat_text(ack, respond, command):
      
    '''This function will wait for a slash command of /check with an argument as a username. '''
    # Acknowledge command request
    ack()
    user_account = command['text']
    match = r"([\w.]+)(@greenhouse\.io)"
    result = re.search(match, user_account)
    
    try:
      if result.group(2) == "@greenhouse.io":
        with onelogin_bot.sync_playwright() as playwright:
          is_active_response = onelogin_bot.run(playwright, one_login_account=f"{command['text']}")
          respond(is_active_response)
      else:
        respond(f"{user_account} is not a proper user account, or was inputted incorrectly. Please try again.")
    except:
      respond("An error has occured please try again.")
    
      
    
# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))