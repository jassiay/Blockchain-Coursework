import hashlib
import json
from time import time
from urllib.parse import urlparse

from uuid import uuid4

import requests

from flask import Flask, jsonify, request



class Blockchain:
    def __init__(self):
        self.current_tx = []
        self.chain = []
        self.nodes = set()

        self.new_genesis_block()


    def new_genesis_block(self):
        """
        """
        first_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        first_time = time()

        block = {
            'index': len(self.chain) + 1,
            'timestamp': first_time,
            'transactions': self.current_tx,
            'nonce': self.proof_of_work(first_hash, first_time),
            'prev_hash': first_hash,
        }
        self.current_tx = []

        self.chain.append(block)
        return block


    def new_block(self, nonce, prev_hash, timestamp):
        """
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': timestamp,
            'transactions': self.current_tx,
            'nonce': nonce or self.proof_of_work(prev_hash, timestamp),
            'prev_hash': prev_hash or self.hash(self.chain[-1]),
        }

        self.current_tx = []

        self.chain.append(block)

        return block


    def new_transaction(self, recipient, sender, amount):
        """
        """
        self.current_tx.append({
            'recipient': recipient,
            'sender': sender,
            'amount': amount,
        })


        return self.last_block['index'] + 1

    @property
    def last_block(self):
        if len(self.chain)>0:
            return self.chain[-1]
        else:
            return None


    @staticmethod
    def hash(block):
        """
        """
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


    def register_node(self, addr):
        """
        """

        url = urlparse(addr)
        if url.netloc:
            self.nodes.add(url.netloc)
        elif url.path:
            self.nodes.add(url.path)
        else:
            raise ValueError('url is invalid')


    def valid_chain(self, chain):
        """
        """
        last_block = chain[0]
        current_ind = 1

        while current_ind < len(chain):
            block = chain[current_ind]
            print(f'{last_block}')
            print(f'{block}')
            print("\n--------------------\n")

            if block['prev_hash'] != self.hash(last_block):
                return False

            if not self.valid_proof(block['index'], block['timestamp'], block['transactions'], block['nonce'], block['prev_hash']):
                return False

            last_block = block
            current_ind += 1

        return True


    def resolve_conflicts(self):
        """
        """
        nghbrs = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in nghbrs:
            rp = requests.get(f'http://{node}/chain')

            if rp.status_code is 200:       #validation
                length = rp.json()['length']
                chain = rp.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False


    @staticmethod
    def valid_proof(index, timestamp, transactions, nonce, last_hash):
        """
        """
        block_to_verify = {
            'index': index,
            'timestamp': timestamp,
            'transactions': transactions,
            'nonce': nonce,
            'prev_hash': last_hash,
        }

        guess_string = json.dumps(block_to_verify, sort_keys=True).encode()
        guess_hash = hashlib.sha256(guess_string).hexdigest()

        return guess_hash[:4] == "0000"


    def proof_of_work(self, last_hash, timestamp):
        """
        """
        if self.last_block is not None:
            current_index = self.last_block['index'] + 1
        else:
            current_index = 1
        nonce = 0

        while self.valid_proof(current_index, timestamp, self.current_tx, nonce, last_hash) is False:
            nonce += 1

        return nonce




app = Flask(__name__)

node_id = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    timestp = time()
    blockchain.new_transaction(
        recipient=node_id,
        sender="coinbase",
        amount=100,
    )
    last_block = blockchain.last_block

    prev_hash = blockchain.hash(last_block)

    nonce = blockchain.proof_of_work(prev_hash, timestp)

    block = blockchain.new_block(nonce, prev_hash, timestp)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'nonce': block['nonce'],
        'prev_hash': block['prev_hash'],
        'block_hash': blockchain.hash(block)
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['recipient', 'sender', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = blockchain.new_transaction(values['recipient'], values['sender'], values['amount'])

    response = {'message': f'The transaction will be added to Block {index}'}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }

    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')

    args = parser.parse_args()

    port = args.port

    app.run(host='127.0.0.1', port=5000)

