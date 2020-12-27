from P2P.node import Node
from threading import Thread

node = Node((1, 1))

thr = Thread(target=node.start_working)

thr.start()
thr.join()
