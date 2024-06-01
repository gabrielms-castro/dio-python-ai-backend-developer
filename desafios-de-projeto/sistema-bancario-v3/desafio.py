import textwrap
from abc import ABC, abstractmethod, classmethod
from datetime import datetime

class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
       
class Conta:
    
    def __init__(self, cliente, numero):
        #Atributos definidos anteriormente no desafio e que deveriam ter esses valores iniciais
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)        
    
    @property
    def saldo(self, valor):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
 
        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False    
            
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

class ContaCorrente(Conta):

    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])
        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saques >= self.limite_saques
        
        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        
        elif excedeu_saque:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
                      
class Historico:
    
    def __init__(self):
        self._transacoes = []
    
    @classmethod
    def transacaos(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo" : transacao.__class__.__name__,
                "valor" : transacao.valor,
                "data" : datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )  

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass
        
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """
    ========= MENU =========
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Novo cliente
    [lc] Listar clientes
    [nu] Novo usuário
    [q] Sair
    """
    print(menu)
    
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui contas. @@@")
        return
    
    return cliente.contas[0]
          
def depositar(clientes):
    cpf = input("Informe o CPF:\t")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente: print("\n@@@ Cliente não localizado. @@@")
    
    valor = float(input("Informe o valor do depósito:\t"))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def sacar(clientes):
    pass

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == "d":
            depositar(clientes)
        
        elif opcao == "s":
            sacar(clientes)
        
        elif opcao == "e":
            exibir_extrato(clientes)
        
        elif opcao == "nu":
            criar_cliente(clientes)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == 'lc':
            listar_contas(contas)
        
        elif opcao == "q":
            break
        