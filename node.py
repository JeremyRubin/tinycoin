from base import *

class Context(object):
    def __init__(self):
        self.peers = {}
        self.q = Queue(maxsize=10)
    def remove_peer(self, peer):
        del self.peers[peer]
    def add_peer(self, peer, conn):
        if peer in self.peers:
            self.peers[peer].close()
        self.peers[peer] = conn
    @gen.coroutine
    def broadcast(self, msg, without=set()):
        for peer, conn in self.peers:
            if peer in without:
                continue
            yield conn.write_message(msg)
"""
Peering Section
"""                

"""http://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=105 shows 7698 being unused"""
def local_peers():
    """List of router-local peers"""
    # a = ["ws://192.168.0.%d:%d"%(x,p) for p in [PORT_DEF, PORT]for x in xrange(2, 256) ] 

    a = ["localhost:%d"%(8000 if sys.argv[1] == "8001" else 8001)]
    random.shuffle(a)
    return a

# print local_peers()


def MakeIncomingPeer(ctx):
    """Create a handler bound to a specific context instance"""
    class IncomingPeer(tornado.websocket.WebSocketHandler):
        def check_origin(self, origin):
            return True
        @gen.coroutine
        def open(self):
            self.peer()
            yield ctx.q.put((OPEN,self.peer(), self))
        def peer(self):
            return self.request.headers["host"]
        @gen.coroutine
        def on_message(self, message):
            print message
            yield ctx.q.put((MSG,self.peer(), message))
        @gen.coroutine
        def on_close(self):
            yield ctx.q.put((CLOSE,self.peer()))
    return IncomingPeer

def client_on_message(ctx, peer):
    @gen.coroutine
    def cls(self, message):
        if message is None:
            yield ctx.q.put((CLOSE,peer))
        else:
            print message
            yield ctx.q.put((MSG,peer, message))
    return cls

def OutGoingPeer(ctx, host):
    return tornado.websocket.websocket_connect("ws://"+host, on_message_callback=client_on_message(ctx, host))

NPEERS = 10
@gen.coroutine
def repeer(ctx):
    # while True:
        print "A"
        for peer in local_peers():
            try:
                conn = yield OutGoingPeer(ctx, peer)
                yield ctx.q.put((OPEN, peer, conn))
            except Exception as e:
                print e

        yield gen.sleep(0.5)

def handle_start(ctx):
    IOLoop.current().spawn_callback(repeer,ctx)
def handle_open(ctx, peer, conn):
    ctx.add_peer(peer, conn)
tx_store = {}
def lookup_tx(txid):
    tx_store.get(txid, {"error":True} )

miner_q = Queue(maxsize=20)

def handle_msg(ctx, peer, message):
    m = ast.literal_eval(message)
    if m["hops"] > 4:
        pass
    else:
        m["hops"] += 1
        t = m["type"]
        if t == ADD_TX:
            tx = TX.deserialize(m["data"])
            yield ctx.broadcast(m, without={peer})
            yield miner_q.put(tx)
        if t == NEW_BLOCK:
            yield ctx.broadcast(m, without={peer})
        if t == QUERY_TX:
            send_reply(lookup_tx(m["data"]))
        

        
def handle_close(ctx, peer):
    ctx.remove_peer(peer)

functions = {START : handle_start,
             OPEN  : handle_open,
             MSG   : handle_msg,
             CLOSE : handle_close}

            

@gen.coroutine
def network_state_machine(ctx):
    yield ctx.q.put((START,))
    while True:
        print "IOLOOP"
        item = yield ctx.q.get()
        print item
        functions[item[0]](ctx, *item[1:])
        ctx.q.task_done()


# if __name__ == "__main__":
def main():
    ctx = Context()
    application = tornado.web.Application([
        (r"/", MakeIncomingPeer(ctx)),
    ])
    if len(sys.argv) > 1:
        application.listen(int(sys.argv[1]))
    else:
        application.listen(PORT)
    IOLoop.current().spawn_callback(network_state_machine, ctx)
    tornado.ioloop.IOLoop.current().start()
main()
