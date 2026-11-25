import pygame

from random import randint

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_OF_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

BLACK_COLOR = (0, 0, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """класс GameObject"""

    def __init__(self, position=CENTER_OF_SCREEN, body_color=BLACK_COLOR):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position):
        """Метод отрисовки одной клетки."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """класс яблоко"""

    def __init__(self,
                 position=CENTER_OF_SCREEN,
                 body_color=APPLE_COLOR,
                 occupied_positions=(CENTER_OF_SCREEN,)
                 ):
        """Инициализирует игровой объект."""
        super().__init__(position, body_color)
        self.randomize_position(occupied_positions)

    def draw(self):
        """отрисовка яблока"""
        self.draw_cell(self.position)

    def randomize_position(self, occupied_positions):
        """случайная позиция для яблока"""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE
                             )
            if self.position not in occupied_positions:
                break


class Snake(GameObject):
    """класс змейки"""

    def __init__(self,
                 body_color=SNAKE_COLOR,
                 ):
        """Инициализирует игровой объект."""
        self.positions = [CENTER_OF_SCREEN]
        super().__init__(self.positions[0], body_color)
        self.length = 1

        self.direction = RIGHT
        self.next_direction = None
        self.body_color = body_color

    def draw(self):
        """Отрисовка змейки"""
        for position in self.positions:
            self.draw_cell(position)

    def update_direction(self):
        """обновляет направление движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """возвращает координаты головы змейки"""
        return self.positions[0]

    def move(self):
        """метод движения змейки"""
        x, y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """
        перезапуск игры и удаления всех сегметов змейки
        кроме головы при столкновения с собой
        """
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = [(320, 240)]
        self.length = 1


def handle_keys(game_object):
    """проверка нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def draw_board_cells():
    """отрисовка обводки клеток поля"""
    for cell_of_width in range(GRID_WIDTH):
        for cell_of_height in range(GRID_HEIGHT):
            rect = pygame.Rect(
                cell_of_width * GRID_SIZE,
                cell_of_height * GRID_SIZE,
                GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def main():
    """главная функция с игровой логикой"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake_in_game = Snake()
    apple_in_game = Apple(occupied_positions=snake_in_game.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake_in_game)
        snake_in_game.update_direction()
        snake_in_game.move()
        if apple_in_game.position == snake_in_game.get_head_position():
            snake_in_game.length += 1
            apple_in_game.randomize_position(snake_in_game.positions)

        elif snake_in_game.get_head_position() in snake_in_game.positions[1:]:
            snake_in_game.reset()

            apple_in_game.randomize_position(
                snake_in_game.positions
            )

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple_in_game.draw()
        snake_in_game.draw()
        draw_board_cells()

        pygame.display.update()


if __name__ == '__main__':
    main()
