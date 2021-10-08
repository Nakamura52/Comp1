from Lexer import Token
from operator import itemgetter
scopeAtual= "main"
table={"main":{}}
buffer_var = []
contador = 0
contador_aux = 0
buffer_type = None
buffer_function = ""
buffer_args=[]
buffer_scope = None
cat = ""


def TS_Busca(cadeia):    
	return cadeia in table[scopeAtual]

def TS_Busca_Global(cadeia):    
	return cadeia in table["main"]

def TS_Busca_escopo(cadeia, escopo):    
	return cadeia in table[escopo]

def VerificaParametros():
	global buffer_args
	global scopeAtual
	global table
	global buffer_scope
	tabelaAux = table[buffer_scope]
	listaAux = []
	for linha in tabelaAux:
		if "param" in tabelaAux[linha]:
			listaAux.append(tabelaAux[linha])
	listaAux = sorted(listaAux, key=itemgetter(-1))
	if len(listaAux) != len(buffer_args):
		exit("Número de argumentos incompatível, esperado: {}, recebido: {}".format(len(listaAux), len(buffer_args)))
	else:
		for a,b in zip(listaAux, buffer_args):
			if not a[2] == b[2]:
				exit("Tipo de parametro incompatível, recebido: {}, esperado: {}".format(b[2],a[2]))
	buffer_args.clear()

def NovoEscopo(nomedoEscopo):
	contador_aux = 0
	table[nomedoEscopo] = {}

def TS_Inserir(cadeia, token, tipo,  escopo, cont):
	global scopeAtual
	global cat
	if TS_Busca(cadeia):
		exit("Variavél {}, já declarada no escopo {}".format(cadeia,escopo))
	table[scopeAtual][cadeia] = ([token, cat, tipo, scopeAtual, cont])

def TS_Var_Inserir(tipo):
    global buffer_var
    global scopeAtual
    global contador_aux
    global contador
    for variavel in buffer_var:
        if scopeAtual == "main":
            TS_Inserir(variavel.valor, variavel.tipo, tipo, scopeAtual, cont=contador)
            contador += 1
        else:
            TS_Inserir(variavel.valor, variavel.tipo, tipo, scopeAtual, cont=contador_aux)
            contador_aux += 1
    buffer_var.clear()  

def erro(token, esperado):
    print("Erro de sintaxe: linha {} | esperado: {} | entrada: {}"
          "".format(token.linha+1, esperado, token.valor))
    exit()

def programa(tokens):
	global table
	if not tokens:
		token = Token('<null>','<null>',0)
		erro(token,'program')
	if(tokens[0].valor != 'program'):
		erro(tokens.pop(0), 'program')
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<identificador>')
		if(tokens[0].tipo != 'identificador'):
			erro(tokens.pop(0),'<identificador>')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'begin')
			corpo(tokens)
			if(tokens[0].valor != '.'):
				erro(tokens.pop(0), '.')
			else:
				tokens.pop(0)
				if tokens:
					erro(tokens.pop(0),'<fim>')
				else:
					return True


def corpo(tokens):
	dc(tokens)
	if(tokens[0].valor != 'begin'):
		erro(tokens.pop(0), 'begin')
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<comando>')
		comandos(tokens)
		if(tokens[0].valor != 'end'):
			erro(tokens.pop(0), 'end')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'.')

def dc(tokens):
	global cat
	aux = tokens[0]
	if(aux.valor == 'var'):
		cat = "var"
		dc_v(tokens)
		mais_dc(tokens)
	elif(aux.valor == 'procedure'):
		cat = "proc"
		dc_p(tokens)
		mais_dc(tokens)
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'comando')
		return

def dc_v(tokens):
	if(tokens[0].valor != 'var'):
		erro(tokens.pop(0),'var')
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<identificador>')
		variaveis(tokens)
		if(tokens[0].valor != ':'):
			erro(tokens.pop(0), ':')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<tipo_var>')
			tipo_var(tokens)

