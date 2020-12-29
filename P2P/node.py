import socket
from threading import Thread
import numpy as np
import struct
from storebase.database import Blockchain
import json
import time


class Node(object):
    R = 20

    # Инициализация через координаты x, y в круге
    def __init__(self, position, name):
        self.x = position[0]
        self.y = position[1]
        self.scan_range = self.define_range()
        self.port = self.define_port()
        self.host_port = self.port + self.scan_range[0]
        self.scan_range = np.delete(self.scan_range, self.port)
        self.coins = np.random.randint(1, 20)
        self.times = []
        self.chain_lengths = 0
        self.message_table = []
        self.name = name
        self.blockchain = Blockchain(id=self.name, file=False)

        print('Мой порт:', self.port)
        print('Мой баланс:', self.coins)
        print('Моя инициализирующая цепочка:', self.blockchain.chain)

    # Определения порта для узла в зависимости от позиции
    # относительно самого себя
    def define_port(self):
        return int(self.R * self.x + self.y)

    # Определение порта относительно круга
    def define_range(self):
        tg = self.y / self.x
        alpha = np.arctan(tg)
        if alpha < 0:
            if self.y < 0:
                alpha += 2 * np.pi
            else:
                alpha = np.pi - np.abs(alpha)
        if self.x < 0 and self.y < 0:
            alpha += np.pi

        alpha = alpha * 180 / np.pi
        quarter = np.ceil(alpha / 360 * 4)
        _range = np.arange(1000 * quarter, 1000 * quarter + self.R ** 2, dtype=int)
        return _range

    # Запуск работы узла
    def start_working(self):

        self.reporting(report_type=1)

        client_thread = Thread(target=self.client_side)
        server_thread = Thread(target=self.server_side)

        server_thread.start()
        client_thread.start()

        server_thread.join()
        client_thread.join()

    # Отправка отчета для отрисовки тех, кто вошел/вышел из сети и
    # установил/оборвал соединение
    def reporting(self, report_type):

        sock = socket.socket()
        sock.connect(('localhost', 5050))
        message = struct.pack(">HHHH", report_type, self.x, self.y, self.host_port)
        sock.send(message)
        sock.close()

    def reporting_in_process(self, destination_port):

        sock = socket.socket()
        sock.connect(('localhost', 5050))
        message = struct.pack(">HH", self.host_port, destination_port)
        sock.send(message)
        sock.close()

    def create_block_for_sending(self, _to, _amount):

        self.blockchain.add_transaction(_to=_to, _amount=_amount)
        self.blockchain.add_block(hash='hash_' + str(np.random.randint(0, 1000)) + '_' + str(self.port),
                                  evidence='evidence_' + str(self.port))
        self.blockchain.save_chain()

    # Вот тут вместо порта id
    def update_balance(self):
        for block in self.blockchain.chain:
            try:
                if int(block['transactions'][0]['to']) == self.host_port \
                        and block['transactions'][0]['time'] not in self.times:
                    print('Вам монеты')
                    self.coins += int(block['transactions'][0]['amount'])
                    self.times.append(block['transactions'][0]['time'])
            except:
                continue
        print('Баланс', self.coins)

    # Логика серверного потока узла
    def server_side(self):
        self.message_table.append('Server side')
        print('Server side')

        sock = socket.socket()
        sock.bind(('', self.host_port))
        sock.listen(1)

        while True:
            conn, addr = sock.accept()
            conn.send(str.encode('Открыт канал связи с {}'.format(self.host_port)))
            msg = conn.recv(100)
            self.message_table.append(msg.decode())
            print(msg.decode())

            _to = input('Кому отправить?')
            if _to != 'n':

                # self.blockchain = Blockchain(id=str(self.port))
                self.chain_lengths = len(self.blockchain)
                _amount = input('Сколько отправить?')
                self.create_block_for_sending(_to=_to, _amount=_amount)

                chain = self.blockchain.get_chain()
                conn.send(chain.encode())

                print(self.blockchain.chain)

    # Логика клиентского потока узла
    def client_side(self):
        self.message_table.append('Client side')
        print('Client side')

        def ping_port(port_number, out_info):

            connected = False

            sock = socket.socket()
            try:
                sock.connect(('localhost', port_number))
                connected = True
                self.reporting_in_process(destination_port=port_number)
                out_info[port_number] = 'Listening'
            except:
                out_info[port_number] = 'Closed'

            if connected:

                sock.send(str.encode('Открыт канал связи с {}'.format(self.host_port)))
                msg = sock.recv(100)
                self.message_table.append(msg.decode())
                print(msg.decode())

                time.sleep(2)

                chain_recv = sock.recv(2000)
                chain_recv = chain_recv.decode()
                chain_recv = json.loads(chain_recv)

                if len(chain_recv) >= self.chain_lengths:
                    self.chain_lengths = len(chain_recv)

                    print('>=')
                    print(chain_recv)

                    for block in chain_recv:
                        if block not in self.blockchain.chain:
                            self.chain_lengths = len(self.blockchain.chain) + 1
                            self.blockchain.add_transaction(_to=block['transactions'][0]['to'],
                                                            _amount=block['transactions'][0]['amount'],
                                                            _from=block['transactions'][0]['from'],
                                                            _time=block['transactions'][0]['time']
                                                            )
                            self.blockchain.add_block(hash=block['hash'],
                                                      evidence=block['evidence'],
                                                      _time=block['time'])
                print(self.blockchain.chain)

                self.update_balance()

                self.blockchain.save_chain()

                self.reporting(report_type=0)
                sock.close()

        threads = []
        output = {}
        for port in self.scan_range:
            t = Thread(target=ping_port, args=(port, output))
            threads.append(t)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
