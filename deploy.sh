#!/bin/bash

docker pull shravani31816/hybrid-chatbot
docker stop chatbot-container || true
docker rm chatbot-container || true
docker run -d --name chatbot-container shravani31816/hybrid-chatbot
