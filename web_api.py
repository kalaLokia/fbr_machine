"""
Webhook/Api implementation

"""

from typing import Optional
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import config


def webhook_request(data: dict, wh_type: Optional[str] = ""):
    """Send the data to webhook."""

    try:
        res = requests.post(config.GOOGLE_WH, json=data)
        if res.status_code >= 400:
            print(f"{wh_type} request failed: #{res.status_code}")
    except Exception as e:
        print(f"Failed to send to {wh_type} webhook\n{e}")


def slack_api(text: str, blocks: list = None) -> None:
    """Slack client execution"""
    try:
        CLIENT = WebClient(token=config.SLACK_TOKEN)
        res = CLIENT.chat_postMessage(
            channel=config.SLACK_CHANNEL, text=text
        )
        print(res.status_code)
    except SlackApiError as e:
        print(f"Failed to send to Slack client\n{e}")
    except Exception as e:
        print(f"Slack App execution failure, please report..\n{e}")
