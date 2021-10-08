
palavraReservada = ('$','if','then','while','do','write','read','else','begin','end','real','integer','var','procedure','program')
simpleSymbol = ('+', '-', '<', '>', '*', '/', ',', '.', '(', ')', ';', ':', '=')
doubleSymbol = (':=', '<>', '<=', '>=')
delimitador = ('\t','\n',' ','$','+','-','<','>','*','/',',','.','(',')',';',':','=')
isComentario1 = False
isComentario2 = False
symbol = ''
isAuxiliar = False
isAuxiliar2 = False
isDoubleChecker = False
token = ''
tokens = []

class Token:
    def __init__(self, valor, tipo, linha):
        self.valor = valor
        self.tipo = tipo
        self.linha = linha
        self.categoria = None

    def __str__ (self):
        return "Token ({valor}: {tipo} - {linha})".format(
            valor = self.valor, tipo = self.tipo, linha = self.linha)

    __repr__ = __str__

    def __eq__(self, outro):
        return (self.valor, self.tipo) == (outro.valor, outro.tipo)

class Lexico(object):
    def __init__(self, texto): #Construtor da classe.
        self.texto = texto

    def verificarToken(self, i):
        if (token[0].isalpha() and token.isalnum()):
            if(token in palavraReservada):
                tokens.append(Token(token,'reservada',i))
            else:
                tokens.append(Token(token,'identificador',i))
        elif(token.isdigit()):
            tokens.append(Token(token,'inteiro',i))
        elif(token == 'end.'):
            tokens.append(Token('end','reservada',i))
            tokens.append(Token('.','simples',i))
        else:
            try:
                float(token)
                tokens.append(Token(token,'real',i))
            except:
                tokens.append(Token(token,'invalido',i))

    def tokenizar(self):
        texto = self.texto
        global palavraReservada
        global simpleSymbol
        global doubleSymbol
        global delimitador
        global symbol
        global isComentario2
        global isComentario1
        global isAuxiliar
        global isAuxiliar2
        global isDoubleChecker
        global token
        global tokens

        for i, linha in enumerate(texto):
            for caracter in linha:
                #identificar se é comentario
                if (isComentario2):
                    '''Se isAux leu /* '''
                    if (isAuxiliar):
                        if (isAuxiliar2):
                            '''Consumiu comentário'''
                            if (caracter == '/'):
                                isAuxiliar = False
                                isAuxiliar2 = False
                                isComentario2 = False
                            else:
                                isAuxiliar2 = False
                        elif (caracter == '*'):
                            isAuxiliar2 = True
                    elif (caracter == '*'):
                        isAuxiliar = True
                    else:
                        if(caracter == '{'):
                            tokens.append(Token('/','simples',i))
                            isComentario2 = False
                            isAuxiliar = False
                            isAuxiliar2 = False
                            isComentario1 = True
                        elif(caracter == '/'):
                            tokens.append(Token('/','simples',i))
                            isComentario1 = False
                            isAuxiliar = False
                            isAuxiliar2 = False
                            isComentario2 = True
                        elif(caracter.isdigit()):
                            tokens.append(Token('/','simples',i))
                            isComentario1 = False
                            isComentario2 = False
                            isAuxiliar = False
                            isAuxiliar2 = False
                        elif(caracter.isalpha()):
                            tokens.append(Token('/','simples',i))
                            isComentario1 = False
                            isComentario2 = False
                            isAuxiliar = False
                            isAuxiliar2 = False
                        else:
                            token = token +'/'+ caracter
                            isComentario1 = False
                            isComentario2 = False
                            isAuxiliar = False
                            isAuxiliar2 = False
                elif (isComentario1):
                    if(caracter == '}'):
                        isComentario1 = False
                elif(caracter == '{'):
                    if(token != ''):
                        self.verificarToken(i)
                        token = ''
                    isComentario1 = True
                elif(caracter == '/'):
                    if(token != ''):
                        self.verificarToken(i)
                        token = ''
                    isComentario2 = True

                elif(caracter in delimitador):
                    if(isDoubleChecker):
                        if(symbol == '<' and (caracter == '=' or caracter == '>')):
                            token = symbol + caracter
                            tokens.append(Token(token, 'duplo', i))
                            token = ''
                        elif((symbol == '>' or symbol == ':') and caracter == '='):
                            token = symbol + caracter
                            tokens.append(Token(token, 'duplo', i))
                            token = ''
                        else:
                            tokens.append(Token(symbol, 'simples', i))
                            if(caracter != ' ' and caracter != '\n' and caracter != '\t'):
                                token = token + caracter
                        isDoubleChecker = False
                        symbol = ''
                    elif(caracter == '<' or caracter == '>' or caracter == ':'):
                        isDoubleChecker = True
                        symbol = caracter
                        if(token != ''):
                            self.verificarToken(i)
                            token = ''
                    elif(caracter == '.'):
                        token = token + '.'
                    else:
                        if(token != ''):
                            self.verificarToken(i)
                            token = ''
                        if(caracter != '\n' and caracter != ' ' and caracter != '\t'):
                            tokens.append(Token(caracter, 'simples', i))
                else:
                    if(symbol != ''):
                        tokens.append(Token(symbol, 'simples', i))
                        symbol = ''
                    token = token + caracter
                    isDoubleChecker = False
        return tokens


    def imprimeTokens(self, tokens):
        for t in tokens:
            print('valor: ' + str(t.valor) + ' tipo: ' + str(t.tipo) + ' linha: ' + str(t.linha+1) + '\n')
