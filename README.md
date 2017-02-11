# Bitcoin Skill for Alexa
Bitcoin Austria Alexa Skill

## Prerequisites

Python 2.7.x (since AWS Lambdas don't support 3.x yet)
An AWS Account

## Howto Install/Test

tbd

## Features

- Get current bitcoin price
- Multiple currencies (USD; GBP; EUR)
- Multilingual (DE; EN)
- Guessing of currency based on locale

## Contribute
Just send a pull request or create an Issue.

## Possible Features for the future
Vertical Features:
- Price changes
- Interactive Mode (Question Answer)
- Remembering of selected options (e.g. currency)
- Better output Card (images etc.)

Horizontal Featues:
- Bitcoin News
- Next BTC AT Meetups
- Bitcoin Map Information

Non Functional:
- Simulated AWS Events for test execution
- Extract i18n 

## Folders

- docs - contains all documentation needed files (images etc.)
- icons - all icons used for the alexa skill
- webpage - the page (probably just an s3 bucket) referenced by the skill (tos, agreements, howtos etc.)