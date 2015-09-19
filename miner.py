from base import *
from node import GET_WORK, NEW_BLOCK
from block import BlockHeader
msg = str({"type": GET_WORK, "hops": 0})

resp = Queue(10)
@gen.coroutine
def response(message):
    if message is None:
        print None
    else:
        bh, b = ast.literal_eval(message)
        bh = BlockHeader.deserialize(bh)
        while not pow(bh.hash(), BOUND):
            b.nonce +=1
        yield resp.put(str((bh.serialize(), b ) ))
        
@gen.coroutine
def OutGoingPeer():
    conn = yield tornado.websocket.websocket_connect("ws://"+sys.argv[1], on_message_callback=response)
    conn.write_message(msg)
    b = yield resp.get()
    conn.write_message(str({"type": NEW_BLOCK, "hops":0, "data": b}))
if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(OutGoingPeer)