def variaveis(tokens):
	global scopeAtual
	global contador
	global contador_aux
	global buffer_var
	if(tokens[0].tipo != 'identificador'):
		erro(tokens.pop(0), '<identificador>')
	else:
		buffer_var.append(tokens[0])
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,':')
		mais_var(tokens)

def mais_var(tokens):
	aux = tokens[0]
	if(aux.valor != ','):
		return
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<identificador>')
		variaveis(tokens)

def tipo_var(tokens):
	global buffer_var
	global scopeAtual
	global escopos
	aux = tokens[0]
	if(aux.valor == 'real' or aux.valor == 'integer'):
		TS_Var_Inserir(aux.valor)
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,';')
			return
	else:
		erro(aux, '<tipo_var>')

def mais_dc(tokens):
	aux = tokens[0]
	if(aux.valor == ';'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'end')
		dc(tokens)
	else:
		return

def dc_p(tokens):
	global cat
	global scopeAtual
	global contador
	if(tokens[0].valor == 'procedure'):
		cat = "proc"
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<identificador>')
		if(tokens[0].tipo == 'identificador'):
			TS_Inserir(tokens[0].valor, tokens[0].tipo, None, scopeAtual, cont=contador)
			scopeAtual = tokens[0].valor
			NovoEscopo(scopeAtual)
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<parametros>')
			parametros(tokens)
			corpo_p(tokens)
		else:
			erro(tokens[0], '<identificador>')
	else:
		erro(tokens[0],'procedure')


def parametros(tokens):
	global cat
	aux = tokens[0]
	if(aux.valor == '('):
		cat = "param"
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<tipo_var>')
		lista_par(tokens)
		if(tokens[0].valor != ')'):
			erro(tokens.pop(0), ')')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'begin')
	else:
		return

def lista_par(tokens):
	global cat
	cat = "param"
	variaveis(tokens)
	if(tokens[0].valor != ':'):
		erro(tokens.pop(0), ':')
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<tipo_var>')
		tipo_var(tokens)
		mais_par(tokens)

def mais_par(tokens):
	aux = tokens[0]
	if(aux.valor == ';'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<tipo_var>')
		lista_par(tokens)
	else:
		return

def corpo_p(tokens):
	global cat
	global scopeAtual
	cat = "var"
	dc_loc(tokens)
	if(tokens[0].valor != 'begin'):
		erro(tokens.pop(0), 'begin')
	else:
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<comando>')
		comandos(tokens)
		if(tokens[0].valor != 'end'):
			erro(tokens.pop(0),'end')
		else:
			scopeAtual = "main"
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'begin')

def dc_loc(tokens):
	aux = tokens[0]
	if(aux.valor == 'var'):
		dc_v(tokens)
		mais_dcloc(tokens)
	else:
		return

def mais_dcloc(tokens):
	aux = tokens[0]
	if(aux.valor == ';'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'begin')
		dc_loc(tokens)
	else:
		return

def comandos(tokens):
	comando(tokens)
	mais_comandos(tokens)

buffer_read = []

buffer_write = []

