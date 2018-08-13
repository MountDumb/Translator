import time
from decouple import config
from slackclient import SlackClient
import helper_utils


# region Functions
def parse_bot_commands(slack_events):
    # Check if the events are of type 'message' and that it's not from a bot,
    # since bots have subtypes. This should probably be reworked.
    for event in slack_events:
        if event['type'] == 'message' and "subtype" not in event:
            print(event)
            return event['text'], event["channel"]
    return None, None


def handle_message(message, channel):
    response, outputdict = '', {}
    message = str.lower(message)

    for word in keywords:
        if word in message:
            outputdict[word] = keywords[word]

    if outputdict:
        for word in outputdict.keys():
            response += '{} means: {} \r\n'.format(word, keywords[word])

    if response:
        print(response)
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response
        )


# endregion


# region Script Execution

# Constants
RTM_READ_DELAY = 1  # read from the RTM API every second

# variables
slack_client = SlackClient(config('TOKEN'))
keywords = helper_utils.load_json_to_dict('keywords.json')  # dictionary of known '1337' keywords
bot_id = None  # bot's user ID in Slack: value is assigned after the bot starts up

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        bot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_message(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed.")
# endregion
