# -*- coding: utf-8 -*-
from __future__ import print_function

# --------------- i18n Stuff ----------------------
messages = {
    'welcome_message': {'de': u"Willkommen beim Alexa Bitcoin Austria skill;" \
                              u"Ich kann dir dabei helfen, den Bitcoin Preis im Auge zu behalten;" \
                              u"Frage nach dem aktuellen Bitcoin Preis, indem du folgende Frage stellst: " \
                              u"Alexa; Frage Bitcoin Austria; Wie viel ist ein Bitcoin in Euro?",
                        'en': u"Welcome to the Bitcoin Austria skill;" \
                              u"I can help you keeping the current Bitcoin price in sight;" \
                              u"Ask for the current Bitcoin exchange rate by saying: " \
                              u"Alexa; Ask Bitcoin Austria; How much is a Bitcoin in Euro?"
                        },
    'reprompt_text': {'de': u"Alexa; Frage Bitcoin Austria; Wie viel ist ein bitcoin in Euro?",
                      'en': u"Alexa; Ask Bitcoin Austria; How much is a Bitcoin in Euro?"
                      },
    'answer_price': {
        'de': u"Der Bitcoin Preis ist rund %d %s",
        'en': u"The Bitcoin price is about %d %s"
    },
    'error_unknown_currency': {
        'de': u"Ich kenne diese Währung nicht. Ich kenne nur Dollar, Euro und Pfund.",
        'en': u"I don't know this currency. I only know Dollar, Euro and Pounds."
    },
    'answer_title': {
        'de': u"Bitcoin Preis in %s",
        'en': u"Bitcoin rate in %s"
    }
}


def getMessage(message_id, arguments=()):
    """ Gets the transalted version of the message """
    global locale_string
    global messages

    language = locale_string[:2].lower()
    if message_id not in messages or language not in messages[message_id]:
        raise ValueError("Translation not found")
    return messages[message_id][language] % arguments


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session = False):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "Coindesk - " + title,
            'content': "Bitcoin Austria - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behaviour ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Hallo"
    speech_output = getMessage('welcome_message')
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = getMessage('reprompt_text')
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text))


def get_btcat(intent, session, slots):
    global locale_currency_string
    session_attributes = {}
    reprompt_text = None

    currency_dict = slots['currency']

    if 'value' in currency_dict:
        currency = str(currency_dict['value']).upper()
    else:
        currency = locale_currency_string

    if currency == 'EURO':
        currency = 'EUR'
    elif currency == 'DOLLAR':
        currency = 'USD'
    elif currency == 'PFUND':
        currency = 'GBP'
    elif currency == 'POUNDS':
        currency = 'GBP'
    elif currency == 'POUND':
        currency = 'GBP'

    if currency not in {'EUR', 'USD', 'GBP'}:
        print("Unknown currency: \"" + currency + "\"")
        speech_output = getMessage('error_unknown_currency')
    else:
        speech_output = getMessage('answer_price', (get_btc_price(currency), currency))

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        getMessage('answer_title', currency), speech_output, reprompt_text))


def get_btc_price(currency):
    from urllib2 import urlopen
    from json import load
    response = urlopen('http://api.coindesk.com/v1/bpi/currentprice.json')
    data = load(response)
    return data['bpi'][currency]['rate_float']


# --------------- Events ------------------
def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session, slots):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "Bitcoin":
        return get_btcat(intent, session, slots)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


# --------------- Main handler ------------------
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """

    global locale_string
    global locale_currency_string
    import locale

    locale_string = locale.normalize(event['request']['locale'])
    locale.setlocale(locale.LC_ALL, locale_string)

    print("event.request.locale=" +
          locale_string)

    locale_currency_string = locale.localeconv()['int_curr_symbol'].strip()

    print("locale_currency_string=" +
          locale_currency_string)

    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'], event['request']['intent']['slots'])