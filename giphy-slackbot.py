import os
import json
import time
import urllib2
from slackclient import SlackClient

slack_client = SlackClient('''[ INSERT SLACKBOT TOKEN HERE ]''')

def handle_command(channel):
    api = json.loads(urllib2.urlopen("http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=spongebob").read()) #REPLACE WITH GIPHY API PRODUCTION KEY IF NEEDED
    slack_client.api_call("chat.postMessage", channel=channel, text=api['data']['url'], as_user=True)

def is_trigger_in_text(text):
    if 'http://giphy.com/gifs/' in text:
        return False
    triggers = ('spongebob', 'squarepants', 'patrick', 'squidward') #INSERT MORE KEYWORDS HERE
    for trigger in triggers:
        if trigger in text.toLowerCase():
            return True
    return False

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and is_trigger_in_text(output['text']):
                return output['channel']
    return None

if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("SpongeBot connected and running! It's giphy meme time! ;)")
        while True:
            channel = parse_slack_output(slack_client.rtm_read())
            if channel:
                handle_command(channel)
            time.sleep(1)
    else:
        print("Connection failed. Invalid Slack token?")
