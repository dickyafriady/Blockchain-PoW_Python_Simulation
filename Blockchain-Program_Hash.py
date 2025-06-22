import hashlib
import json
from time import time
from uuid import uuid4
import random

class Blockchain(object):
    difficulty_target = "0000"

    unique_ids = [ "w['8X0#J`nTA&zo[o[jR", "88'9~(LW%8:]-#6g$N9E","bN~>vp`PF5R1=MQA1?1*",]

    def hash_block(self, block):
        block_copy = block.copy()
        block_copy.pop('hash_of_previous_block', None)
        block_encoded = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(block_encoded).hexdigest()

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        genesis_block = {
            'index': 0,
            'timestamp': time(),
            'transactions': [],
            'nonce': 0,
            'hash_of_previous_block': None,
            'verifier': 'Genesis',
            'user': 'System'
        }
        self.append_block(genesis_block)

    def proof_of_work(self, index, hash_of_previous_block, transactions):
        nonce = 0
        while self.valid_proof(index, hash_of_previous_block, transactions, nonce) is False:
            nonce += 1
        return nonce

    def valid_proof(self, index, hash_of_previous_block, transactions, nonce):
        content = f'({index}{hash_of_previous_block}{transactions}{nonce})'.encode()
        content_hash = hashlib.sha256(content).hexdigest()
        return content_hash[:len(self.difficulty_target)] == self.difficulty_target

    def append_block(self, block):
        if len(self.chain) > 0:
            block['hash_of_previous_block'] = self.hash_block(self.chain[-1])
        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'amount': amount,
            'recipient': recipient,
            'sender': sender
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def validate_unique_id(self, unique_id):
        return unique_id in self.unique_ids

    def get_block_count(self):
        return len(self.chain)

if __name__ == "__main__":
    blockchain = Blockchain()
    node_identifier = str(uuid4()).replace('-', "")

    while True:
        unique_id = input("Masukkan Unique ID (atau ketik 'stop' untuk berhenti): ")
        if unique_id.lower() == 'stop':
            break

        start_time = time()
        if blockchain.validate_unique_id(unique_id):
            blockchain.add_transaction(sender="0", recipient=node_identifier, amount=1)
            verifier = random.choice(["Miner", "Perusahaan xyz"])
            user = "User"
            nonce = blockchain.proof_of_work(len(blockchain.chain), blockchain.hash_block(blockchain.last_block), blockchain.current_transactions)
            block = {
                'index': len(blockchain.chain),
                'timestamp': time(),
                'transactions': blockchain.current_transactions,
                'nonce': nonce,
                'verifier': verifier,
                'user': user
            }
            blockchain.append_block(block)

            print("Blok baru telah ditambahkan (ditambang)")
            print("Indeks:", block['index'])
            print("Hash Blok Sebelumnya:", block['hash_of_previous_block'])
            print("Nonce:", block['nonce'])
            print("Transaksi:", block['transactions'])
            print("Verifikator:", block['verifier'])
            print("User:", block['user'])
        else:
            print("Unique ID Tidak Valid!")

        end_time = time()
        print("Total Waktu Komputasi:", end_time - start_time, "detik")
        print("-" * 30)

    print("Jumlah Blok dalam Blockchain:", blockchain.get_block_count())
