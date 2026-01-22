# Collect Blocks
# Author: Ubial
# 7 January 2026

import pygame
import random

# COLOURS - (R, G, B)
# CONSTANTS ALL HAVE CAPS FOR THEIR NAMES
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
GREY  = (128, 128, 128)
PINK = (255, 182, 193)

# Ending Scene
class Block(pygame.sprite.Sprite):
    def __init__(self, colour: pygame.Color, width: int, height: int):
        """A block of any colour"""
        super().__init__()

        # Visual representation of our image
        self.image = pygame.Surface((width, height))
        # change the colour of self.image
        self.image.fill(colour)

        # A Rect tells you two things:
        #   - how big the hitbox is (width, height)
        #   - where it is (x, y)
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 100

        self.point_value = 1


    def level_up(self, val: int):
        """Incr point value"""
        self.point_value *= val

# Energy is a special element that the player can collect
# Players need to consume energy to defend themself from the fire
class Energy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/star_transparent.png")
        self.image = pygame.transform.scale_by(self.image, 0.025)
        self.rect = self.image.get_rect()

    def spawn_energy(amount, all_sprites, energy_group):
        for _ in range(amount):
            energy = Energy()
            all_sprites.add(energy)
            energy_group.add(energy)

# Each shield takes 2 energy
# Shield can defend fire's attack
class Shield(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        self.player = player  # reference to Mario

        self.image = pygame.image.load("assets/shield.png")
        self.image = pygame.transform.scale_by(self.image, 0.09)
        self.image.set_alpha(90)

        self.rect = self.image.get_rect()

    def update(self):
        # Always stay centered on the player
        self.rect.center = self.player.rect.center

# Fire will appear randomly form the screen
# Player have to use shield to defend or escape
# class Fire(pygame.sprite.Sprite):



class Mario(pygame.sprite.Sprite):
    def __init__(self):
        """The player"""
        super().__init__()

        # Right version of Mario and Left version
        self.image_right =  pygame.image.load("assets/mario-snes.png")
        self.image_right = pygame.transform.scale_by(self.image_right, 0.5)
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        self.image = self.image_right
        self.rect = self.image.get_rect()

        self.previous_x = 0               # help with direction
        self.health = 100
        self.points = 0
        self.energy = 0
        self.shield_active = False
        self.shield_timer = 0
        self.speed = 7.5




    def calc_damage(self, amt: int) -> int:
        """Decrease player health by amt
        Returns:
            Remaining health"""
        self.health -= amt
        return self.health

    def incr_score(self, amt: int) -> int:
        """Increases player score by amt
        Returns:
            Score"""
        self.points += amt
        return self.points

    def get_damage_percentage(self) -> float:
        return self.health / 100

    def update(self):
        """Update Mario's location based on the mouse pos
        Update Mario's image based on where he's going"""
        # W, S, A, D
        # Control direction of moving
        keys = pygame.key.get_pressed()

        # Left
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.image = self.image_left
        # Right
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.image = self.image_right
        # Up
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        # Down
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(800, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(600, self.rect.bottom)

        # If Mario's previous x less than current x
        #   Then Mario is facing Right
        # If Mario's previous x is greater than current x
        #   Then Mario is facing Left
        if self.previous_x < self.rect.x:
            self.image = self.image_right
        elif self.previous_x > self.rect.x:
            self.image = self.image_left

        self.previous_x = self.rect.x

        # Shield countdown
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
                print("Shield expired")

    # Update method for player to collect energy
    def collect_energy(self, amt:int):
        self.energy += amt

    # Consume energy to use shield
    def activate_shield(self):
        SHIELD_COST = 5
        SHIELD_DURATION = 60

        if self.energy >= SHIELD_COST and not self.shield_active:
            self.energy -= SHIELD_COST
            self.shield_active = True
            self.shield_timer = SHIELD_DURATION
            print("Shield activated!")




class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/goomba-nes.png")
        self.rect = self.image.get_rect()

        self.vel_x = 0
        self.vel_y = 0

        self.damage = 1

    def update(self):
        # movement in the x- and y-axis
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def level_up(self):
        # increase damage
        self.damage *= 2

class HealthBar(pygame.Surface):
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        super().__init__((width, height))

        self.fill(RED)

    def update_info(self, percentage: float):
        """Updates the healthbar with the given percentage"""
        self.fill(RED)
        pygame.draw.rect(self, GREEN, (0, 0, percentage * self._width, self._height))

def game():
    pygame.init()

    # BACKGROUND MUSIC
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load("assets/background_music.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    # CONSTANTS
    WIDTH = 800
    HEIGHT = 600
    STAR_MARGIN_RIGHT = 10
    STAR_MARGIN_TOP = 10
    SIZE = (WIDTH, HEIGHT)

    # Creating the Screen
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Collect Blocks")
    star_icon = pygame.image.load("assets/star_transparent.png")
    star_icon = pygame.transform.scale_by(star_icon, 0.4)

    # Energy counter
    star_icon = pygame.image.load("assets/star_transparent.png").convert_alpha()
    star_icon = pygame.transform.scale_by(star_icon, 0.05)

    STAR_MARGIN_RIGHT = 10
    STAR_MARGIN_TOP = 10

    star_rect = star_icon.get_rect()
    star_rect.topright = (WIDTH - STAR_MARGIN_RIGHT, STAR_MARGIN_TOP)


    # Variables
    done = False
    clock = pygame.time.Clock()
    num_enemies = 8
    num_blocks = 100
    health_bar = HealthBar(200, 10)
    level = 1
    font = pygame.font.SysFont(None, 40)

    # Create a Sprite Group
    all_sprites_group = pygame.sprite.Group()
    block_sprites_group = pygame.sprite.Group()
    enemy_sprites_group = pygame.sprite.Group()
    energy_sprites_group = pygame.sprite.Group()


    # Create Energy on the screen randomly
    energy_amt = 10

    for _ in range(energy_amt):
        energy = Energy()
        energy.rect.center = (random.randrange(0, WIDTH), random.randrange(0,HEIGHT))
        all_sprites_group.add(energy)
        energy_sprites_group.add(energy)


    # Create Enemies
    for _ in range(num_enemies):
        # Create an enemy
        enemy = Enemy()
        # Randomize movement
        random_x = random.choice([-5, -3, -1, 1, 3, 5])
        random_y = random.choice([-5, -3, -1, 1, 3, 5])
        enemy.vel_x, enemy.vel_y = random_x, random_y
        # Start them in the middle
        enemy.rect.center = (random.randrange(0, WIDTH),random.randrange(0, HEIGHT))

        all_sprites_group.add(enemy)
        enemy_sprites_group.add(enemy)

    # Create 100 blocks
    # Randomly place them throughout the screen
    for _ in range(num_blocks):
        block = Block(PINK, 20, 10)
        # Choose a random position for it
        block.rect.centerx = random.randrange(0, WIDTH)
        block.rect.centery = random.randrange(0, HEIGHT)

        all_sprites_group.add(block)
        block_sprites_group.add(block)

    # Create a player
    player = Mario()
    player.rect.center = (WIDTH / 2, HEIGHT / 2)
    # Create the shield with the player
    shield = Shield(player)
    # Add the player to the sprite group
    all_sprites_group.add(player)



    # ------------ MAIN GAME LOOP
    while not done:
        # ------ MAIN EVENT LISTENER
        # when the user does something
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Press "s" to release the shield
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        player.activate_shield()

        # ------ GAME LOGIC
        all_sprites_group.update()

        # Update shield's position
        if player.shield_active:
            shield.update()

        # Keep enemies in screen
        for enemy in enemy_sprites_group:
            if enemy.rect.left < 0 or enemy.rect.right > WIDTH:
                enemy.vel_x = -enemy.vel_x
            if enemy.rect.top < 0 or enemy.rect.bottom > HEIGHT:
                enemy.vel_y = -enemy.vel_y

        # Collision between Player and Blocks
        blocks_collided = pygame.sprite.spritecollide(player, block_sprites_group, True)
        # if the blocks_collided list has something in it
        # print Mario has collided with a block!
        for block in blocks_collided:
            if type(block) is Block:
                print("Player score: ", player.incr_score(block.point_value))

        if not block_sprites_group:
            level += 1
            print("Level:", level)

            # Respawn blocks
            for _ in range(num_blocks):
                block = Block(BLUE, 20, 10)
                block.rect.center = (
                    random.randrange(0, WIDTH),
                    random.randrange(0, HEIGHT)
                )
                block.level_up(level)

                all_sprites_group.add(block)
                block_sprites_group.add(block)

            # 2 more enemeis each level up
            for _ in range(2):
                enemy = Enemy()
                enemy.vel_x = random.choice(
                    list(range(-20, 0)) + list(range(1, 21))
                )
                enemy.vel_y = random.choice(
                    list(range(-20, 0)) + list(range(1, 21))
                )
                enemy.rect.center = (WIDTH // 2, HEIGHT // 2)

                all_sprites_group.add(enemy)
                enemy_sprites_group.add(enemy)

        # Collision between Player and Stars
        energy_collided = pygame.sprite.spritecollide(player, energy_sprites_group, True)
        # if the energy list has something in it
        # print Mario has collided with a energy!
        for stars in energy_collided:
            if type(stars) is Energy:
                player.collect_energy(1)
                print("Player Energy: ", player.energy)

        # Fill stars if star list is empty
        # Add more blocks and add one enemy
        if not energy_sprites_group:
            for _ in range(8):
                energy = Energy()
                # Choose a random position for it
                energy.rect.centerx = random.randrange(0, WIDTH)
                energy.rect.centery = random.randrange(0, HEIGHT)
                all_sprites_group.add(energy)
                energy_sprites_group.add(energy)



            # enemy = Enemy()
            # random_x = random.choice([-5, -3, -1, 1, 3, 5])
            # random_y = random.choice([-5, -3, -1, 1, 3, 5])
            # enemy.vel_x, enemy.vel_y = random_x, random_y
            # # Start them in the middle
            # enemy.rect.center = (WIDTH/2, HEIGHT/2)
            # all_sprites_group.add(enemy)
            # enemy_sprites_group.add(enemy)

        # Collision between Player and Enemies
        enemies_collided = pygame.sprite.spritecollide(player, enemy_sprites_group, False)
        for enemy in enemies_collided:
            # decrease mario's life
            if player.shield_active:
                print("damage defend by the shield")
            else:
                player.calc_damage(enemy.damage)

        health_bar.update_info(player.get_damage_percentage())

        # Game ends when Player's health is zero or less
        if player.health <= 0:
            done = True


        # ------ DRAWING TO SCREEN
        screen.fill(BLACK)
        all_sprites_group.draw(screen)
        screen.blit(health_bar, (10, 10))

        # Draw energy number
        # Draw energy icon
        screen.blit(star_icon, star_rect)

        energy_text = font.render(str(player.energy), True, WHITE)
        print(player.energy)
        text_rect = energy_text.get_rect(
            midright=(star_rect.left - 5, star_rect.centery)
        )
        screen.blit(energy_text, text_rect)

        # Draw the shield when it is shield_active
        if player.shield_active:
            screen.blit(shield.image, shield.rect)

        # Update screen
        pygame.display.flip()

        # ------ CLOCK TICK
        clock.tick(60) # 60 fps

    # Display final score:
    print("Thanks for playing!")
    print("Final score is:", player.points)

    # Stop the music
    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    game()
