#Creando un blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify

#Armando el blockchain

class Blockchain:
    def __init__(self):
        self.chain = [] #cadena de bloques
        self.createBlock(proof=1, previous_hash='0') #bloque genesis
    
    def createBlock(self, proof, previous_hash):
        block = {'index':len(self.chain)+1, #indice del bloque
                 'timestamp': str(datetime.datetime.now()), #tiempo de creacion
                 'proof': proof, #proof
                 'previous_hash': previous_hash #hash previo
                 }
        
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1 #iremos incrementando
        check_proof = False
        
        #vamos a iterar hasta enontrar el proof que resuelva nuestro problema
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
            
            return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
                
    #chechamos si la informacion del blockchain es valida.
    #Checamos que el hash del previous block es igual en todos los bloques
    #Que le proof de cada bloque sea valido de acuerdo a cada bloque definido
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        new_proof = 1 #iremos incrementando
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1
        return True
    

#Minando el blockchain
app = Flask(__name__)
blockchain = Blockchain()


#Minando el nuevo bloque
@app.route('/mineblock', methods = ['GET'])

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.createBlock(proof, previous_hash)
    response = {'message': 'Felicidades, has minado un bloque!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash':block['previous_hash']
                }
    return jsonify(response), 200


#obteniendo cadena completa
@app.route('/get_chain', methods = ['GET'])

def get_chain():
    response = {'chain': blockchain.chain,
                'lenght': len(blockchain.chain)
                }
    return jsonify(response), 200


#Corriendo el app
app.run(host='0.0.0.0', port='5000')



        
        
        
        


