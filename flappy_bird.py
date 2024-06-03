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