from time import sleep
import json

white = '\033[1;97m'
red = '\033[1;91m'
blue = '\033[1;34m'
light_blue = '\033[38;5;51m'
green = '\033[38;5;83m'
yellow = '\033[1;93m'
dark_red = '\033[38;5;88m'

TIPOS = {
    '1': ('chep', 'CHEP'),
    '2': ('quebradas', 'Quebradas'),
    '3': ('exportacao', 'Exportação'),
}

#Função de timer, para repetir menos.
def timer(x, y):
    for c in range(0, y):
        print('*'.center(60))
        sleep(x)


#Função de save com Json
def data_save(data):
    with open('sfrio.json', 'w') as file:
        json.dump(data, file, indent = 4)


#Funçao de load com Json
def data_load():
    padrao = {
        'chep': 0,
        'quebradas': 0,
        'exportacao': 0,
        'slip_sheet': 0
    }

    try:
        with open ('sfrio.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return padrao


#Input de escolha
def input_choice(msg, opt, erro):
    while True:
        chc = input(msg).strip().upper()

        if chc[0] in opt:
            return chc[0]

        num_error(erro)


#Mensagem de erro
def num_error(msg):
    print()

    print('\033[1;97m┌────────────────────────────────────┐'.center(70))
    print(f'   [\033[1;91mERRO\033[1;97m] {msg}    '.center(75))
    print('└────────────────────────────────────┘'.center(62))
    print()


#Caixa de mensagens/titulos
def box(msg):
    print(f'{white}┌────────────────────────────────────┐'.center(68))
    print(f'           |       {msg}        |')
    print(f'└────────────────────────────────────┘'.center(60))


#Menu principal
def menu_p():
    print()
    print(f'  {white}--------------- {blue}SUPER FRIO{white} --------------- \n'.center(82))
    print('╔──────────────────────────────────────╗'.center(60))
    print('|         CONTAGEM DE PALLETS          |'.center(60))
    print('╠══════════════════════════════════════╣'.center(60))
    print(f'|  {blue}1{white} - Pallets CHEP                    |'.center(73))
    print(f'|  2 - Pallets Quebradas               |'.center(60))
    print(f'|  3 - Pallets de Exportação           |'.center(60))
    print('|  4 - Slip Sheet                      |'.center(60))
    print('|  5 - Ver resumo                      |'.center(60))
    print(f'|  {red}6{white} - Resetar contagens               |'.center(73))
    print(f'|  {dark_red}0{white} - Sair                            |'.center(78))
    print('╚──────────────────────────────────────╝\n'.center(62))


#Menu de modos (Fileira e avulso [A/B])
def menu_modo(nome):
    print(f'                        ---{nome}---  ')
    print('           ┌───────────────────────────────────┐')
    print('           |       A - Fileira x Altura        |')
    print('           |       B - Avulso                  |')
    print('           |       V - Voltar                  |')
    print('           └───────────────────────────────────┘')
    return input('\n                          Modo: ').strip().upper()


#Modo A
def modo_fileiras(contagens, tipo, nome):
    print(f'{white}┌────────────────────────────────────┐'.center(68))
    print(f'|     [Fileiras x Altura] -- {nome}    |'.center(60))
    print(f'└────────────────────────────────────┘'.center(60))
    print(f'\n            Digite os blocos um a um. |ENTER em branco para parar|.')
    subtotal_sessao = 0

    while True:
        entrada = input('\n            N° de fileiras (ENTER para parar): ').strip()

        if entrada == '':
            break
        try:

            fileiras = int(entrada)
            altura = int(input('            Altura: ').strip())
            bloco = fileiras * altura
            subtotal_sessao += bloco
            contagens[tipo] += bloco
            data_save(contagens)

            print()
            print(f'┌────────────────────────┐'.center(58))
            print(f'     |{green}{fileiras} x {altura} ={white} {bloco}       '.center(75))
            print(f'      |Sessão: {subtotal_sessao}     '.center(53))
            print(f'     |Total {nome}: {contagens[tipo]}      '.center(60))
            print(f'└────────────────────────┘'.center(58))

        except ValueError:
            num_error('DIGITE NÚMEROS INTEIROS')


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
            data_save(contagens)
            print(f'      |+{qtd}|')
            print(f'      |Sessão: {subtotal_sessao}')
            print(f'      |Total {nome}: {contagens[tipo]}')
        except ValueError:
            print('            \033[1;91mERRO\033[m. Digite apenas números inteiros.')


def slp_sht(contagens):
    total = 0
    box('CONTAGEM -SLIP SHEET-')

    while True:
        sheets = input('\n                    Qtd de Slip Sheets: ').replace(',','.') #CADA MARCA NA RÉGUA == 25 slip sheets
        try:
            if sheets == '':
                break

            else:
                sheets = float(sheets)
                total += sheets*25 #Converte as marcas pra medida final de slip sheets
        except ValueError:
            num_error('NÚMERO INVÁLIDO')

    contagens['slip_sheet'] = total
    data_save(contagens)
    print(total)


#'dispatcher' (escolher o modo e chamar função)
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
            num_error('OPÇÃO INVÁLIDA')


#Resumo (mostrar os valores totais)

def resumo(contagens):
    print()
    print("╔══════════════════════════════════════╗".center(60))
    print("║           RESUMO FINAL               ║".center(60))
    print("╠══════════════════════════════════════╣".center(60))
    print(f'║  CHEP:        {contagens['chep']:>5} pallets          ║'.center(60))
    print(f'║  Quebradas:   {contagens['quebradas']:>5} pallets          ║'.center(60))
    print(f'║  Exportação:  {contagens['exportacao']:>5} pallets          ║'.center(60))
    print(f'║  Slip Sheet:      {contagens['slip_sheet']:>5}              ║'.center(60))
    print("╚══════════════════════════════════════╝\n".center(62))
    sleep(2.5)


#main (menu PRINCIPAL agora)

def main():

    contagens = data_load()

    while True:

        menu_p()

        opcao = input('                    Escolha uma opção: ').strip()
        print()

        if opcao in TIPOS:
            tipo, nome = TIPOS[opcao]
            gerenciar_tipo(contagens, tipo, nome)

        elif opcao == '4':
            slp_sht(contagens)

        elif opcao == '5':
            resumo(contagens)

        elif opcao == '6':
            confirma = input_choice('                   Resetar tudo? (S/N): ', ('S', 'N'), 'OPÇÃO INVÁLIDA')

            if confirma == 'S':

                contagens = {'chep': 0, 'quebradas': 0, 'exportacao': 0, 'slip_sheet': 0}

                data_save(contagens)

                print(f'\n                  ✅{green}Contagens resetadas{white}.')
                print()

                timer(0.3, 3)

        elif opcao == '0':
            print(f'\n             {light_blue}Encerrando{white}. Bom trabalho amanhã!')
            sleep(0.6)
            print()

            timer(0.5, 3)

            resumo(contagens)
            break

        else:
            num_error('OPÇÃO INVÁLIDA')

if __name__ == '__main__':
    main()