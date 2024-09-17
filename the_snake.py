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

# Инициализация Pygame и создание экрана и часов
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:

    def __init__(self, position=(0, 0), color=(0, 0, 0), body_color=(0, 0, 0)):
        """
        Инициализация объекта игры с позицией, цветом и цветом тела.

        Args:
            position (tuple): Позиция объекта.
            color (tuple): Цвет объекта.
            body_color (tuple): Цвет тела объекта.
        """
        self.position = position
        self.color = color
        self.body_color = body_color

    def draw(self, screen):
        """
        Отображение объекта на экране.

        Args:
            screen (pygame.Surface): Поверхность для отрисовки.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    def __init__(self):
        """
        Инициализация яблока с случайной позицией и цветом.
        """
        position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                    randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        super().__init__(position, APPLE_COLOR, APPLE_COLOR)

    def randomize_position(self):
        """
        Изменение позиции яблока на случайную.
        """
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class Snake(GameObject):

    def __init__(self):
        """
        Инициализация змейки с начальной позицией, направлением и цветом.
        """
        self.positions = [(100, 100), (80, 100), (60, 100)
                          ]  # Начальная позиция змейки
        self.direction = RIGHT  # Начальное направление
        self.next_direction = None  # Следующее направление
        self.last = None  # Последний сегмент для увеличения змейки
        super().__init__(self.positions[0], SNAKE_COLOR, SNAKE_COLOR)

    def update_direction(self):
        """
        Обновление направления змейки на основе следующего направления.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Перемещение змейки в текущем направлении.
        """
        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0] * GRID_SIZE,
                    head_y + self.direction[1] * GRID_SIZE)
        self.positions = [new_head] + self.positions[:-1]
        self.last = self.positions[-1]
        self.wrap_around()

    def grow(self):
        """
        Увеличение змейки за счет добавления сегмента к её хвосту.
        """
        tail = self.positions[-1]
        self.positions.append(self.last)
        self.last = None

    def wrap_around(self):
        """
        Обеспечение того, чтобы змейка появлялась с противоположной стороны экрана, если выходит за его пределы.
        """
        head_x, head_y = self.positions[0]
        if head_x < 0:
            head_x = SCREEN_WIDTH - GRID_SIZE
        elif head_x >= SCREEN_WIDTH:
            head_x = 0
        if head_y < 0:
            head_y = SCREEN_HEIGHT - GRID_SIZE
        elif head_y >= SCREEN_HEIGHT:
            head_y = 0
        self.positions[0] = (head_x, head_y)

    def draw(self, screen):
        """
        Отображение змейки на экране.

        Args:
            screen (pygame.Surface): Поверхность для отрисовки.
        """
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Получение позиции головы змейки.

        Returns:
            tuple: Позиция головы.
        """
        return self.positions[0]

    def reset(self):
        """
        Сброс змейки к её начальному состоянию.
        """
        self.__init__()


def handle_keys(snake):
    """
    Обработка пользовательского ввода для управления змейкой.

    Args:
        snake (Snake): Объект змейки, который нужно управлять.
    """
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
    """
    Основной игровой цикл.
    """
    pygame.display.set_caption('Змейка')

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.grow()
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
