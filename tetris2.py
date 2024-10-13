import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar dan grid
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
COLS = SCREEN_WIDTH // GRID_SIZE
ROWS = SCREEN_HEIGHT // GRID_SIZE

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)

# Bentuk Tetris (berdasarkan grid 4x4)
SHAPES = [
    [[1, 1, 1, 1]],  # I Shape
    [[1, 1, 1], [0, 1, 0]],  # T Shape
    [[1, 1], [1, 1]],  # O Shape
    [[1, 1, 0], [0, 1, 1]],  # Z Shape
    [[0, 1, 1], [1, 1, 0]],  # S Shape
    [[1, 1, 1], [1, 0, 0]],  # L Shape
    [[1, 1, 1], [0, 0, 1]]   # J Shape
]

# Warna untuk setiap bentuk
SHAPE_COLORS = [CYAN, PURPLE, YELLOW, RED, GREEN, ORANGE, BLUE]

# Menggambar grid di layar
def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))

# Kelas untuk Tetrimino (Blok Tetris)
class Tetrimino:
    def __init__(self, shape):
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        # Putar bentuk (transpose lalu balik urutannya)
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self, screen):
        for row_index, row in enumerate(self.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color, pygame.Rect((self.x + col_index) * GRID_SIZE, (self.y + row_index) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Kelas untuk permainan Tetris
class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
        self.current_tetrimino = Tetrimino(random.choice(SHAPES))
        self.game_over = False
        self.score = 0

    def check_collision(self, dx, dy):
        for row_index, row in enumerate(self.current_tetrimino.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    x = self.current_tetrimino.x + col_index + dx
                    y = self.current_tetrimino.y + row_index + dy
                    if x < 0 or x >= COLS or y >= ROWS or (y >= 0 and self.grid[y][x] != BLACK):
                        return True
        return False

    def freeze_tetrimino(self):
        # Tempatkan tetrimino saat mencapai dasar atau bertabrakan
        for row_index, row in enumerate(self.current_tetrimino.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    self.grid[self.current_tetrimino.y + row_index][self.current_tetrimino.x + col_index] = self.current_tetrimino.color
        self.clear_lines()
        self.current_tetrimino = Tetrimino(random.choice(SHAPES))
        if self.check_collision(0, 0):
            self.game_over = True

    def clear_lines(self):
        # Menghapus baris yang penuh
        lines_to_clear = [row for row in range(ROWS) if all(self.grid[row][col] != BLACK for col in range(COLS))]
        for row in lines_to_clear:
            del self.grid[row]
            self.grid.insert(0, [BLACK for _ in range(COLS)])
        self.score += len(lines_to_clear) * 100

    def move_tetrimino(self, dx, dy):
        if not self.check_collision(dx, dy):
            self.current_tetrimino.x += dx
            self.current_tetrimino.y += dy
        elif dy > 0:  # Tetrimino tidak bisa turun lebih jauh
            self.freeze_tetrimino()

    def rotate_tetrimino(self):
        original_shape = self.current_tetrimino.shape
        self.current_tetrimino.rotate()
        if self.check_collision(0, 0):
            self.current_tetrimino.shape = original_shape

    def draw_tetrimino(self):
        self.current_tetrimino.draw(self.screen)

    def draw_grid(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] != BLACK:
                    pygame.draw.rect(self.screen, self.grid[row][col], pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_score(self):
        font = pygame.font.SysFont("led_counter-7_italic", 30)
        score_text = font.render(f"Skor: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def reset_game(self):
        self.grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
        self.current_tetrimino = Tetrimino(random.choice(SHAPES))
        self.game_over = False
        self.score = 0

    def run(self):
        fall_time = 0
        fall_speed = 500  # Milidetik

        while True:
            self.screen.fill(BLACK)
            fall_time += self.clock.get_rawtime()
            self.clock.tick()

            # Kontrol pemain
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_tetrimino(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_tetrimino(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_tetrimino(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_tetrimino()
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()

            # Turunkan tetrimino secara otomatis
            if fall_time >= fall_speed:
                if not self.game_over:
                    self.move_tetrimino(0, 1)
                fall_time = 0

            # Gambar grid, tetrimino, dan skor
            self.draw_grid()
            self.draw_tetrimino()
            draw_grid(self.screen)
            self.draw_score()

            if self.game_over:
                font = pygame.font.SysFont("led_counter-7_italic", 50)
                game_over_text = font.render("Game Over!", True, RED)
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
                font = pygame.font.SysFont("led_counter-7_italic", 30)
                restart_text = font.render("Tekan R untuk restart", True, WHITE)
                self.screen.blit(restart_text, (SCREEN_WIDTH // 4 - 30, SCREEN_HEIGHT // 2 + 50))

            pygame.display.update()

# Menjalankan permainan
if __name__ == "__main__":
    game = TetrisGame()
    game.run()
