#!/usr/bin/env python3
# This will be the RESTful coap connection to the minecrat server
# This module will export a class that creates a coap context when created,
# then is able to handle requests for the user.
# Request 1: Get an id from the server
# Request 2: Get the current position and turn id from the server
# Request 3: Post a new block to the server

#imports
from aiocoap import *
import pickle
import logging
import asyncio

#...
