from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """
    класс GameObject от которого наследуются змейка и яблоко
    содержит позицию и цвет
    """

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color


class Apple(GameObject):
    """класс яблоко"""

    def __init__(self):
        super().__init__(self.randomize_position(), APPLE_COLOR)
    """Инициализирует игровой объект."""
    def draw(self):
        """отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """случайная позиция для яблока"""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x, y


class Snake(GameObject):
    """класс змейки"""

    def __init__(self,
                 positions,
                 body_color,
                 direction,
                 next_direction,
                 last,
                 length=1
                 ):
        """Инициализирует игровой объект."""
        self.length = length
        self.positions = positions
        self.direction = direction
        self.next_direction = next_direction
        self.last = last
        self.body_color = body_color

    def draw(self):
        """Отрисовка змейки"""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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
        head = self.get_head_position()

        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """
        перезапуск игры и удаления всех сегметов змейки
        кроме головы при столкновения с собой
        """
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions[0] = 320, 240
        self.length = 1
        while len(self.positions) > 1:
            self.positions.pop()


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
    apple_in_game = Apple()
    snake_in_game = Snake([(320, 240)], SNAKE_COLOR, RIGHT, None, None)
    while True:
        clock.tick(SPEED)
        handle_keys(snake_in_game)
        snake_in_game.update_direction()
        snake_in_game.move()
        if apple_in_game.position == snake_in_game.positions[0]:
            snake_in_game.length += 1
            apple_in_game.position = apple_in_game.randomize_position()

        for position in snake_in_game.positions[1:]:
            if snake_in_game.get_head_position() == position:
                snake_in_game.reset()
                break
        screen.fill(BOARD_BACKGROUND_COLOR)

        apple_in_game.draw()
        snake_in_game.draw()
        draw_board_cells()

        pygame.display.update()


if __name__ == '__main__':
    main()
