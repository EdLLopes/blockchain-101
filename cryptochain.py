""" Importante entender que esse codigo é um demonstrativo para pessoas leigas compreenderem como funciona um blockchain.
Um sistema real teria criptografias mais robustas, reconheceria cada player desse mercado, e como cada player tem sua blockchain verificaria antes de uma transacao se o hash e valido. (Todos players devem ter o mesmo hash para participar do sistema, ja que tem a mesma chain).
O sistema de Proof odf Work e Mining, estão super simplificados perto de um codigo real, porem nesse e possivel perceber o sistema de segurança do blockchain, basta alterar o parametro difficuty do blockchain e vera a dificuldade do seu processador de realizar o PoW. 
"""



from hashlib import sha256 # Algoritmo de hash seguro de 256 bits

def transaction(user, receiver, value, asset):
    """Funcao vai coletar dados de uma transacao e concatenar esses dados em uma string
    
    :param user: Player que ira realizar uma transação
    :type user: string
    :param receiver: Player que vai receber a transação
    :type receiver: string
    :param value: O valor de criptomoedas que vai ser transferido
    :type value: string, int, float
    :param asset: O ativo que sera trocado entre os players (Ativo real, ativo virtual, NFT, serviço, etc.)
    :type asset: string
    :return: informacoes dos parametros concatenadas em uma string
    """
    
    return '/'.join([user, str(value), receiver, asset])

class Block:
    """Cria um bloco que será utilizado no blockchain
    """
    
    def __init__(self, transactions: str, previous_hash, nonce = 0):
        """Receve dados e define como propriedades do objeto bloco
        
        :param transactions: Recebe um conjunto de transacoes
        :type transactions: str
        :param previous_hash: Recebe o hash do bloco anterios
        :type previous_hash: string
        :param nonce: "number only used once" e o numero que sera adicionado ao Block para determinar seu grau de dificuldade na criptografia 
        :type nonce: int
        :return: None
        """
        
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = 'None' # Espaço para o futuro hash de um bloco
    
    def create_hash(self):
        """Concatena os parametros do Bloco e faz sua criptografia
        
        :return: hash calculado do bloco em uma sting
        """
        
        bloc_string = '/'.join([str(self.nonce), self.transactions, self.previous_hash])
        next_hash = sha256(bloc_string.encode()).hexdigest()
        return next_hash   
        

class Blockchain:
    
    def __init__(self):
        """Define algumas propriedades do Objeto Blockchain        
        """
        
        self.difficuty = 2 # Grau de dificuldade do PoW 
        self.chain = list()
        self.uncorfimed_transactions = list()
        self.zero_block() # Criando o primeiro bloco do blockchain
        
    def zero_block(self):
        """Cria o primeiro bloco e acrescenta na lista como primeiro objeto.
        """
        genesis = Block('None', 'None') # Criacao de um bloco sem hash anterior 
        genesis.hash = genesis.create_hash()
        self.chain.append(genesis)
    
    @property
    def last_block(self):
        """Propriedade que vai retornar o ultimo Block adicionado a blockchain
        """
        return self.chain[-1]
    
    def create_block(self, *args):
        """ Cria um Block a partir de informacoes de transacoes
        
        :param args: Todas as transacoes que vão fazer parte daquele bloco
        :type args: string
        """
        
        block_string = str()
        for i in args:
            block_string += i
        block = Block(block_string, self.last_block.hash)
        self.uncorfimed_transactions.append(block) # Adiciona a lista de blocos ainda não computados o hash 
        
    def proof_of_work(self, block):
        """A partir de um Block calcula seu hash e retorna ele computado
        
        :param block: Bloco que sera computado o hash
        :type block: Block
        """
        
        block.nonce = 0 
        computed_hash = block.create_hash()
        while not computed_hash.startswith('0' * self.difficuty): # Aqui é onde entra o grau de dificuldade 
            block.nonce += 1
            computed_hash = block.create_hash()
        return computed_hash
    
    def mine(self):
        """ Vai pegar o bloco nao confirmado e computar o seu hash, transformando em um bloco confirmado e colocando-o como ultimo bloco na chain
        
        :return: Novo bloco com seu hash computado 
        """
        
        if not self.uncorfimed_transactions: # Verificando se a lista de blocos nao computados esta vazia 
            return False
        
        new_block = self.uncorfimed_transactions[0] 
        
        proof = self.proof_of_work(new_block)
        new_block.hash = proof # Colocando como hash do bloco 
        self.chain.append(new_block)
        self.uncorfimed_transactions = []
        return new_block
    

        
         
        
    
    
        
        
        