# terra_nova_full_images.py
import pygame
import sys
import random

# --- SETTINGS ---
WIDTH, HEIGHT = 800, 500
FPS = 60

# --- INIT ---
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Terra Nova: The Game")
clock = pygame.time.Clock()

# --- ASSET PATHS ---
BG_LOADING = r"env_game\assets\images\background\Terra Nova Loading Page.jpg"
NPC_2125_IMG = r"env_game\assets\images\npc\NPC 2125.png"
NPC_2025_IMG = r"env_game\assets\images\npc\NPC 2025.png"

TRASH_1 = r"env_game\assets\images\trash\Trash 1.png"
TRASH_2 = r"env_game\assets\images\trash\Trash 2.png"
TRASH_3 = r"env_game\assets\images\trash\Trash 3.png"

TREE_1 = r"env_game\assets\images\tree\Tree 1.png"
TREE_2 = r"env_game\assets\images\tree\Tree 2.png"
TREE_3 = r"env_game\assets\images\tree\Tree 3.png"
TREE_4 = r"env_game\assets\images\tree\Tree 4.png"

# Music
MUSIC_2125 = r"env_game\assets\sounds\Cycle of Ruin (Dynamic Game BGM).mp3"
MUSIC_2025 = r"env_game\assets\sounds\Where Green Returns (Softened Highs).mp3"

# Flashback Scenes
Scene_1 = r"env_game\assets\images\background\Background Healthy Earth.jpg"
Scene_2 = r"env_game\assets\images\background\cute animals.jpg"
Scene_3 = r"env_game\assets\images\background\grey.jpg"
Scene_4 = r"env_game\assets\images\background\drying river.jpg"
Scene_5 = r"env_game\assets\images\background\grenery 2025.jpg"
Scene_6 = r"env_game\assets\images\background\Healthy Forest.jpg"
Scene_7 = r"env_game\assets\images\background\Smoking Factory.png"
Scene_8 = r"env_game\assets\images\background\tiger 2025.jpg"
Scene_9 = r"env_game\assets\images\background\wasteland 2125.jpg"
Scene_10 = r"env_game\assets\images\background\Wasteland.jpg"

# --- LOAD ASSETS ---
background = pygame.image.load(BG_LOADING)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# NPC faces
npc_2125 = pygame.image.load(NPC_2125_IMG).convert_alpha()
npc_2125 = pygame.transform.scale(npc_2125, (70, 70))

try:
    npc_2025 = pygame.image.load(NPC_2025_IMG).convert_alpha()
    npc_2025 = pygame.transform.scale(npc_2025, (70, 70))
except Exception:
    npc_2025 = npc_2125  # fallback

# Trash sprites
trash_images = [
    pygame.transform.scale(pygame.image.load(TRASH_1).convert_alpha(), (32, 32)),
    pygame.transform.scale(pygame.image.load(TRASH_2).convert_alpha(), (32, 32)),
    pygame.transform.scale(pygame.image.load(TRASH_3).convert_alpha(), (32, 32)),
]
# Tree sprites
tree_images = [TREE_1, TREE_2, TREE_3, TREE_4]
# Bigger size, e.g., 60x60
tree_sprites = [pygame.transform.scale(pygame.image.load(p).convert_alpha(), (60, 60)) for p in tree_images]

# --- COLORS & FONTS ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
BLUE = (0, 150, 255)
BROWN = (139, 69, 19)

font = pygame.font.SysFont("Tempus Sans ITC", 30, bold=True)
button_font = pygame.font.SysFont("Algerian", 36, bold=False)

# --- MENU BUTTON ---
menu = True
button_w, button_h = 150, 50
button_x = WIDTH // 2 - button_w // 2
button_y = HEIGHT // 2 + 50
button_rect = pygame.Rect(button_x, button_y, button_w, button_h)
button_color = (64, 224, 208)
hover_color = (72, 239, 227)
outline_gap = 4
BUTTON_BORDER_RADIUS = 15

# --- GAME STATE ---
stage = "menu"
score = 0
npc_dialogue = "Welcome! I am your guide. Let’s heal the Earth together."
show_score = False

# --- STAGE 1 SETUP (Wastewater) ---
water_rect = pygame.Rect(0, 100, WIDTH, HEIGHT - 200)
trash_list = []
for _ in range(8):
    x = random.randint(water_rect.left, water_rect.right - 32)
    y = random.randint(water_rect.top, water_rect.bottom - 32)
    img = random.choice(trash_images)
    rect = img.get_rect(topleft=(x, y))
    trash_list.append({"rect": rect, "img": img})

