#  Copyright (c) 2025. Diplomado en Inteligencia Artificial Aplicada
import time
import turtle
from dataclasses import dataclass
from random import randint


@dataclass
class ScreenConfig:
    """Configuración de la pantalla"""
    width: int = 640
    height: int = 480
    title: str = "The Bouncing Ball"
    bg_color: str = "white"
    frame_delay: float = 0.02


@dataclass
class BallConfig:
    """Configuración de la pelota"""
    shape: str = "circle"
    color: str = "red"
    size: float = 1
    speed_x: int = 3
    speed_y: int = 3
    speed_increment: float = 0.2
    speed_limit: float = 50


class Screen:
    """Maneja la pantalla"""
    
    def __init__(self, config: ScreenConfig):
        self.config = config
        self.screen = self._configure()
    
    def _configure(self):
        """Configura la pantalla"""
        screen = turtle.Screen()
        screen.title(self.config.title)
        screen.bgcolor(self.config.bg_color)
        screen.setup(self.config.width, self.config.height)
        screen.tracer(0)
        return screen
    
    def update(self):
        """Actualiza la pantalla"""
        self.screen.update()
    
    def get_limits(self):
        """Retorna los límites de la pantalla"""
        x_limit = self.config.width // 2
        y_limit = self.config.height // 2
        return x_limit, y_limit


class Ball:
    """Maneja la pelota"""
    
    def __init__(self, ball_config: BallConfig, x_limit: int, y_limit: int):
        self.config = ball_config
        self.x_limit = x_limit
        self.y_limit = y_limit
        self.turtle = self._create_ball()
        self.vx = ball_config.speed_x
        self.vy = ball_config.speed_y
        self._random_position()
        self.turtle.pendown()
    
    def _create_ball(self):
        """Crea la pelota"""
        ball = turtle.Turtle()
        ball.shape(self.config.shape)
        ball.fillcolor(self.config.color)
        ball.shapesize(self.config.size)
        ball.penup()
        return ball
    
    def _random_position(self):
        """Coloca la pelota en una posición aleatoria"""
        x = randint(-self.x_limit + 50, self.x_limit - 50)
        y = randint(-self.y_limit + 50, self.y_limit - 50)
        self.turtle.goto(x, y)
    
    def move(self):
        """Mueve la pelota"""
        new_x = self.turtle.xcor() + self.vx
        new_y = self.turtle.ycor() + self.vy
        self.turtle.goto(new_x, new_y)
    
    def check_collision(self):
        """Maneja colisiones con los bordes y aumenta la velocidad"""
        x = self.turtle.xcor()
        y = self.turtle.ycor()
        
        ball_radius = self.config.size * 10
        
        if x + ball_radius >= self.x_limit or x - ball_radius <= -self.x_limit:
            self.vx = -self.vx
            if self.vx > 0:
                self.vx = min(self.vx + self.config.speed_increment, self.config.speed_limit)
            else:
                self.vx = max(self.vx - self.config.speed_increment, -self.config.speed_limit)
        
        if y + ball_radius >= self.y_limit or y - ball_radius <= -self.y_limit:
            self.vy = -self.vy
            if self.vy > 0:
                self.vy = min(self.vy + self.config.speed_increment, self.config.speed_limit)
            else:
                self.vy = max(self.vy - self.config.speed_increment, -self.config.speed_limit)


class BounceGame:
    """Clase principal"""
    
    def __init__(self, screen_config: ScreenConfig = None, ball_config: BallConfig = None):
        self.screen_config = screen_config or ScreenConfig()
        self.ball_config = ball_config or BallConfig()
        
        self.game_screen = Screen(self.screen_config)
        x_limit, y_limit = self.game_screen.get_limits()
        self.ball = Ball(self.ball_config, x_limit, y_limit)
    
    def run(self):
        """Ejecuta el bucle principal"""
        while True:
            self.game_screen.update()
            self.ball.move()
            self.ball.check_collision()
            time.sleep(self.screen_config.frame_delay)


def main():
    game = BounceGame()
    game.run()


if __name__ == "__main__":
    main()
