from P2P.node import Node
from threading import Thread

node = Node((5, 5))

thr = Thread(target=node.start_working)

thr.start()
thr.join()
