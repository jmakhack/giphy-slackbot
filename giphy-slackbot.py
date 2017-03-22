from slackclient import SlackClient
import json
import os.path
import sys.exit
import time
import urllib2

if os.path.isfile("config.json"):
    with open("config.json") as config:
        data = json.load(config)
        if data["token"]:
            slack_client = SlackClient(data["token"])
        else:
            sys.exit("Setup failed. Token not found in configuration file.")
else:
    sys.exit("Setup failed. Configuration file missing.")

def handle_command(channel, key, tag):
    url = "http://api.giphy.com/v1/gifs/random?api_key="
    url += "dc6zaTOxFJmzC" if not key else key
    if tag: url += "&tag=" + tag
    api = json.loads(urllib2.urlopen(url).read())
    slack_client.api_call("chat.postMessage", channel=channel, text=api['data']['url'], as_user=True)

def is_trigger_in_text(text, triggers):
    if 'http://giphy.com/gifs/' in text:
        return False
    for trigger in triggers:
        if trigger in text.toLowerCase():
            return True
    return False

def parse_slack_output(slack_rtm_output, triggers):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and is_trigger_in_text(output['text'], triggers):
                return output['channel']
    return None

if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("giphy-slackbot connected and running! It's giphy meme time! ;)")
        while os.path.isfile("config.json"):
            with open("config.json") as config:
                data = json.load(config)
                channel = parse_slack_output(slack_client.rtm_read(), data["triggers"])
                if channel:
                    handle_command(channel, data["key"], data["tag"])
            time.sleep(1)
        sys.exit("Error loading configuration file.")
    else:
        sys.exit("Connection failed. Invalid Slack token?")
