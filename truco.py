from time import sleep
from random import randint

class Baralho:
    def __init__(self):
        self.CARTAS = ['j', 'q', 'k', 'a', '2', '3', 'coringa', 'ouro', 'espadas', 'copas', 'zap']
        self.cartas = {'j': 4, 'q': 4, 'k': 4, 'a': 3, '2': 4, '3': 4, 'coringa': 1, 'ouro': 1, 'espadas': 1, 'copas': 1, 'zap': 1}

    def distribuir(self):
        if sum([x for x in self.cartas.values()]) > 4:
            mao = []
            for x in range(0, 3):
                while True:
                    index = randint(0, 10)
                    carta = self.CARTAS[index]
                    if self.cartas[carta] >= 1:
                        break
                self.cartas[carta] -= 1
                mao.append(carta)
            return mao
        else:
            return False

    def familia(self, cartas):
        if sum([x for x in self.cartas.values()]) > 4:
            familia = ['j', 'q', 'k', 'a', 'coringa', 'espadas']
            if len([ 1 for x in cartas if x in familia]) == 3:
                return self.distribuir()
            else:
                return 'Não era uma família'
        else:
            return False

    def maiorCarta(self, cartas, cangado=True):
        cartas = [x for x in cartas]
        maior = self.CARTAS[max([self.CARTAS.index(x) for x in cartas], default=0)]
        if cartas.count(maior) >= 2 and cangado == True:
            return 'cangado'
        return maior

    def queimar(self, quantidade=1 ,escuro=False):
        if quantidade >= 4: quantidade = 3
        elif quantidade <= 0: quantidade = 1
        queima = [self.distribuir() for x in range(0, quantidade)]
        if escuro == False: return queima

class Jogador():
    def __init__(self, id, baralho):
        self.id = id
        self.cartas = []
        self.vitorias = 0
        self.roundVencido = []
        self.baralho = baralho

    def pedirFamilia(self):
        cartas = self.baralho.familia(self.cartas)
        if isinstance(cartas, list): self.cartas = cartas
        else: return cartas

    def jogar(self, carta):
        if carta in self.cartas:
            self.cartas.remove(carta)
            return carta
        else:
            return False

    def vencerRodada(self, rodada):
        self.vitorias += 1
        self.roundVencido.append(rodada)

    def embaralhar(self):
        print('embaralhando', end='')
        for x in range(0, 4):
            sleep(.3)
            print('.', end='')

    def zerar(self):
        self.vitorias = 0
        self.roundVencido = []
        self.cartas = []

