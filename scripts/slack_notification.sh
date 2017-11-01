#!/bin/bash
#
#    usage: slack_message.sh $SLACK_WEBHOOK_URL "Yo!"
#
SLACK_MESSAGE="$2"
curl -X POST --data "payload={\"text\": \"${SLACK_MESSAGE}\", \"icon_emoji\": \":house:\", \"username\": \"12 Oxford Avenue\"}" $1

