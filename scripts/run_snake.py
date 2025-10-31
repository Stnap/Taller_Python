#  Copyright (c) 2025. Diplomado en Inteligencia Artificial Aplicada
import time
import turtle
from dataclasses import dataclass
from random import randint


@dataclass
class GameConfig:
    """Configuración del juego"""
    screen_width: int = 640
    screen_height: int = 480
    bg_color: str = "yellow"
    title: str = "The Snake Game"
    initial_speed: int = 10
    min_speed: int = 3
    speed_increment: int = 1
    movement_step: int = 24
    frame_delay: float = 0.02
    border_margin: int = 30


@dataclass
class Colors:
    """Colores del juego"""
    snake_head: str = "black"
    snake_body: str = "green"
    food: str = "red"
    scoreboard: str = "blue"


class GameScreen:
    """Maneja la configuración y gestión de la pantalla del juego"""
    
    def __init__(self, config: GameConfig):
        self.config = config
        self.width = config.screen_width
        self.height = config.screen_height
        self.screen = self._configure()
    
    def _configure(self):
        """Configura la pantalla del juego"""
        screen = turtle.Screen()
        screen.title(self.config.title)
        screen.bgcolor(self.config.bg_color)
        screen.setup(self.config.screen_width, self.config.screen_height)
        screen.tracer(0)
        return screen
    
    def update(self):
        """Actualiza la pantalla"""
        self.screen.update()
    
    def listen(self):
        """Habilita escuchar eventos de teclado"""
        self.screen.listen()
    
    def onkey(self, func, key):
        """Registra un manejador de tecla"""
        self.screen.onkey(func, key)


class Scoreboard:
    """Maneja el marcador de puntos del juego"""
    
    def __init__(self, screen_height: int, colors: Colors):
        self.points = 0
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.color(colors.scoreboard)
        self.turtle.penup()
        self.turtle.hideturtle()
        self.turtle.goto(0, screen_height // 2 - 25)
        self.display()
    
    def display(self):
        """Muestra el marcador en pantalla"""
        self.turtle.clear()
        self.turtle.write(
            f"Points: {self.points}", align="center", font=("Courier", 24, "normal")
        )
    
    def increment(self):
        """Incrementa y muestra los puntos"""
        self.points += 1
        self.display()
    
    def reset(self):
        """Reinicia el marcador"""
        self.points = 0
        self.display()


class Border:
    """Dibuja los bordes del área de juego"""
    
    def __init__(self, x_limit: int, y_limit: int, border_color: str = "black"):
        self.x_limit = x_limit
        self.y_limit = y_limit
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.color(border_color)
        self.turtle.penup()
        self.turtle.hideturtle()
        self.draw()
    
    def draw(self):
        """Dibuja un rectángulo que marca los límites del juego"""
        offset_x = 10
        offset_y = 0
        
        self.turtle.goto(-self.x_limit - offset_x, -self.y_limit - offset_y)
        self.turtle.pendown()
        self.turtle.pensize(3)
        
        for _ in range(2):
            self.turtle.forward((self.x_limit + offset_x) * 2)
            self.turtle.left(90)
            self.turtle.forward((self.y_limit + offset_y) * 2)
            self.turtle.left(90)
        
        self.turtle.penup()


class Food:
    """Maneja la comida del juego"""
    
    def __init__(self, x_limit: int, y_limit: int, colors: Colors):
        self.x_limit = x_limit
        self.y_limit = y_limit
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.fillcolor(colors.food)
        self.turtle.penup()
        self.move()
    
    def move(self):
        """Mueve la comida a una posición aleatoria"""
        x = randint(-self.x_limit, self.x_limit)
        y = randint(-self.y_limit, self.y_limit)
        self.turtle.goto(x, y)
    
    def position(self):
        """Retorna la posición actual de la comida"""
        return self.turtle.position()


class Snake:
    """Maneja la serpiente del juego"""
    
    def __init__(self, config: GameConfig, colors: Colors):
        self.config = config
        self.colors = colors
        self.head = turtle.Turtle()
        self.head.fillcolor(colors.snake_head)
        self.head.shape("square")
        self.head.penup()
        self.head.goto(0, 0)
        self.segments = [self.head]
    
    def add_segment(self):
        """Agrega un segmento al cuerpo de la serpiente"""
        segment = turtle.Turtle()
        segment.penup()
        segment.goto(self.head.xcor(), self.head.ycor())
        segment.setheading(self.head.heading())
        segment.shape("square")
        segment.fillcolor(self.colors.snake_body)
        segment.speed(0)
        self.segments.append(segment)
    
    def move(self):
        """Mueve la serpiente"""
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].goto(self.segments[i - 1].xcor(), self.segments[i - 1].ycor())
            self.segments[i].setheading(self.segments[i - 1].heading())

        step = self.config.movement_step
        if self.head.heading() == 0:
            self.head.setx(self.head.xcor() + step)
        elif self.head.heading() == 90:
            self.head.sety(self.head.ycor() + step)
        elif self.head.heading() == 180:
            self.head.setx(self.head.xcor() - step)
        elif self.head.heading() == 270:
            self.head.sety(self.head.ycor() - step)
    
    def go_up(self):
        """Mueve la serpiente hacia arriba"""
        if self.head.heading() != 270:
            self.head.setheading(90)
    
    def go_down(self):
        """Mueve la serpiente hacia abajo"""
        if self.head.heading() != 90:
            self.head.setheading(270)
    
    def go_right(self):
        """Mueve la serpiente hacia la derecha"""
        if self.head.heading() != 180:
            self.head.setheading(0)
    
    def go_left(self):
        """Mueve la serpiente hacia la izquierda"""
        if self.head.heading() != 0:
            self.head.setheading(180)
    
    def check_wall_collision(self, x_limit, y_limit):
        """Verifica si la serpiente chocó con las paredes"""
        return abs(self.head.xcor()) >= x_limit or abs(self.head.ycor()) >= y_limit
    
    def check_self_collision(self):
        """Verifica si la serpiente chocó consigo misma"""
        for segment in self.segments[1:]:
            if self.head.distance(segment) <= 20:
                return True
        return False
    
    def check_food_collision(self, food_position):
        """Verifica si la serpiente comió la comida"""
        return self.head.distance(food_position) <= 18
    
    def reset(self):
        """Reinicia la serpiente a su estado inicial"""
        self.head.goto(0, 0)
        self.head.setheading(0)
        for segment in self.segments[1:]:
            segment.reset()
            segment.hideturtle()
        self.segments = [self.head]


