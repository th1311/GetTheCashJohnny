import asyncio
import random
import sys
import pygame

WEB = sys.platform == 'emscripten'
if WEB:
    import platform

WIDTH, HEIGHT = 1000, 700
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Get the Cash')
BG = pygame.transform.scale(pygame.image.load('figures/background.jpg'), (WIDTH, HEIGHT))
PLAYER = pygame.transform.scale(pygame.image.load('figures/Johann.jpg'), (50, 50))
OBSTACLE = pygame.transform.scale(pygame.image.load('figures/lgbt.png'), (40, 40))
CASH = pygame.transform.scale(pygame.image.load('figures/cash.jpg'), (31, 42))
FONT = pygame.font.Font(None, 36)
BIG = pygame.font.Font(None, 80)
try:
    pygame.mixer.music.load('audio/JohannTheme.mp3')
except pygame.error:
    pass


def new_round():
    return {'player': pygame.Rect(475, 325, 50, 50), 'x': 475.0, 'y': 325.0,
            'vx': 0, 'vy': 0, 'score': 0, 'elapsed': 0.0, 'stars': [], 'cash': [],
            'star_timer': 0.0, 'cash_timer': 0.0, 'star_interval': 2.0,
            'cash_interval': 2.0, 'state': 'ready'}


def update_hud(g):
    if WEB:
        platform.window.parent.cashUpdate(g['score'], int(g['elapsed']), g['state'])


async def main():
    g = new_round()
    clock = pygame.time.Clock()
    muted = False
    music_started = False
    update_hud(g)
    running = True
    while running:
        dt = min(clock.tick(0) / 1000.0, 0.05)
        command = ''
        if WEB:
            command = str(platform.window.parent.cashCommand)
            platform.window.parent.cashCommand = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    command = 'pause' if g['state'] == 'playing' else 'start'
                elif event.key == pygame.K_r:
                    command = 'restart'
                elif event.key == pygame.K_m:
                    command = 'mute'
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    g['vx'] = -300
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    g['vx'] = 300
                elif event.key in (pygame.K_UP, pygame.K_w):
                    g['vy'] = -300
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    g['vy'] = 300
        if command in ('start', 'restart'):
            if command == 'restart' or g['state'] in ('ready', 'over'):
                g = new_round()
            g['state'] = 'playing'
            if not music_started and not WEB:
                try:
                    pygame.mixer.music.play(-1, 177.0)
                    music_started = True
                except pygame.error:
                    try:
                        pygame.mixer.music.play(-1)
                        music_started = True
                    except pygame.error:
                        pass
        elif command == 'pause':
            if g['state'] == 'playing':
                g['state'] = 'paused'
            elif g['state'] == 'paused':
                g['state'] = 'playing'
        elif command == 'mute':
            muted = not muted
            if WEB:
                platform.window.parent.cashToggleSound()
            else:
                pygame.mixer.music.set_volume(0 if muted else 1)
        elif command in ('left', 'right', 'up', 'down'):
            if command == 'left': g['vx'] = -300
            if command == 'right': g['vx'] = 300
            if command == 'up': g['vy'] = -300
            if command == 'down': g['vy'] = 300
        if g['state'] == 'playing':
            g['elapsed'] += dt
            g['star_timer'] += dt
            g['cash_timer'] += dt
            if g['star_timer'] >= g['star_interval']:
                g['stars'].append(pygame.Rect(random.randint(30, 960), random.randint(20, 660), 40, 40))
                g['stars'] = g['stars'][-8:]
                g['star_timer'] = 0
                g['star_interval'] = max(.2, g['star_interval'] - .05)
            if g['cash_timer'] >= g['cash_interval']:
                for _ in range(2):
                    g['cash'].append(pygame.Rect(random.randint(30, 970), random.randint(20, 670), 30, 20))
                g['cash_timer'] = 0
                g['cash_interval'] = max(.2, g['cash_interval'] - .05)
            g['x'] += g['vx'] * dt
            g['y'] += g['vy'] * dt
            g['player'].topleft = (round(g['x']), round(g['y']))
            if g['x'] < 0 or g['x'] + 50 > WIDTH or g['y'] < 0 or g['y'] + 50 > HEIGHT:
                g['state'] = 'over'
            if any(g['player'].colliderect(s) for s in g['stars']):
                g['state'] = 'over'
            for item in g['cash'][:]:
                if g['player'].colliderect(item):
                    g['cash'].remove(item)
                    g['score'] += 1
                    break
        WIN.blit(BG, (0, 0))
        for item in g['cash']:
            WIN.blit(CASH, (item.x - 1, item.y - 11))
        for star in g['stars']:
            WIN.blit(OBSTACLE, star.topleft)
        WIN.blit(PLAYER, g['player'].topleft)
        if g['state'] != 'playing':
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((5, 12, 15, 180))
            WIN.blit(shade, (0, 0))
            title = {'ready': 'GET THE CASH', 'paused': 'PAUSED', 'over': 'GAME OVER'}[g['state']]
            subtitle = {'ready': 'Collect cash. Dodge obstacles. Stay inside.', 'paused': 'Press Space to continue', 'over': f"${g['score']} collected  /  {int(g['elapsed'])} seconds"}[g['state']]
            text = BIG.render(title, True, (218, 255, 90))
            WIN.blit(text, (500-text.get_width()/2, 290))
            text = FONT.render(subtitle, True, 'white')
            WIN.blit(text, (500-text.get_width()/2, 385))
        pygame.display.flip()
        update_hud(g)
        await asyncio.sleep(0)
    pygame.quit()

asyncio.run(main())
