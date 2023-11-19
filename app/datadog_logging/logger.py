from datadog import initialize, api, statsd
import logging

import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

# Reading datadog configuration
app_key = config['datadog']['DD_APP_KEY']
api_key = config['datadog']['DD_API_KEY']

# Initializing Datadog with the API key and application key
options = {
    'app_key': app_key,
    'api_key': api_key
}

initialize(**options)

# Set up logging to send logs to Datadog
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def logInfo(title, text, priority):
    # Log an info event
    api.Event.create(
        title=title,
        text=text,
        priority=priority,
        tags=['info', 'application:forsit-test']
    )

def logError(title, text, priority):
    # Log an error event
    api.Event.create(
        title=title,
        text=text,
        priority=priority,
        tags=['error', 'application:forsit-test']
    )
