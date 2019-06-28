from os import system

class JogoDaVelha:

	__grade = []
	__simbolo_da_vez = "x"
	__contador_de_jogadas = 0
	__fim_de_jogo = False
	__vencedor = None

	# Preenche a matriz "grade" com símbolos que representam o vazio
	def __init__(self):
		for i in range(0, 3):
			self.__grade.append(3 * ["-"])

	# Converte a estrutura de dados em uma representação gráfica
	def __str__(self):
		texto = ""
		for i in range(0, 3):
			texto += str(self.__grade[i]) + "\n"
		return texto

	# Retorna o símbolo vencedor
	def get_vencedor(self):
		return self.__vencedor

	# Limpa o terminal e imprime a representação do jogo
	def atualizar(self):
		system("clear")
		print(self)

	# Retorna se o jogo terminou
	def is_fim_de_jogo(self):
		return self.__fim_de_jogo

	# Passa a vez de um símbolo para o outro
	def __swap_de_simbolo(self):
		if self.__simbolo_da_vez == "x":
			self.__simbolo_da_vez = "o"
		else:
			self.__simbolo_da_vez = "x"

	# Recebe uma string que contem informações das coordenadas da posição
	# da jogada. Caso a entrada não seja válida, é retornado None.
	# Caso contrário, retorna um inteiro representando a linha e outro
	# representando a coluna.
	def __processar_entrada(self, coordenadas):
		try:
			[linha, coluna] = coordenadas.split(",")
			linha = int(linha)
			coluna = int(coluna)
			linha -= 1
			coluna -= 1
			if linha < 0 or linha > 2:
				return None
			if coluna < 0 or coluna > 2:
				return None
			return linha, coluna
		except:
			return None

	# Esse é o método que realiza, de fato, uma jogada. Ele recebe o símbolo
	# do jogador que está tentando fazer uma jogada e a posição onde este tentou
	# jogar. É retornada uma mensagem de acordo com o status da jogada.
	def desenhar_simbolo(self, simbolo, coordenadas):
		# Caso não seja a vez do símbolo que tentou jogar.
		if not simbolo == self.__simbolo_da_vez:
			return "Nao eh sua vez"
		# Caso a entrada seja inválida.
		if self.__processar_entrada(coordenadas) == None:
			return "Jogada invalida"
		else:
			linha, coluna = self.__processar_entrada(coordenadas)
		# Caso a jogada tenha sido feita em uma posição já ocupada.
		if self.__grade[linha][coluna] != "-":
			return "Jogada invalida"

		# Caso o fluxo tenha chegado aqui, a jogada pode ser realizada,
		# de fato.
		self.__grade[linha][coluna] = self.__simbolo_da_vez
		self.__contador_de_jogadas += 1
		self.__swap_de_simbolo()
		self.__vencedor = self.__verificar_fim_de_jogo()
		# Caso o jogo tenha terminado com essa jogada.
		if self.__vencedor != None:
			self.__fim_de_jogo = True
			self.atualizar()
			return "Fim de jogo"
		# Caso a jogada não tenha terminado o jogo.
		else:
			self.atualizar()
			return "Ok"

	# São verificadas todas situações em que o jogo se encerra.
	# Retorna o símbolo do vencedor, ou None (não acabou), ou "Nenhum" (empate).
	def __verificar_fim_de_jogo(self):
		#Se houve vencedor nas linhas.
		for linha in range(0, 3):
			if self.__grade[linha][0] == self.__grade[linha][1]:
				if self.__grade[linha][1] == self.__grade[linha][2]:
					if self.__grade[linha][2] != "-":
						return self.__grade[linha][2];
		#Se houve vencedor nas colunas.
		for coluna in range(0, 3):
			if self.__grade[0][coluna] == self.__grade[1][coluna]:
				if self.__grade[1][coluna] == self.__grade[2][coluna]:
					if self.__grade[2][coluna] != "-":
						return self.__grade[2][coluna];
		#Se houve vencedor nas diagonal 1.
		if self.__grade[0][0] == self.__grade[1][1]:
			if self.__grade[1][1] == self.__grade[2][2]:
				if self.__grade[2][2] != "-":
					return self.__grade[2][2];
		#Se houve vencedor nas diagonal 2.
		if self.__grade[0][2] == self.__grade[1][1]:
			if self.__grade[1][1] == self.__grade[2][0]:
				if self.__grade[2][0] != "-":
					return self.__grade[2][0];

		# Se o jogo empatou.
		if self.__contador_de_jogadas == 9:
				return "Nenhum"

		# O jogo continua...
		return None