# --- STAGE 2 SETUP (Afforestation) ---
seeds = [pygame.Rect(x, 300, 20, 30) for x in range(150, 700, 100)]
planted = [False] * len(seeds)
planted_trees = [None] * len(seeds)  # same length as seeds

# --- STORY SCRIPT WITH BACKGROUNDS ---
story_script = [
    ("Guide (2125)", "Traveler… welcome to Earth, Year 2125.", None, "normal", r"env_game\assets\images\background\wasteland 2125.jpg"),
    ("Guide (2125)", "This is what remains of the world...", None, "normal", r"env_game\assets\images\background\Wasteland.jpg"),
    ("Guide (2125)", "But this is not how Earth was always meant to be. Let me show you… a memory.", "to_2025", "normal", r"env_game\assets\images\background\Healthy Forest.jpg"),
    
    ("Narrator", "(The screen distorts...colors warm, soft focus)", None, "flashback", r"env_game\assets\images\background\greenery 2025.jpg"),
    ("2025 NPC", "Oh! A traveler? You look… different.", None, "flashback", r"env_game\assets\images\background\tiger 2025.jpg"),
    ("2025 NPC", "This is 2025, and Earth is alive, breathing...", None, "flashback", r"env_game\assets\images\background\Background Healthy Earth.jpg"),
    ("2025 NPC", "Promise me… if you’re from the future, protect this Earth.", None, "flashback", r"env_game\assets\images\background\cute animals.jpg"),
    
    ("Narrator", "(Flashback fades. Colors drain back to gray.)", "to_2125", "normal", r"env_game\assets\images\background\grey.jpg"),
    ("Guide (2125)", "That was Earth in 2025 — bright, full of hope.", None, "normal", r"env_game\assets\images\background\drying river.jpg"),
    ("Guide (2125)", "Now look around you: forests turned to ash...", None, "normal", r"env_game\assets\images\background\Smoking Factory.png"),
    ("Guide(2125)", "Let's give a shot to save the Earth, protect it, revive it; ONE STEP AT A TIME", None, "normal", r"env_game\assets\images\background\Smoking Factory.png")
]

story_index = 0
_last_music_hint = None

# --- PRELOAD STORY BACKGROUNDS ---
story_bg_images = {}
for entry in story_script:
    path = entry[4]
    if path not in story_bg_images:
        img = pygame.image.load(path)
        story_bg_images[path] = pygame.transform.scale(img, (WIDTH, HEIGHT))

# --- UTILITY FUNCTIONS ---
def draw_text(text, x, y, color=BLACK, size=28, center=False):
    f = pygame.font.SysFont("Tempus Sans ITC", size, bold=True)
    surf = f.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)

def draw_dialogue_box(speaker, line, face_img=None, visual_mode="normal"):
    if visual_mode == "flashback":
        warm_overlay = pygame.Surface((WIDTH, HEIGHT))
        warm_overlay.fill((255, 200, 150))
        warm_overlay.set_alpha(60)
        screen.blit(warm_overlay, (0, 0))
    box_rect = pygame.Rect(20, HEIGHT - 120, WIDTH - 40, 100)
    pygame.draw.rect(screen, GRAY, box_rect, border_radius=8)
    if face_img is not None:
        screen.blit(face_img, (30, HEIGHT - 110))
    draw_text(f"{speaker}", 110, HEIGHT - 110, color=BLACK, size=20)
    draw_text(line, 110, HEIGHT - 80, color=BLACK, size=18)

def safe_music_load(path, volume=0.5, loop=-1):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loop)
        pygame.mixer.music.set_volume(volume)
    except Exception as e:
        print("Music load/play failed:", path, e)

# --- GAME STAGE FUNCTIONS ---
def wastewater_stage():
    global npc_dialogue
    screen.fill(WHITE)
    draw_text("Stage 1: Wastewater Treatment", 250, 20, BLUE)
    draw_text("Click the trash to clean the water!", 200, 60, BLACK)
    pygame.draw.rect(screen, BLUE, water_rect)
    for trash in trash_list:
        screen.blit(trash["img"], trash["rect"])
    pygame.draw.rect(screen, GRAY, (20, HEIGHT-100, WIDTH-40, 80))
    screen.blit(npc_2125, (30, HEIGHT-90))
    draw_text(npc_dialogue, 110, HEIGHT-70, BLACK)
    draw_text(f"Score: {score}", 20, 20, BLACK)

