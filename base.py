
import hashlib
import sys
import ast
import random
import tornado
import tornado.websocket
from tornado.queues import Queue
from tornado import gen
from tornado.ioloop import IOLoop
def sha(x):
    return hashlib.sha256(x).hexdigest()

BOUND = 10e1000

PORT_DEF = 8001

PORT = 8000



ALREADY_PEERED = 0

# Msg Type
START = 0
OPEN = 1
MSG = 2
CLOSE = 3

ADD_TX = 0
NEW_BLOCK = 1
QUERY_TX = 2
def example(name, condition):
    print name
    assert condition


def pow(string, b):
    return int(string, 16) < b
