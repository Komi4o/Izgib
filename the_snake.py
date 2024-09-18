import pygame
from random import randint

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения змейки
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона поля
BORDER_COLOR = (93, 216, 228)       # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)           # Цвет яблока
SNAKE_COLOR = (0, 255, 0)           # Цвет змейки

# Скорость движения змейки
SPEED = 10

# Начальная позиция змейки
INITIAL_SNAKE_POSITION = [(100, 100), (80, 100), (60, 100)]

# Инициализация Pygame и создание экрана и часов
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для объектов игры."""

    def __init__(self, position=(0, 0), color=(0, 0, 0), body_color=(0, 0, 0)):
        self.position = position
        self.color = color
        self.body_color = body_color

    def draw_rect(self, screen, position):
        """Рисует прямоугольник на экране."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def erase_rect(self, screen, position):
        """Стирает прямоугольник на экране."""
        last_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def draw(self, screen):
        raise NotImplementedError


class Apple(GameObject):
    """Класс для объекта яблока."""

    def __init__(self, snake_positions=None):
        """Инициализация яблока с случайной позицией и цветом."""
        super().__init__(position=(0, 0), color=APPLE_COLOR,
                         body_color=APPLE_COLOR)
        if snake_positions is not None:
            self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in snake_positions:
                self.position = position
                break

    def draw(self, screen):
        """Отображение яблока на экране."""
        self.draw_rect(screen, self.position)


class Snake(GameObject):
    """Класс для объекта змейки."""

    def __init__(self, position=None):
        """Инициализация змейки с начальной позицией, направлением и цветом."""
        if position is None:
            position = INITIAL_SNAKE_POSITION[0]
        self.positions = INITIAL_SNAKE_POSITION
        self.direction = RIGHT
        self.next_direction = None
        super().__init__(position=position, color=SNAKE_COLOR,
                         body_color=SNAKE_COLOR)

    def update_direction(self):
        """Обновление направления змейки на основе следующего направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещение змейки в текущем направлении."""
        head_x, head_y = self.get_head_position()
        new_head = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions = [new_head] + self.positions  # Обновляем позицию
        self.positions.pop()  # Убираем последний сегмент

    def grow(self):
        """Увеличение змейки за счет добавления сегмента к её хвосту."""
        self.positions.append(self.positions[-1])

    def draw(self, screen):
        """Отображение змейки на экране."""
        # Рисуем каждый сегмент
        for position in self.positions:
            self.draw_rect(screen, position)

    def get_head_position(self):
        """Получение позиции головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки к её начальному состоянию."""
        self.__init__()


def handle_keys(snake):
    """Обработка пользовательского ввода для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    pygame.display.set_caption('Змейка')

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        # Обновляем экран
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        clock.tick(SPEED)


if __name__ == '__main__':
    main()
