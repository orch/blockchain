import json
from time import time


class Blockchain(object):

    # Инициализация цепи
    def __init__(self, id, file=True, chain=None):
        self.current_transactions = []

        # Тут инициализация переменной id, как идентификатора в сети,
        # но должно быть имя/никнейм
        self.id = id
        self.chain = []
        if chain is not None:
            self.chain = chain
        else:
            if file is False:
                try:
                    file = open("history/{}_chain.json".format(self.id), 'r')
                    self.chain = json.load(file)
                    file.close()
                except:
                    file = open("history/{}_chain.json".format(self.id), 'w')
                    self.add_block(hash='prev_hash', evidence='evidence')
                    json.dump(self.chain, file)
                    file.close()
            else:
                self.add_block(hash='prev_hash', evidence='evidence')

    # Метод добавления блока
    def add_block(self, hash, evidence, _time = None):

        # Проверка на None если мы лишь копируем блоки, а не создаем новый
        if _time is None:
            _time = time()

        block = {
            'index': len(self.chain) + 1,
            'time': _time,
            'transactions': self.current_transactions,
            'evidence': evidence,
            'hash': hash
        }

        self.current_transactions = []
        self.chain.append(block)

    # Метод добавления транзакции
    def add_transaction(self, _to, _amount, _from=None, _time=False):

        # Проверка на None если мы лишь копируем блоки, а не создаем новый
        if _from is None and not _time:
            _from = self.id
            _time = time()

        transaction = {
            'from': _from,
            'to': _to,
            'amount': _amount,
            'time': _time
        }
        self.current_transactions.append(transaction)

        return self.get_last_block['index'] + 1

    @property
    def get_last_block(self):
        return self.chain[-1]

    # Получаем блок по хешу
    def get_block(self, hash_value):

        for block in self.chain:
            if block['hash'] is hash_value:
                return block
        return False

    # Сохраняем цепь в файл
    def save_chain(self):

        file = "history/{}_chain.json".format(self.id)
        file = open(file, 'w')
        json.dump(self.chain, file)
        file.close()

    def __len__(self):
        return len(self.chain)

    # Получаю всю цепь
    def get_chain(self):
        return json.dumps(self.chain)