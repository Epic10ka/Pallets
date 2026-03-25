TIPOS = {
    '1': ('chep', 'CHEP'),
    '2': ('quebradas', 'Quebradas'),
    '3': ('exportacao', 'Exportação')
}

def menu_p():
    print('--------------- \033[1;34mEMPRESA\033[m --------------- ')
    print("╔══════════════════════════════════════╗")
    print("║         \033[1;97mCONTAGEM DE PALLETS\033[m          ║")
    print("╠══════════════════════════════════════╣")
    print("║  1 - Pallets CHEP                    ║")
    print("║  2 - Pallets Quebradas               ║")
    print("║  3 - Pallets de Exportação           ║")
    print("║  4 - Ver resumo                      ║")
    print("║  5 - Resetar contagens               ║")
    print("║  0 - Sair                            ║")
    print("╚══════════════════════════════════════╝")

def menu_modo(nome):
    print(f'           ------- {nome} -------')
    print()
    print('            \033[1;97mA - Fileira x Altura')
    print('            B - Avulso')
    print('            V - Voltar\033[m')
    print()
    return input('           Modo: ').strip().upper()

#Modo A

def modo_fileiras(contagens, tipo, nome):
    print(f'            [Fileiras x Altura] -- {nome} ')
    print()
    print(f'            Digite os blocos um a um. |ENTER em branco para parar|.')
    subtotal_sessao = 0
    print()

    while True:
        entrada = input('            N° de fileiras (ENTER para parar): ').strip()
        if entrada == '':
            break
        try:
            fileiras = int(entrada)
            altura = int(input('            Altura: ').strip())
            bloco = fileiras * altura
            subtotal_sessao += bloco
            contagens[tipo] += bloco
            print()
            print(f'      |{fileiras} x {altura} = {bloco}|')
            print(f'      |Sessão: {subtotal_sessao}')
            print(f'      |Total {nome}: {contagens[tipo]}')
        except ValueError:
            print('            \033[1;91ERRO\033[m. Digite apenas números inteiros.')

#Modo B

def modo_avulso(contagens, tipo, nome):
    print(f'            [AVULSO] - {nome}')
    print()
    print('             Digite a quantidade de grupos de pallet |ENTER em branco para parar|')
    print()
    subtotal_sessao = 0
    print()

    while True:
        entrada = input('           Qtd do grupo (ENTER para parar): ').strip()
        if entrada == '':
            break
        try:
            qtd = int(entrada)
            subtotal_sessao += qtd
            contagens[tipo] += qtd
            print(f'      |+{qtd}|')
            print(f'      |Sessão: {subtotal_sessao}')
            print(f'      |Total {nome}: {contagens[tipo]}')
        except ValueError:
            print('            \033[1;91mERRO\033[m. Digite apenas números inteiros.')

#dispatcher (escolher o modo e chamar função)

def gerenciar_tipo(contagens, tipo, nome):
    while True:
        modo = menu_modo(nome)
        if modo == 'A':
            modo_fileiras(contagens, tipo, nome)
        elif modo == 'B':
            modo_avulso(contagens, tipo, nome)
        elif modo == 'V':
            break
        else:
            print('            \033[1;91mERRO\033[m. Opção inválida')

#Resumo (mostrar os valores totais)

def resumo(contagens):
    total = sum(contagens.values())
    print("\n╔══════════════════════════════════════╗")
    print("║           RESUMO FINAL               ║")
    print("╠══════════════════════════════════════╣")
    print(f"║  CHEP:        {contagens['chep']:>5} pallets          ║")
    print(f"║  Quebradas:   {contagens['quebradas']:>5} pallets          ║")
    print(f"║  Exportação:  {contagens['exportacao']:>5} pallets          ║")
    print("║  ————————————————————————————————    ║")
    print(f"║  TOTAL GERAL: {total:>5} pallets          ║")
    print("╚══════════════════════════════════════╝\n")


#main (menu PRINCIPAL agora)

def main():
    contagens = {'chep': 0, 'quebradas': 0, 'exportacao': 0}
    print()
    print('       Bem vindo ao Sistema de contagem de pallets')
    print()
    print('       Use o modo A para blocos organizados e o modo B para pallets avulsas.')
    print()
    while True:
        menu_p()
        opcao = input('           Escolha uma opção: ').strip()

        if opcao in TIPOS:
            tipo, nome = TIPOS[opcao]
            gerenciar_tipo(contagens, tipo, nome)
        elif opcao == '4':
            resumo(contagens)

        elif opcao == '5':
            confirma = input('            Resetar tudo? (S/N)').strip().upper()
            if confirma == 'S':
                contagens = {'chep': 0, 'quebradas': 0, 'exportacao': 0}
                print('            ✅Contagens resetadas.')
        elif opcao == '0':
            resumo(contagens)
            print('     Encerrando. Bom trabalho amanhã!')
            break
        else:
            print('            \033[1;91mERRO\033[m. Opção inválida')

if __name__ == '__main__':
    main()