def comando(tokens):
	global buffer_type
	global buffer_var
	global buffer_scope
	global buffer_read
	global scopeAtual
	global buffer_write
	aux = tokens[0]
	if(aux.valor == 'read'):
		tokens.pop(0)
		if(tokens[0].valor != '('):
			erro(tokens.pop(0), '(')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<identificador>')
			variaveis(tokens)
			for i in buffer_var:
				if(TS_Busca(i.valor)):
					buffer_read.append(table[scopeAtual][i.valor])
				elif(TS_Busca_Global(i.valor)):
					buffer_read.append(table["main"][i.valor])
				else:
					print("Variável: {} não declarada na linha: {}".format(i.valor,aux.linha+1))
					exit()
			if(tokens[0].valor != ')'):
				erro(tokens.pop(0), ')')
			else:
				linha = tokens.pop(0).linha
				if not tokens:
					token = Token('<null>','<null>',linha)
					erro(token,'end')
	elif(aux.valor == 'write'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'(')
		if(tokens[0].valor != '('):
			erro(tokens.pop(0),'(')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<identificador>')
			variaveis(tokens)
			for i in buffer_var:
				if(TS_Busca(i.valor)):
					buffer_read.append(table[scopeAtual][i.valor])
				elif(TS_Busca_Global(i.valor)):
					buffer_read.append(table["main"][i.valor])
				else:
					print("Variável: {} não declarada na linha: {}".format(i.valor,aux.linha+1))
					exit()
			if(tokens[0].valor != ')'):
				erro(tokens.pop(0),')')
			else:
				linha = tokens.pop(0).linha
				if not tokens:
					token = Token('<null>','<null>',linha)
					erro(token,'end')
	elif(aux.valor == 'while'):
		peek = tokens[1]
		if peek.valor == '(':
			peek = tokens[2]
		buffer_type = table[scopeAtual][peek.valor]
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
		condicao(tokens)
		if(tokens[0].valor != 'do'):
			erro(tokens.pop(0),'do')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<comando>')
			comandos(tokens)
			if(tokens[0].valor != '$'):
				erro(tokens.pop(0),'$')
			else:
				linha = tokens.pop(0).linha
				if not tokens:
					token = Token('<null>','<null>',linha)
					erro(token,'end')
	elif(aux.valor == 'if'):
		peek = tokens[1]
		if peek.valor == '(':
			peek = tokens[2]
		buffer_type = table[scopeAtual][peek.valor]
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
		condicao(tokens)
		if(tokens[0].valor != 'then'):
			erro(tokens.pop(0),'then')
		else:
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<comando>')
			comandos(tokens)
			pfalsa(tokens)
			if(tokens[0].valor != '$'):
				erro(tokens.pop(0),'$')
			else:
				linha = tokens.pop(0).linha
				if not tokens:
					token = Token('<null>','<null>',linha)
					erro(token,'end')
	elif(aux.tipo == 'identificador'):
		# pegar o valor e buscar na TS e jogar no buffer 
		if not(TS_Busca(tokens[0].valor)):
			if not(TS_Busca_Global(tokens[0].valor)):
				print("Variável: {} não declarada na linha: {}".format(aux.valor,aux.linha+1))
				exit()
		buffer_type = table[scopeAtual][tokens[0].valor] if TS_Busca(tokens[0].valor) else table["main"][tokens[0].valor]
		buffer_scope = tokens[0].valor
		restoident(tokens)
	else:
		erro(tokens.pop(0),'<comando>')

def condicao(tokens):
	expressao(tokens)
	relacao(tokens)
	expressao(tokens)

def expressao(tokens):
	termo(tokens) 
	outros_termos(tokens)

def termo(tokens):
	op_un(tokens)
	fator(tokens) 
	mais_fatores(tokens)

