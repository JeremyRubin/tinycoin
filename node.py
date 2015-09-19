from base import *
import chain as C
import block as B

class Context(object):
    def __init__(self):
        self.peers = {}
        self.q = Queue(maxsize=10)
        self.chain = C.Chain()
    def remove_peer(self, peer):
        del self.peers[peer]
    def add_peer(self, peer, conn):
        if peer in self.peers:
            self.peers[peer].close()
        self.peers[peer] = conn
    def peer_open(self, peer):
        return peer in self.peers
    @gen.coroutine
    def msg(self, peer, msg):
        print self.peers
        self.peers[peer].write_message(msg)
    @gen.coroutine
    def broadcast(self, msg, without=set()):
        for peer, conn in self.peers.iteritems():
            print "LOOK", peer, without, dir(conn)
            if peer in without:
                continue
            try:
                yield conn.write_message(msg)
            except Exception as e:
                print peer, e

#######################
### Peering Section####
#######################

START = 0
OPEN = 1
MSG = 2
CLOSE = 3

"""http://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=105 shows 7698 being unused"""
def local_peers():
    """List of router-local peers"""
    # a = ["ws://192.168.0.%d:%d"%(x,p) for p in [PORT_DEF, PORT]for x in xrange(2, 256) ] 

    a = ["localhost:%d"%(8000 if sys.argv[1] == "8001" else 8001)]
    random.shuffle(a)
    return a

# print local_peers()

#######################
###### Incoming Peer ##
#######################
def MakeIncomingPeerHandler(ctx):
    """Create a handler bound to a specific context instance"""
    class IncomingPeerHandler(tornado.websocket.WebSocketHandler):
        def check_origin(self, origin):
            return True
        @gen.coroutine
        def open(self):
            self.peer()
            yield ctx.q.put((OPEN,self.peer(), self))
        def peer(self):
            return self.request.remote_ip
        @gen.coroutine
        def on_message(self, message):
            print message
            yield ctx.q.put((MSG,self.peer(), message))
        @gen.coroutine
        def on_close(self):
            yield ctx.q.put((CLOSE,self.peer()))
    return IncomingPeerHandler

###############################
####   Outgoing Peer ##########
###############################
def client_on_message(ctx, peer):
    @gen.coroutine
    def cls(message):
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
    #while True:
        print "A"
        for peer in local_peers():
            if ctx.peer_open(peer):
                continue
            try:
                conn = yield OutGoingPeer(ctx, peer)
                yield ctx.q.put((OPEN, peer, conn))
            except Exception as e:
                print e
            yield gen.sleep(10)

@gen.coroutine
def handle_start(ctx):
    IOLoop.current().spawn_callback(repeer,ctx)
@gen.coroutine
def handle_open(ctx, peer, conn):
    ctx.add_peer(peer, conn)
@gen.coroutine
def handle_close(ctx, peer):
    ctx.remove_peer(peer)


#################################
# THIS IS THE IMPORTANT PART ####
#################################
#################################

ADD_TX = 0
NEW_BLOCK = 1
QUERY_TX = 2
GET_WORK = 3
@gen.coroutine
def handle_msg(ctx, peer, message):
    m = ast.literal_eval(message)
    if m["hops"] > 4:
        pass
    else:
        m["hops"] += 1
        t = m["type"]
        if t == ADD_TX:
            tx = TX.deserialize(m["data"])
            ctx.chain.add_tx(tx)
            yield ctx.broadcast(str(m), without={peer})
        if t == GET_WORK:
            yield ctx.msg(peer, str(map(lambda a: a.serialize(), ctx.chain.get_work())))
        if t == NEW_BLOCK:
            header_s, block_s = ast.literal_eval(m["data"])
            header = B.BlockHeader.deserialize(header_s)
            block = B.BlockTX.deserialize(block_s)
            ctx.chain.add_block(header, block)
            yield ctx.broadcast(str(m), without={peer})
        if t == QUERY_TX:
            yield ctx.msg(peer, str(ctx.chain.lookup_tx(m["data"])))




functions = {START : handle_start,
             OPEN  : handle_open,
             MSG   : handle_msg,
             CLOSE : handle_close}


@gen.coroutine
def network_state_machine(ctx):
    yield ctx.q.put((START,))
    while True:
        item = yield ctx.q.get()
        print item
        yield functions[item[0]](ctx, *item[1:])
        ctx.q.task_done()


def launch_app(ctx):
    application = tornado.web.Application([
        (r"/", MakeIncomingPeerHandler(ctx)),
    ])
    if len(sys.argv) > 1:
        application.listen(int(sys.argv[1]))
    else:
        application.listen(PORT)
def main():
    ctx = Context()
    launch_app(ctx)
    IOLoop.current().spawn_callback(network_state_machine, ctx)
    tornado.ioloop.IOLoop.current().start()
if __name__ == "__main__":
    main()
