import pygame
import random
import math
import sys

# 初始化Pygame
pygame.init()

# 游戏窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
PURPLE = (255, 50, 255)
CYAN = (50, 255, 255)
ORANGE = (255, 150, 50)
DARK_GREEN = (0, 150, 0)
LIGHT_GREEN = (150, 255, 150)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow_flag = False
        self.color = GREEN

    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # 检查边界碰撞
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False

        # 检查自身碰撞
        if new_head in self.positions:
            return False

        self.positions.insert(0, new_head)

        if not self.grow_flag:
            self.positions.pop()
        else:
            self.grow_flag = False

        return True

    def change_direction(self, new_direction):
        # 防止蛇直接掉头
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def grow(self):
        self.grow_flag = True

    def draw(self, screen):
        for i, pos in enumerate(self.positions):
            x, y = pos
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

            # 渐变效果
            if i == 0:  # 蛇头
                pygame.draw.rect(screen, DARK_GREEN, rect)
                pygame.draw.rect(screen, GREEN, rect, 2)
                # 画眼睛
                eye_size = 4
                eye_offset = 5
                if self.direction == (1, 0):  # 向右
                    pygame.draw.circle(screen, WHITE,
                                       (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + eye_offset), eye_size)
                    pygame.draw.circle(screen, WHITE,
                                       (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + GRID_SIZE - eye_offset),
                                       eye_size)
                elif self.direction == (-1, 0):  # 向左
                    pygame.draw.circle(screen, WHITE, (x * GRID_SIZE + eye_offset, y * GRID_SIZE + eye_offset),
                                       eye_size)
                    pygame.draw.circle(screen, WHITE,
                                       (x * GRID_SIZE + eye_offset, y * GRID_SIZE + GRID_SIZE - eye_offset), eye_size)
                elif self.direction == (0, 1):  # 向下
                    pygame.draw.circle(screen, WHITE,
                                       (x * GRID_SIZE + eye_offset, y * GRID_SIZE + GRID_SIZE - eye_offset), eye_size)
                    pygame.draw.circle(screen, WHITE,
                                       (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + GRID_SIZE - eye_offset),
                                       eye_size)
                else:  # 向上
                    pygame.draw.circle(screen, WHITE, (x * GRID_SIZE + eye_offset, y * GRID_SIZE + eye_offset),
                                       eye_size)
                    pygame.draw.circle(screen, WHITE,
                                       (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + eye_offset), eye_size)
            else:  # 蛇身
                color_intensity = max(50, 255 - i * 10)
                color = (0, color_intensity, 0)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, LIGHT_GREEN, rect, 1)


class Food:
    def __init__(self):
        self.position = None
        self.color = RED
        self.animation_offset = 0

    def generate(self, snake_positions):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_positions:
                self.position = (x, y)
                break

    def draw(self, screen):
        if self.position:
            x, y = self.position
            center_x = x * GRID_SIZE + GRID_SIZE // 2
            center_y = y * GRID_SIZE + GRID_SIZE // 2

            # 动画效果
            self.animation_offset = (self.animation_offset + 0.1) % (2 * math.pi)
            radius = GRID_SIZE // 2 - 2 + int(2 * math.sin(self.animation_offset))

            # 绘制食物（圆形）
            pygame.draw.circle(screen, RED, (center_x, center_y), radius)
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius - 2)
            pygame.draw.circle(screen, ORANGE, (center_x, center_y), radius - 4)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("贪吃蛇游戏")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.food.generate(self.snake.positions)
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                else:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction((1, 0))
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

    def update(self):
        if not self.game_over:
            if not self.snake.move():
                self.game_over = True

            # 检查是否吃到食物
            if self.snake.positions[0] == self.food.position:
                self.snake.grow()
                self.score += 10
                self.food.generate(self.snake.positions)

    def draw_background(self):
        # 绘制渐变背景
        for y in range(WINDOW_HEIGHT):
            color_value = int(20 + (y / WINDOW_HEIGHT) * 30)
            color = (color_value, color_value, color_value + 10)
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))

        # 绘制网格
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (30, 30, 40), (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (30, 30, 40), (0, y), (WINDOW_WIDTH, y), 1)

    def draw_ui(self):
        # 绘制分数
        score_text = self.font.render(f"分数: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(topleft=(10, 10))

        # 绘制分数背景
        pygame.draw.rect(self.screen, (0, 0, 0, 128), score_rect.inflate(20, 10))
        pygame.draw.rect(self.screen, WHITE, score_rect.inflate(20, 10), 2)
        self.screen.blit(score_text, score_rect)

        # 绘制控制提示
        controls = [
            "使用方向键或WASD控制",
            "ESC - 退出游戏"
        ]
        y_offset = WINDOW_HEIGHT - 60
        for control in controls:
            control_text = self.small_font.render(control, True, WHITE)
            control_rect = control_text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(control_text, control_rect)
            y_offset += 25

    def draw_game_over(self):
        # 绘制游戏结束画面
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # 游戏结束文字
        game_over_text = self.font.render("游戏结束!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)

        # 最终分数
        final_score_text = self.font.render(f"最终分数: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(final_score_text, final_score_rect)

        # 重新开始提示
        restart_text = self.small_font.render("按空格键重新开始，ESC退出", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)

    def reset_game(self):
        self.snake.reset()
        self.food.generate(self.snake.positions)
        self.score = 0
        self.game_over = False

    def draw(self):
        self.draw_background()

        if not self.game_over:
            self.snake.draw(self.screen)
            self.food.draw(self.screen)

        self.draw_ui()

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # 控制游戏速度

        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