class SnakeGame:
    """Clase principal que maneja el juego"""
    
    def __init__(self, config: GameConfig = None, colors: Colors = None):
        self.config = config or GameConfig()
        self.colors = colors or Colors()
        
        self.game_screen = GameScreen(self.config)
        self.scoreboard = Scoreboard(self.game_screen.height, self.colors)
        
        self.x_limit = self.game_screen.width // 2 - self.config.border_margin
        self.y_limit = self.game_screen.height // 2 - self.config.border_margin
        
        self.border = Border(self.x_limit, self.y_limit)
        self.food = Food(self.x_limit, self.y_limit, self.colors)
        self.snake = Snake(self.config, self.colors)
        self.move_delay = self.config.initial_speed
        self.frame_count = 0
        
        self._setup_controls()
    
    def _setup_controls(self):
        """Configura los controles del teclado"""
        self.game_screen.onkey(self.snake.go_up, "Up")
        self.game_screen.onkey(self.snake.go_down, "Down")
        self.game_screen.onkey(self.snake.go_left, "Left")
        self.game_screen.onkey(self.snake.go_right, "Right")
        self.game_screen.listen()
    
    def reset_game(self):
        """Reinicia el juego"""
        time.sleep(1)
        self.snake.reset()
        self.move_delay = self.config.initial_speed
        self.frame_count = 0
        self.scoreboard.reset()
        self.food.move()
    
    def run(self):
        """Ejecuta el bucle principal del juego"""
        while True:
            self.game_screen.update()
            self.frame_count += 1
            
            if self.frame_count >= self.move_delay:
                self.frame_count = 0
                self.snake.move()
                
                if self.snake.check_wall_collision(self.x_limit, self.y_limit) or self.snake.check_self_collision():
                    self.reset_game()
                
                if self.snake.check_food_collision(self.food.position()):
                    self.food.move()
                    self.move_delay = max(self.config.min_speed, 
                                         self.move_delay - self.config.speed_increment)
                    self.snake.add_segment()
                    self.scoreboard.increment()
            
            time.sleep(self.config.frame_delay)


def main():
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()