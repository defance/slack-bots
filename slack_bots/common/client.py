import os

import slack


def get_client(**kwargs):
    """
    Returns authorized slack client.

    :return: Slack client.
    """
    return slack.WebClient(token=os.environ['SLACK_API_TOKEN'], **kwargs)


def get_rtm_client():
    return slack.RTMClient(token=os.environ['SLACK_API_TOKEN'], run_async=True)
