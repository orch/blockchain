from P2P.node import Node
from threading import Thread

node = Node((2, 3))

thr = Thread(target=node.start_working)

thr.start()
thr.join()
