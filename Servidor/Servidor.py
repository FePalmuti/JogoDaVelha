import socket
import threading
import time
from JogoDaVelha import JogoDaVelha

class Servidor:
	ip = ""
	porta = 4000
	lista_conexoes =[]
	simbolo_correspondente = {}
	fim_da_conexao = False
	resultado = ""

	def __init__(self):
		# O socket do servidor é preparado.
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((self.ip, self.porta))
		self.s.listen(7)
		# Uma thread é criada para estabelecer novas conexões com clientes.
		t_aceitacao = threading.Thread(target=self.aceitacao)
		t_aceitacao.daemon = True;
		t_aceitacao.start()

		# É instanciado um objeto do tipo jogo da velha.
		self.jv = JogoDaVelha()
		self.jv.atualizar()

	# Vincula uma conexão com cliente a um símbolo, por "órdem
	# de chegada".
	def adicionar_relacao_com_um_simbolo(self, conexao):
		if len(self.simbolo_correspondente) == 0:
			self.simbolo_correspondente[conexao] = "x"
		elif len(self.simbolo_correspondente) == 1:
			self.simbolo_correspondente[conexao] = "o"

	# Método que define o comportamento da thread de aceitação.
	def aceitacao(self):
		while not self.fim_da_conexao:
			try:
				# Uma nova conexão é estabelecida.
				conexao, ip_cliente = self.s.accept()
				# É enviada a representação do jogo para o cliente.
				conexao.send(self.jv.__str__().encode())
				print(ip_cliente, " conectado!")

				self.lista_conexoes.append(conexao)
				# O cliente é vinculado a um símbolo.
				self.adicionar_relacao_com_um_simbolo(conexao)
				# É criada uma thread para gerenciar a comunicação entre
				# o servidor e o cliente em questão.
				t = threading.Thread(target=self.processamento, args=(conexao,))
				t.daemon = True;
				t.start()
			except:
				pass

	# Método que define o comportamento da thread que gerencia a comunicação entre
	# o servidor e o cliente em questão.
	def processamento(self, conexao):
		while not self.fim_da_conexao:
			try:
				# Servidor recebe dados do cliente.
				dados = conexao.recv(1024)
				resposta = self.jv.__str__()

				# Caso um espectador tente fazer uma jogada.
				if conexao not in self.simbolo_correspondente:
					resposta += "\nVoce nao estah no jogo!"
					conexao.send(resposta.encode())
				# Caso um jogador tente fazer uma jogada.
				else:
					coordenadas = dados.decode()
					# É feita uma tentativa de jogada e uma mensagem de status é recebida.
					status = self.jv.desenhar_simbolo(self.simbolo_correspondente[conexao], coordenadas)
					resposta = self.jv.__str__()

					# Para os casos abaixo, somente o cliente que fez a jogada recebe uma resposta.
					if status == "Nao eh sua vez":
						resposta += "\nNao eh sua vez!"
						conexao.send(resposta.encode())
					elif status == "Jogada invalida":
						resposta += "\nJogada invalida!"
						conexao.send(resposta.encode())
					# Para os casos abaixo, todos os cliente recebem uma resposta.
					elif status == "Ok":
						for c in self.lista_conexoes:
							c.send(resposta.encode())
					elif status == "Fim de jogo":
						if self.jv.get_vencedor() == "Nenhum":
							resposta += "\nO jogo empatou!"
						else:
							resposta += "\nO simbolo " + self.jv.get_vencedor() + " venceu!"
						for c in self.lista_conexoes:
							c.send(resposta.encode())
							time.sleep(0.4)
							c.send("Fim da conexao".encode())
						self.fim_da_conexao = True
			except:
				pass


serv = Servidor()
while not serv.fim_da_conexao:
	pass
print("Fim de jogo e conexoes encerradas!")
input()