def op_un(tokens):
	aux = tokens[0]
	if(aux.valor == '+'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(aux.valor == '-'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	else:
		return

def fator(tokens):
	global buffer_var
	global buffer_type
	global scopeAtual
	global table
	aux = tokens[0]
	if(aux.tipo == 'identificador'):
		if(TS_Busca(tokens[0].valor)):
			if(buffer_type[2] != table[scopeAtual][tokens[0].valor][2]):
				exit("Variável: {} de tipo não permitido na linha: {}".format(tokens[0].valor,tokens[0].linha+1))
		elif(TS_Busca_Global(tokens[0].valor)):
			if(buffer_type[2] != table["main"][tokens[0].valor][2]):
				exit("Variável: {} de tipo não permitido na linha: {}".format(tokens[0].valor,tokens[0].linha+1))
		else:
			exit("Variável: {} não declarada na linha: {}".format(tokens[0].valor,tokens[0].linha+1))
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<relação>')
	elif(aux.tipo == 'inteiro'):
		if(buffer_type[2] != "integer"):
			exit("Variável: {} de tipo não permitido na linha: {}".format(tokens[0].valor,tokens[0].linha+1))
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<relação>')
	elif(aux.tipo == 'real'):
		if(buffer_type[2] != "real"):
			exit("Variável: {} de tipo não permitido na linha: {}".format(tokens[0].valor,tokens[0].linha+1))
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<relação>')
	else:
		if(tokens[0].valor == '('):
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'<expressao>')
			expressao(tokens) 
			if(tokens[0].valor == ')'):
				linha = tokens.pop(0).linha
				if not tokens:
					token = Token('<null>','<null>',linha)
					erro(token,'<expressao>')
			else:
				erro(tokens.pop(0), ')')
		else:
			erro(tokens.pop(0), '(')

def mais_fatores(tokens):
	aux = tokens[0]
	if(aux.valor == '*' or aux.valor == '/'):
		op_mul(tokens)
		fator(tokens)
		mais_fatores(tokens)
	else:
		return

def op_mul(tokens):
	if(tokens[0].valor == '*'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '/'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	else:
		erro(tokens.pop(0), '<op_mul>')

def outros_termos(tokens):
	aux = tokens[0]
	if(aux.valor == '+' or aux.valor == '-'):
		op_ad(tokens)
		termo(tokens)
		outros_termos(tokens)
	else:
		return

def op_ad(tokens):
	if(tokens[0].valor == '+'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '-'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	else:
		erro(tokens.pop(0), 'op_ad')

def relacao(tokens):
	if(tokens[0].valor == '='):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '<>'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '>='):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '<='):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '>'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	elif(tokens[0].valor == '<'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<fator>')
	else:
		erro(tokens.pop(0), 'relação')

def restoident(tokens):
	global table
	global buffer_scope
	linha = tokens.pop(0).linha
	if not tokens:
		token = Token('<null>','<null>',linha)
		erro(token,'<fator')
	if(tokens[0].valor == ':='):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<expressao>')
		expressao(tokens)
	else:
		if table["main"][buffer_scope][1] != "proc":
			exit("Procedimento: {}. Não declarado na linha: {}".format(buffer_scope, tokens[0].linha + 1))
		lista_arg(tokens)


def argumentos(tokens):
	global buffer_args
	global table
	global scopeAtual
	global buffer_scope
	if(tokens[0].tipo != 'identificador'):
		erro(tokens.pop(0),'<identificador>')
	else:
		# mais_ident(tokens)
		if not TS_Busca_escopo(tokens[0].valor, buffer_scope):
			if not TS_Busca_Global(tokens[0].valor):
				exit("Variavel não declarada!!!!!")
		buffer_args.append(table[buffer_scope][tokens[0].valor] if TS_Busca_escopo(tokens[0].valor, buffer_scope) else table["main"][tokens[0].valor])
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<argumento>')
		mais_ident(tokens)

def mais_ident(tokens):
	if(tokens[0].valor == ';'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<argumento>')
		argumentos(tokens)
	else:
		return

def pfalsa(tokens):
	if(tokens[0].valor == 'else'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<argumento>')
		comandos(tokens)
	else:
		return

def mais_comandos(tokens):
	if(tokens[0].valor == ';'):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<comando>')
		comandos(tokens)
	else:
		return

def lista_arg(tokens):
	if(tokens[0].valor == '('):
		linha = tokens.pop(0).linha
		if not tokens:
			token = Token('<null>','<null>',linha)
			erro(token,'<argumento>')
		argumentos(tokens)
		if(tokens[0].valor != ')'):
			erro(tokens.pop(0),')')
		else:
			VerificaParametros()
			linha = tokens.pop(0).linha
			if not tokens:
				token = Token('<null>','<null>',linha)
				erro(token,'comando')
	else:
		return


