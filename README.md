# TinyCoin

## What is TinyCoin?

The goal of TinyCoin is to provide a simple teaching cryptocurrency.

It is not "industrial quality", with an emphasis on simplicity over robustness.

It is a work in progress and is not feature complete at this point, however it is usable as an educational tool.

TinyCoin has the following constraint: total size of executable code should not exceed 1000 lines of code or teachable in an hour or two. This limit does not include tests or the README.md.

This initial version was put together in a couple of hours for HackMIT HackWeek 2015.

## Repo Overview

1. LICENSE -- MIT License
2. README.md -- This File
3. base.py -- Some primitives and common imports
4. transaction.py -- the way to build the instruction to tell the TinyCoin chain to spend an amount from A to B
5. block.py  -- The structure and header that transactions are bundled into
6. chain.py -- The data structure that aggregates blocks together and checks for validity of blocks
7. node.py -- the network code for talking to other users running TinyCoin and propagating blocks as well as interacting with clients.
8. miner.py -- a client script that gets mining work from a running nod
9. tests.py -- A (growing!) set of tests to ensure proper behavior. Full testing is not needed as certain "industrial strength" classes of errors should be ignored for simplicity


## TODO

1. Add a persistent client/wallet feature and more calls to node.py (perhaps spv)
2. Fix bugs in the networking code
3. Refactor the transaction format to be simpler
4. Provide a better mechanism for peering than local_peers in node.py.
5. Come up with some labs for adding certain features.
6. More todos ;)



# Pull requests welcome! Please keep in mind simplicity & teaching over correctness.


