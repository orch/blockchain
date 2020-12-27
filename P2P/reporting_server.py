import socket
import struct
import matplotlib.pyplot as plt

"""
    Тут все для визуализации
"""

sock = socket.socket()
sock.bind(('', 5050))
sock.listen(1)

nodes = {}
matrix = {}

while True:

    conn, addr = sock.accept()
    message = conn.recv(8)
    try:
        message = struct.unpack(">HHHH", message)
        report_type = message[0]
        x = message[1]
        y = message[2]
        port = message[3]
        # print(x, y)

        if report_type is 1:
            nodes[port] = [x, y]
        else:
            # del nodes[port]
            keys_to_del = []
            for key in matrix.keys():
                if str(port) in key:
                    keys_to_del.append(key)
            for key in keys_to_del:
                del matrix[key]
    except:
        message = struct.unpack(">HH", message)
        # print(message)
        host_port, port = message[0], message[1]
        key = '{}-{}'.format(host_port, port)
        print(key)
        matrix[key] = [nodes[host_port], nodes[port]]

    circle = plt.Circle((0, 0), 20, color='b', fill=False)
    plt.figure(figsize=(7, 7))
    ax = plt.gca()
    ax.cla()
    ax.set_xlim((-25, 25))
    ax.set_ylim((-25, 25))
    ax.add_artist(circle)

    for key in nodes.keys():
        plt.plot(nodes[key][0], nodes[key][1], color='red', marker='o', markersize=5)
    for key in matrix.keys():
        plt.plot((matrix[key][0][0], matrix[key][1][0]), (matrix[key][0][1], matrix[key][1][1]), color='red')

    plt.savefig('map.png')
    plt.show()