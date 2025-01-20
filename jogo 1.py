import pygame
import random
import time

# Inicialização do Pygame
pygame.init()

# Definir dimensões da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Definir cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Definir FPS
clock = pygame.time.Clock()
FPS = 60

# Função para carregar recursos (imagens e sons)
def load_image(image_path):
    try:
        return pygame.image.load(image_path)
    except pygame.error as e:
        print(f"Erro ao carregar a imagem {image_path}: {e}")
        return None

def load_sound(sound_path):
    return pygame.mixer.Sound(sound_path)

# Função para ajustar o tamanho da imagem à tela
def scale_image(image, width, height):
    return pygame.transform.scale(image, (width, height))

# Função para carregar a imagem do fundo
def load_background(image_path):
    background = load_image(image_path)
    if background is not None:
        return scale_image(background, screen_width, screen_height)
    else:
        return pygame.Surface((screen_width, screen_height))

# Função para carregar a imagem do personagem
def load_player_image(image_path):
    return load_image(image_path)

# Função para carregar a imagem do inimigo
def load_enemy_image(image_path):
    return load_image(image_path)

# Função para carregar a imagem da explosão
def load_explosion_image(image_path):
    return load_image(image_path)

# Sons
pygame.mixer.music.load('musica_fundo.mp3')  # Música de fundo
pygame.mixer.music.set_volume(0.5)

# Carregar som de tiro
shoot_sound = load_sound('tiro.mp3')
shoot_sound.set_volume(0.5)

# Carregar som de explosão
explosion_sound = load_sound('explosao.mp3')
explosion_sound.set_volume(0.5)

# Carregar som de coleta de power-up
powerup_sound = load_sound('powerup.mp3')
powerup_sound.set_volume(0.5)

# Classe da explosão
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_explosion_image('explosao.png')  # Imagem da explosão
        self.image = scale_image(self.image, 50, 50)  # Ajustando tamanho
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.duration = 30  # Duração da explosão em frames
    
    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.kill()  # Remove a explosão após a duração

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_player_image('player_1.png')  # Imagem do personagem
        self.image = scale_image(self.image, 50, 50)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed = 5
        self.health = 100
        self.xp = 0
        self.level = 1
        self.shoot_cooldown = 0

    def update(self):
        keys = pygame.key.get_pressed()

        # Movimentação com as teclas A, W, S, D
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed  # Mover para a esquerda
        if keys[pygame.K_d] and self.rect.right < screen_width:
            self.rect.x += self.speed  # Mover para a direita
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed  # Mover para cima
        if keys[pygame.K_s] and self.rect.bottom < screen_height:
            self.rect.y += self.speed  # Mover para baixo
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self):
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()  # Reproduzir o som do tiro
            self.shoot_cooldown = 20  # Cooldown de 20 frames

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()  # Remove o personagem quando morrer
            return True
        return False

# Classe do tiro
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Classe do inimigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_enemy_image('inimigo.png')
        self.image = scale_image(self.image, 50, 50)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 50)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - 50)
            self.rect.y = random.randint(-100, -40)

# Criar grupos de sprites
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
explosions = pygame.sprite.Group()

# Criar o jogador
player = Player()
all_sprites.add(player)

# Criar inimigos
for i in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Variáveis de controle do jogo
score = 0
font = pygame.font.SysFont('Arial', 30)

# Função para reiniciar o jogo
def restart_game():
    global player, all_sprites, bullets, enemies, score
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    score = 0
    for i in range(5):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

# Tela de Carregamento (barra de progresso)
def display_loading_screen(progress):
    screen.fill(BLACK)
    font = pygame.font.SysFont('Arial', 40)
    loading_text = font.render('Carregando...', True, WHITE)
    loading_rect = loading_text.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
    screen.blit(loading_text, loading_rect)

    # Barra de progresso
    pygame.draw.rect(screen, WHITE, (screen_width // 4, screen_height // 2, screen_width // 2, 30))
    pygame.draw.rect(screen, GREEN, (screen_width // 4, screen_height // 2, (screen_width // 2) * progress, 30))  # Progresso
    
    pygame.display.flip()

# Função de carregamento
def load_resources():
    resources = [
        'espaço.png', 'player_1.png', 'inimigo.png', 'explosao.png', 'musica_fundo.mp3', 'tiro.mp3', 'explosao.mp3'
    ]
    total_resources = len(resources)
    loaded = 0
    for resource in resources:
        if resource.endswith('.png'):
            load_image(resource)
        elif resource.endswith('.mp3'):
            load_sound(resource)
        loaded += 1
        display_loading_screen(loaded / total_resources)  # Atualiza a barra de progresso
        pygame.time.wait(100)  # Simula um pequeno atraso para o carregamento dos recursos

# Tela inicial (logo e mensagem "Press Start to Play")
def display_start_screen():
    start_font = pygame.font.SysFont('Arial', 50)
    start_text = start_font.render('Press Start to Play', True, WHITE)
    start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
    
    # Exibir fundo
    logo_image = pygame.image.load('logo.png')  # Tente carregar a imagem da logo
    logo_image = scale_image(logo_image, screen_width, screen_height)  # Ajusta para tela cheia
    screen.blit(logo_image, (0, 0))
    
    screen.blit(start_text, start_text_rect)
    pygame.display.flip()

# Carregar fundo inicial
espaço_image = load_background('espaço.png')  # Tente carregar o fundo

# Carregar recursos antes de começar o jogo
load_resources()

# Loop principal do jogo
pygame.mixer.music.play(-1)  # Reproduzir música de fundo em loop
running = True
game_over = False
show_start_screen = True

while running:
    if show_start_screen:
        display_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Pressione ENTER para começar o jogo
                    show_start_screen = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

    else:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.shoot()
                elif event.key == pygame.K_r and game_over:
                    restart_game()
                    game_over = False

        # Atualizar
        all_sprites.update()

        # Verificar colisões de tiros com inimigos
        for bullet in bullets:
            enemy_hit = pygame.sprite.spritecollide(bullet, enemies, True)
            if enemy_hit:
                bullet.kill()
                score += 10
                explosion_sound.play()  # Som de explosão
                for _ in enemy_hit:
                    explosion = Explosion(bullet.rect.centerx, bullet.rect.centery)
                    all_sprites.add(explosion)
                    explosions.add(explosion)
                    
                    # Criar novo inimigo
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)

        # Verificar colisões do jogador com inimigos
        if pygame.sprite.spritecollide(player, enemies, False):
            if player.hit(10):  # Reduz a vida do jogador quando colide
                game_over = True
                explosion = Explosion(player.rect.centerx, player.rect.centery)
                all_sprites.add(explosion)

        # Desenhar
        screen.blit(espaço_image, (0, 0))  # Desenha o fundo
        all_sprites.draw(screen)

        # Exibir informações
        score_text = font.render(f'Pontos: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        lives_text = font.render(f'Vidas: {player.health}', True, WHITE)
        screen.blit(lives_text, (screen_width - 150, 10))

        if game_over:
            game_over_text = font.render('GAME OVER', True, RED)
            screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 30))
            restart_text = font.render('Pressione R para Reiniciar', True, WHITE)
            screen.blit(restart_text, (screen_width // 2 - 150, screen_height // 2 + 30))

        pygame.display.flip()

pygame.quit()
