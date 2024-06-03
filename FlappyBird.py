import pygame  # Importa a biblioteca Pygame para criar o jogo
import os  # Importa a biblioteca os para manipular caminhos de arquivos
import random  # Importa a biblioteca random para gerar números aleatórios

# Define as dimensões da tela do jogo
TELA_LARGURA = 500
TELA_ALTURA = 800

# Carrega e redimensiona as imagens usadas no jogo
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

# Inicializa as fontes para exibir texto na tela
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)
FONTE_MENSAGEM = pygame.font.SysFont('arial', 60)

class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        # Define a velocidade para o pássaro "pular" (ir para cima)
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # Atualiza a posição do pássaro com base na física do jogo
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # Limita o deslocamento máximo para evitar que o pássaro caia muito rápido
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # Controla o ângulo do pássaro para parecer que ele está voando ou caindo
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # Animação do pássaro (bate as asas)
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # Mantém a asa para cima quando o pássaro estiver caindo rápido
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # Desenha o pássaro na tela com a rotação apropriada
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        # Retorna a máscara para a detecção de colisão
        return pygame.mask.from_surface(self.imagem)

class Cano:
    DISTANCIA = 200  # Distância entre os canos superior e inferior
    VELOCIDADE = 5  # Velocidade de movimento dos canos

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False  # Indica se o pássaro já passou pelo cano
        self.definir_altura()

    def definir_altura(self):
        # Define a altura dos canos de forma aleatória
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        # Move os canos para a esquerda
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        # Desenha os canos na tela
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        # Verifica a colisão entre o pássaro e os canos usando máscaras
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False
class Chao:
    VELOCIDADE = 5  # Velocidade de movimento do chão
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        # Move o chão para a esquerda, criando um efeito de movimento contínuo
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        # Reseta a posição do chão quando ele sai da tela
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        # Desenha o chão na tela
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos, pausado):
    # Desenha todos os elementos do jogo na tela
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    # Desenha a pontuação
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)

    # Se o jogo estiver pausado, desenha a mensagem de pausa
    if pausado:
        texto_pausa = FONTE_MENSAGEM.render("PAUSADO", 1, (255, 0, 0))
        tela.blit(texto_pausa, (TELA_LARGURA // 2 - texto_pausa.get_width() // 2, TELA_ALTURA // 2 - texto_pausa.get_height() // 2))

    pygame.display.update()

def mostrar_mensagem(tela, mensagem):
    # Mostra uma mensagem temporária na tela (por exemplo, ao perder o jogo)
    texto = FONTE_MENSAGEM.render(mensagem, 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA // 2 - texto.get_width() // 2, TELA_ALTURA // 2 - texto.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)
