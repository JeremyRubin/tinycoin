from base import *
from node import GET_WORK
msg = str({"type": GET_WORK, "hops": 0})


@gen.coroutine
def client_on_message(self, message):
    if message is None:
        print None
    else:
        print message

def OutGoingPeer():
    
    conn = yield tornado.websocket.websocket_connect("ws://"+sys.argv[1], on_message_callback=client_on_message)
    print conn
    conn.write_message(msg)
if __name__ == "__main__":
    OutGoingPeer()