class Round(Jogador):
    def __init__(self, jogadores, baralho, ordem):
        self.rodada = 0
        self.iniciarPartida = 0
        self.jogadores = jogadores
        self.baralho = baralho
        self.ordem = ordem
        self.acabou = False
        self.vencedor = 0
        self.pontosJogadores = []
        self.idTruco = 4
        self.truco = False
        self.quantidadePontos = 1

    def Truco(self, id):
        self.truco = True
        if self.quantidadePontos == 1:
            self.idTruco = id
            self.quantidadePontos = 3
            self.mostrar([f'Truco ({self.quantidadePontos})', 0 if self.idTruco % 2 == 0 else 1])
        #if (id % 2 == 0 and self.idTruco % 2 == 1) or (id % 2 == 1 and self.idTruco % 2 == 0):
        elif self.quantidadePontos < 12:
            self.idTruco += 1
            self.quantidadePontos += 3
            self.mostrar([f'Truco ({self.quantidadePontos})', 0 if self.idTruco % 2 == 0 else 1])

    def correr(self):
        #if (id % 2 == 0 and self.idTruco % 2 == 1) or (id % 2 == 1 and self.idTruco % 2 == 0):
        id = self.idTruco + 1
        if self.truco:
            if self.quantidadePontos == 3:
                self.quantidadePontos = 1
            else:
                self.quantidadePontos -= 3
            return {'id': 0 if id % 2 == 1 else 1, 'pontos': self.quantidadePontos}

    def verificarGanhador(self):
        pass

    def mostrar(self, txt):
        print('\033[1m=' * 45)
        if isinstance(txt, str):
            if isinstance(txt, list) and len(txt) == 1:
                txt = txt[0]
            print(f'{txt:^45}')
        else:
            i = 0
            for x in txt:
                print(f'{x:^45}')
                if i != len(txt) - 1: print('        ', f'-' * 29)
                i += 1
        print('\033[1m=' * 45, '\033[m')

    def Acabou(self):
        acabou = True if len([1 for x in self.jogadores if len(x.cartas) <= 0]) == 4 else False
        duplas = [[],[]]

        if acabou:
            for x in range(0, 4):
                duplas[0].append(self.jogadores[x].vitorias) if x % 2 == 0 else duplas[1].append(self.jogadores[x].vitorias)
            duplas = [sum(x) for x in duplas]
            vencedor = duplas.index(max(duplas))
            return {'id': vencedor, 'pontos': self.quantidadePontos}
        else:
            return False

    def roundCangado(self, cartas):
        maior = self.baralho.maiorCarta(cartas.values())
        if self.rodada == 1:
            return False if maior == 'cangado' else maior
        elif self.rodada == 3 or self.rodada == 2:
            return [x.id for x in cartas.keys() if 1 in x.roundVencido][0]

    def round(self):
        if self.acabou == False:
            self.rodada += 1
            print(f'\033[32mRound {self.rodada}\033[m')
            if self.rodada == 1:
                index = self.ordem
            else:
                index = self.iniciarPartida

            i = 0
            cartas = {}
            for x in self.jogadores:
                print(x.cartas, x.id)
            while True:
                self.mostrar(', '.join(self.jogadores[index].cartas))
                while True:
                    carta = str(input(f'jogue sua carta({index}): ')).lower()
                    if carta == 'truco':
                        self.Truco(self.jogadores[index].id)
                        continue
                    elif carta == 'correr':
                        if self.truco:
                            correr = self.correr()
                            if isinstance(correr, object):
                                return correr
                        else: print('\033[033mNão pode correr sem um Truco\033[m')
                    elif carta == 'familia' and self.rodada == 1:
                        self.jogadores[index].pedirFamilia()
                        self.mostrar(', '.join(self.jogadores[index].cartas))
                    elif carta in self.jogadores[index].cartas:
                        break
                    else:
                        print(f'\033[033mVocê não tem essa carta, jogue outra\033[m')

                self.jogadores[index].jogar(carta)
                cartas[self.jogadores[index]] = carta
                i += 1
                index += 1
                if index >= 4:
                    index = 0
                if i >= 4:
                    break

            maiorCarta = self.baralho.maiorCarta(cartas.values())
            if maiorCarta != 'cangado':
                vencedor = [k for k, x in cartas.items() if x == maiorCarta][0]
                print(f'o jogador {vencedor.id} ganhou com o {maiorCarta}')
                sleep(1.20)
                vencedor.vencerRodada(self.rodada)
                self.iniciarPartida = vencedor.id
                return self.Acabou()
            else:
                if self.rodada == 1:
                    self.mostrar('Cangou')
                    maioresCartas = [self.baralho.maiorCarta(x.cartas, False) for x in self.jogadores]
                    maiorCartaJogador = {}
                    index = 0

                    for x in maioresCartas:
                        maiorCartaJogador[self.jogadores[index]] = x
                        index += 1
                        if index >= 4:
                            index = 0

                    cartaGanhadora = self.roundCangado(maiorCartaJogador)
                    idGanhador = [k.id for k, x in maiorCartaJogador.items() if x == cartaGanhadora][0]
                    for x in self.jogadores:
                        x.zerar()
                    self.acabou = True
                    print(f'o jogador {idGanhador} ganhou com o {maiorCarta}')
                    sleep(1.20)
                    return {'id': 0 if idGanhador % 2 == 0 else 1, 'pontos': self.quantidadePontos}
                else:
                    for x in self.jogadores:
                        if 1 in x.roundVencido:
                            print(f'o jogador {x.id} ganhou com o {maiorCarta}')
                            sleep(1.20)
                            return {'id': 0 if x.id % 2 == 0 else 1, 'pontos': self.quantidadePontos}
        return False


class Jogo(Round):
    def __init__(self):
        self.baralho = Baralho()
        self.jogadores = [Jogador(x, self.baralho) for x in range(0, 4)]
        self.dupla = {'dupla 0': [self.jogadores[0], self.jogadores[2]], 'dupla 1': [self.jogadores[1], self.jogadores[3]]}
        self.pontos = {'pontos 0': 0, 'pontos 1': 0}
        self.quantidadePontos = 1

    def verificarGahou(self):
        if self.pontos['pontos 0'] >= 12: return 0
        elif self.pontos['pontos 1'] >= 12: return 1
        else: return False

    def marcarPonto(self, dupla):
        if self.verificarGahou() == False:
            self.pontos[f'pontos {dupla}'] += self.quantidadePontos
            if self.pontos[f'pontos {dupla}'] > 12:
                self.pontos[f'pontos {dupla}'] = 12
            self.quantidadePontos = 1
        else:
            self.quantidadePontos = 1
            if self.pontos[f'pontos {dupla}'] > 12:
                self.pontos[f'pontos {dupla}'] = 12
            return self.verificarGahou()

    def status(self):
        self.mostrar([f'Dupla 1: {self.pontos["pontos 0"]} pontos', f'Dupla 2: {self.pontos["pontos 1"]} pontos'])
        sleep(1.25)

b = Baralho()
jogo = Jogo()
ordem = 0
jogo.mostrar(['Comandos', 'familia, truco, correr, queimar'])
while True:
    baralho = Baralho()
    jogo.status()
    jogadores = [Jogador(x, baralho) for x in range(0, 4)]

    for x in jogadores:
        x.cartas = baralho.distribuir()

    round = Round(jogadores, baralho, ordem)

    for x in range(0, 3):
        vencedor = round.round()
        if vencedor != False:
            break

    id = 0 if vencedor['id'] % 2 == 0 else 1
    jogo.quantidadePontos = vencedor['pontos']
    jogo.marcarPonto(id)
    if jogo.verificarGahou() != False:
        jogo.mostrar(f'Dupla {jogo.verificarGahou()} Ganhou')
        break
    ordem += 1
    if ordem >= 4:
        ordem = 0
jogo.status()