def afforestation_stage():
    global npc_dialogue
    screen.fill(WHITE)
    draw_text("Stage 2: Afforestation", 280, 20, GREEN)
    draw_text("Click on spots to plant trees!", 250, 60, BLACK)
    pygame.draw.rect(screen, BROWN, (0, 350, WIDTH, 250))
    for i, seed in enumerate(seeds):
        if planted[i] and planted_trees[i] is not None:
            # Draw tree on the brown land
            tree_width, tree_height = planted_trees[i].get_size()
            screen.blit(planted_trees[i], (seed.x + seed.width//2 - tree_width//2, 350 - tree_height))
        else:
            pygame.draw.ellipse(screen, (160, 82, 45), seed)  # brown oval


# --- MAIN LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # MENU CLICK
            if stage == "menu":
                if button_rect.collidepoint(mouse_pos):
                    safe_music_load(MUSIC_2125, 0.5)
                    stage = "story"
                    story_index = 0
                    _last_music_hint = None
            # STORY CLICK
            elif stage == "story":
                story_index += 1
                if story_index >= len(story_script):
                    safe_music_load(MUSIC_2125, 0.5)
                    stage = "stage1"
                    npc_dialogue = "This river is polluted. Let’s clean it!"
                if story_index >= 10:  # index of that dialogue line
                    show_score = True
            # STAGE 1 CLICK
            elif stage == "stage1":
                for trash in trash_list[:]:
                    if trash["rect"].collidepoint(mouse_pos):
                        trash_list.remove(trash)
                        score += 10
                        npc_dialogue = "Good job! Keep going!"
                if not trash_list:
                    stage = "stage2"
                    npc_dialogue = "Now let’s grow a forest!"
    # --- STAGE 2 CLICK HANDLING ---
            elif stage == "stage2":
                for i, seed in enumerate(seeds):
                    if seed.collidepoint(mouse_pos) and not planted[i]:
                        planted[i] = True
                        # Pick a random tree sprite
                        planted_trees[i] = random.choice(tree_sprites)
                        score += 15
                        npc_dialogue = "Tree planted! Great work!"

                if all(planted):
                    npc_dialogue = "You restored greenery! Earth is healing!"
                    safe_music_load(MUSIC_2025, 0.6)
                    stage = "end"

    # --- DRAW ---
    screen.fill(WHITE)
    if stage == "menu":
        screen.blit(background, (0,0))
        outline_rect = button_rect.inflate(outline_gap, outline_gap)
        pygame.draw.rect(screen, BLACK, outline_rect, border_radius=BUTTON_BORDER_RADIUS)
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, hover_color, button_rect, border_radius=BUTTON_BORDER_RADIUS)
        else:
            pygame.draw.rect(screen, button_color, button_rect, border_radius=BUTTON_BORDER_RADIUS)
        button_text = button_font.render("START!", True, WHITE)
        screen.blit(button_text, button_rect)
    elif stage == "story":
        speaker, line, music_hint, visual_mode, bg_img_path = story_script[story_index]
        screen.blit(story_bg_images[bg_img_path], (0,0))
        # music switching
        if music_hint is not None and music_hint != _last_music_hint:
            if music_hint == "to_2025":
                safe_music_load(MUSIC_2025, 0.55)
            elif music_hint == "to_2125":
                safe_music_load(MUSIC_2125, 0.5)
            _last_music_hint = music_hint
        face_img = npc_2025 if "2025" in speaker else npc_2125
        draw_dialogue_box(speaker, line, face_img=face_img, visual_mode=visual_mode)
        draw_text("Click to continue...", WIDTH-180, HEIGHT-40, WHITE, 16)
    elif stage == "stage1":
        wastewater_stage()
    elif stage == "stage2":
        afforestation_stage()
    elif stage == "end":
        screen.fill((18,90,60))
        draw_text("Congratulations!", WIDTH//2, HEIGHT//2 - 40, WHITE, 36, center=True)
        draw_text("You are restoring greenery. Earth is beginning to heal. (Game still under development)", WIDTH//2, HEIGHT//2 + 10, WHITE, 20, center=True)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
