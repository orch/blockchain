from storebase.database import Blockchain

blockchain = Blockchain('Zyaeen')

print(blockchain.chain)

blockchain.add_transaction(_to='Nastya', _amount=123)
blockchain.add_block(hash='new_hash_zyaeen', evidence='evidence_zyaeen')
blockchain.save_chain()



print(blockchain.chain)

blockchain = Blockchain('Zyaeen', False)

print(len(blockchain))

print(blockchain.chain)