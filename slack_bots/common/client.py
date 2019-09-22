import os

import slack


def get_client():
    """
    Returns authorized slack client.

    :return: Slack client.
    """
    return slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
