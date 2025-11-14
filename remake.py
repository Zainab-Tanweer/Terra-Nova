import pygame
import sys
import random

# --- SETTINGS ---
WIDTH, HEIGHT = 800, 500
FPS = 60

# --- INIT ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Terra Nova: The Game")
pygame.mixer.init()
clock = pygame.time.Clock()

# --- LOAD ASSETS ---
background = pygame.image.load("env_game\\assets\\images\\background\\Terra Nova Loading Page.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
BLUE = (0, 150, 255)
BROWN = (139, 69, 19)

# Fonts
font = pygame.font.SysFont("Tempus Sans ITC", 30, bold=True)
button_font = pygame.font.SysFont("Algerian", 36, bold=False)

# --- Menu variables ---
menu = True
button_width, button_height = 150, 50
button_x = WIDTH//2 - button_width//2
button_y = HEIGHT//2 + 50
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
button_color = (64, 224, 208)
hover_color = (72, 239, 227)
WHITE = (255, 255, 255)

# --- Game variables ---
stage = 0   # 0 = intro, 1 = wastewater, 2 = afforestation
score = 0
npc_dialogue = "Welcome! I am your guide. Let’s heal the Earth together."

# --- Stage 1: Wastewater ---
trash_images = [
    pygame.transform.scale(pygame.image.load("env_game\\assets\\images\\trash\\Trash 1.png").convert_alpha(), (32, 32)),
    pygame.transform.scale(pygame.image.load("env_game\\assets\\images\\trash\\Trash 2.png").convert_alpha(), (32, 32)),
    pygame.transform.scale(pygame.image.load("env_game\\assets\\images\\trash\\Trash 3.png").convert_alpha(), (32, 32))
]

trash_list = []
water_rect = pygame.Rect(0, 100, WIDTH, HEIGHT-200)
npc_face = pygame.image.load("env_game\\assets\\images\\npc\\NPC 2125.png").convert_alpha()
npc_face = pygame.transform.scale(npc_face, (70, 70))

for _ in range(8):
    x = random.randint(water_rect.left, water_rect.right - 32)
    y = random.randint(water_rect.top, water_rect.bottom - 32)
    img = random.choice(trash_images)
    rect = img.get_rect(topleft=(x, y))
    trash_list.append({"rect": rect, "img": img})

# --- Stage 2: Afforestation ---
seeds = [pygame.Rect(x, 300, 20, 20) for x in range(150, 700, 100)]
planted = [False] * len(seeds)

# --- Functions ---
def draw_text(text, x, y, color=BLACK, size=30, center=False):
    font2 = pygame.font.SysFont("Tempus Sans ITC", size, bold=True)
    label = font2.render(text, True, color)
    rect = label.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(label, rect)

def wastewater_stage():
    global stage, score, npc_dialogue
    screen.fill(WHITE)
    draw_text("Stage 1: Wastewater Treatment", 250, 20, BLUE)
    draw_text("Click the trash to clean the water!", 200, 60, BLACK)
    pygame.draw.rect(screen, BLUE, water_rect)
    for trash in trash_list:
        screen.blit(trash["img"], trash["rect"])
    pygame.draw.rect(screen, GRAY, (20, HEIGHT-100, WIDTH-40, 80))
    screen.blit(npc_face, (30, HEIGHT-90))
    draw_text(npc_dialogue, 110, HEIGHT-70, BLACK)
    draw_text(f"Score: {score}", 20, 20, BLACK)

def afforestation_stage():
    global stage, score, npc_dialogue
    screen.fill(WHITE)
    draw_text("Stage 2: Afforestation", 280, 20, GREEN)
    draw_text("Click on spots to plant trees!", 250, 60, BLACK)
    pygame.draw.rect(screen, BROWN, (0, 350, WIDTH, 250))
    for i, seed in enumerate(seeds):
        if planted[i]:
            pygame.draw.rect(screen, GREEN, pygame.Rect(seed.x, seed.y-40, 40, 40))
        else:
            pygame.draw.rect(screen, (160, 82, 45), seed)
    pygame.draw.rect(screen, GRAY, (20, HEIGHT-100, WIDTH-40, 80))
    draw_text(npc_dialogue, 40, HEIGHT-80, BLACK)
    draw_text(f"Score: {score}", 20, 20, BLACK)

# --- MAIN LOOP ---
while True:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if menu:
                # Start button click
                if button_rect.collidepoint(mouse_pos):
                    menu = False
                    stage = 0
                    npc_dialogue = "Welcome! I am your guide. Let’s heal the Earth together."
                    pygame.mixer.music.load("env_game\\assets\\sounds\\Cycle of Ruin (Dynamic Game BGM).mp3")
                    pygame.mixer.music.play(-1)  # -1 means loop forever
                    pygame.mixer.music.set_volume(0.5)  # optional, 0.0 to 1.0    
            else:
                # Click to move through stages
                if stage == 0:
                    stage = 1
                    npc_dialogue = "This river is polluted. Let’s clean it!"
                elif stage == 1:
                    for trash in trash_list[:]:
                        if trash["rect"].collidepoint(mouse_pos):
                            trash_list.remove(trash)
                            score += 10
                            npc_dialogue = "Good job! Keep going!"
                    if not trash_list:
                        stage = 2
                        npc_dialogue = "Now let’s grow a forest!"
                elif stage == 2:
                    for i, seed in enumerate(seeds):
                        if seed.collidepoint(mouse_pos) and not planted[i]:
                            planted[i] = True
                            score += 15
                            npc_dialogue = "Tree planted! Great work!"
                    if all(planted):
                        npc_dialogue = "You restored greenery! Earth is healing!"
                        pygame.mixer.music.load("env_game\\assets\\sounds\\Where Green Returns (Softened Highs).mp3")
                        pygame.mixer.music.play(-1)  # loop it too
                        pygame.mixer.music.set_volume(0.6)  # slightly louder for effect

    # --- DRAW ---
    if menu:
        screen.blit(background, (0, 0))
        outline_rect = button_rect.inflate(4, 4)
        pygame.draw.rect(screen, BLACK, outline_rect, border_radius=15)
        # button hover effect
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, hover_color, button_rect, border_radius=15)
        else:
            pygame.draw.rect(screen, button_color, button_rect, border_radius=15)
        button_text = button_font.render("START!", True, WHITE)
        screen.blit(button_text, button_rect)

    else:
        # Stage rendering
        if stage == 0:
            screen.fill(WHITE)
            draw_text("Heal the Earth 2125", 400, 200, BLACK, 32, center=True)
            draw_text("Click anywhere to begin!", 400, 260, BLACK, 24, center=True)
            pygame.draw.rect(screen, GRAY, (20, HEIGHT-100, WIDTH-40, 80))
            draw_text(npc_dialogue, 40, HEIGHT-80, BLACK)
        elif stage == 1:
            wastewater_stage()
        elif stage == 2:
            afforestation_stage()

    pygame.display.flip()
    clock.tick(FPS)