lexer = Lexer("PROGRAMME test; FIN")
tokens = lexer.readalltokens()

for token in tokens:
    print(token.type, repr(token.value))