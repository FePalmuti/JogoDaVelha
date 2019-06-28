import socket
import threading
from os import system

class Cliente:
	porta = 4000
	fim_da_conexao = False

	def __init__(self, ip_servidor):
		# O socket do cliente é preparado para estabelecer conexão.
		self.ip = ip_servidor
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.ip, self.porta))
		# É criada uma thread para enviar dados para o servidor.
		t_envio = threading.Thread(target=self.enviar)
		t_envio.start()
		# É criada uma thread para receber dados do servidor.
		t_recebimento = threading.Thread(target=self.receber)
		t_recebimento.start()

	# Método que define o comportamento da thread de envio.
	def enviar(self):
		while not self.fim_da_conexao:
			try:
				mensagem = input("")
				self.s.send(mensagem.encode())
			except:
				pass

	# Método que define o comportamento da thread de recebimento.
	def receber(self):
		while not self.fim_da_conexao:
			try:
				dados = self.s.recv(1024)
				mensagem = dados.decode()
				# Caso o jogo no servidor tenha sofrido uma alteração de jogada comum.
				if mensagem != "Fim da conexao":
					system("clear")
					print(mensagem)
				# Caso o jogo tenha encerrado no servidor.
				else:
					self.s.close()
					self.fim_da_conexao = True
			except:
				pass


ip = input("Digite o IP do servidor: ")
c = Cliente(ip)
