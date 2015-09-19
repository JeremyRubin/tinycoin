from ecdsa import SigningKey, VerifyingKey
import hashlib
import sys
import ast
import random
import tornado
import tornado.websocket
from tornado.queues import Queue
from tornado import gen
from tornado.ioloop import IOLoop
import datetime
def sha(x):
    return hashlib.sha256(x).hexdigest()

BOUND = 0b111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
print BOUND

PORT_DEF = 8001

PORT = 8000



ALREADY_PEERED = 0




BLOCK_REWARD = 25e8
def example(name, condition):
    print name
    assert condition


def pow(string, b):
    print string, b
    return int(string, 16) < b
