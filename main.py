from Lexer import Lexico
from Syntax import programa
from os.path import exists
import pdb

if __name__ == '__main__':


	#Verfica a existencia do arquivo
	if not exists('inputtest.txt'):
		print('Arquivo Inexistente!')
		exit()

	#abrir arquivo
	archive = open('inputtest.txt', 'r')
	#lendo as linhas do arquivo
	texto = archive.readlines()

	lexico = Lexico(texto)
	tokens = lexico.tokenizar()

	syntax = programa(tokens)
	if (syntax):
		print("Sucesso na análise sintática.")

	archive.close()
