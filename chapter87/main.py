import tkinter as tk
BG='#DBB5B5'
BALL_COLOR='#F1E5D1'
PADDLE_COLOR='#987070'
BRICK_C1='#AF8F6F'
BRICK_C2='#74512D'
BRICK_C3='#543310'

class Game(tk.Frame):
    """Tkinter.Frame subclass has given to Tkinter.Tk() root."""
    def __init__(self, master):
        """Initialize game environment."""
        tk.Frame.__init__(self, master)
        self.lives = 3
        self.width = 610
        self.height = 400
        self.canvas = tk.Canvas(self, bg=BG, width=self.width,
                                height=self.height)
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.ball = None
        self._paddle_y_start = 326
        self.paddle = Paddle(self.canvas, self.width / 2, self._paddle_y_start)

        self.items[self.paddle.item] = self.paddle

        for x in range(5, self.width - 5, 75):  # 75 px step
            self.add_brick(x + 37.5, 50, 2)
            self.add_brick(x + 37.5, 70, 1)
            self.add_brick(x + 37.5, 90, 1)

        self.hud = None

        self.setup_game()

        self.canvas.focus_set()
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>', lambda _: self.paddle.move(10))

    def setup_game(self):
        """Do all the necessary things to start the game."""
        self.add_ball()
        self.update_lives_text()
        self.text = self.draw_text(300, 200, "Press Spacebar to start")

        self.canvas.bind('<space>', lambda _: self.start_game())

    def add_ball(self):
        """Create a Ball and store a reference."""
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 310)
        self.paddle.set_ball(self.ball)

    def add_brick(self, x, y, ball_hits):
        """Create a Brick object."""
        brick = Brick(self.canvas, x, y, ball_hits)
        self.items[brick.item] = brick

    def draw_text(self, x, y, text, size='40'):
        """this shows text message on the canvas instance."""
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=text, font=font)

    def update_lives_text(self):
        """Displays number of lives left."""
        text = "Lives: {}".format(self.lives)
        if self.hud is None:
            self.hud = self.draw_text(50, 20, text, 15)
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def start_game(self):
        """Start main loop of game."""
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()

    def game_loop(self):
        """Main game loop."""
        self.check_collisions()
        bricks_number = len(self.canvas.find_withtag('brick'))
        if bricks_number == 0:
            self.ball.speed = None
            self.draw_text(300, 200, "You've won!")
        elif self.ball.get_position()[3] >= self.height:
            self.ball.speed = None
            self.lives -= 1
            if self.lives < 0:
                self.draw_text(300, 200, "Game Over")
            else:
                self.after(1000, self.setup_game)
        else:
            self.ball.update()
            self.after(50, self.game_loop)

    def check_collisions(self):
        """Collisions of ball."""
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords) 
        collideables = [self.items[x] for x in items if x in self.items]
        self.ball.collide(collideables)


class GameObject():
    """Base class for game entities."""
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        """Returns coordinates of instance's item property."""
        return self.canvas.coords(self.item)

    def move(self, x, y):
        """Move x horizontally, and y vertically."""
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


class Ball(GameObject):
    """Stores information
    about speed, direction, and radius of the ball."""
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.direction = [1, -1]  # right and up
        self.speed = 10

        # self.item value will be an integer, which is ref num returned by method
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill=BALL_COLOR)
        # now call parent constructor with our required item
        GameObject.__init__(self, canvas, item)

    def update(self):
        """COLLISIONS."""
        ball_coords = self.get_position()
        width = self.canvas.winfo_width()

        if ball_coords[0] <= 0 or ball_coords[2] >= width:
            self.direction[0] *= -1  
        if ball_coords[1] <= 0:
            self.direction[1] *= -1 
        x = self.direction[0] * self.speed  
        y = self.direction[1] * self.speed
        self.move(x, y)  


    def collide(self, game_objects):
        """list of colliding objects."""
        ball_coords = self.get_position()
        ball_center_x = (ball_coords[0] + ball_coords[2]) * 0.5  

        if len(game_objects) > 1:  
            self.direction[1] *= -1
        elif len(game_objects) == 1:  
            game_object = game_objects[0]
            coords = game_object.get_position()
            if ball_center_x > coords[2]:
                self.direction[0] = 1
            elif ball_center_x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1
        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()  


class Paddle(GameObject):
    """Create a Paddle"""
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = 10
        self.ball = None

        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=PADDLE_COLOR)
        GameObject.__init__(self, canvas, item)

    def set_ball(self, ball):
        """Store a reference to a ball."""
        self.ball = ball

    def move(self, offset):
        """Move the Paddle left or right."""
        coords = self.get_position()  
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            GameObject.move(self, offset, 0)  
            if self.ball is not None:
                self.ball.move(offset, 0) 


class Brick(GameObject):
    """Destroy rectangle objects when ball hit them."""
    COLORS = {1: BRICK_C1, 2: BRICK_C2, 3: BRICK_C3}

    def __init__(self, canvas, x, y, ball_hits):
        self.width = 75
        self.height = 20
        self.ball_hits = ball_hits
        color = Brick.COLORS[ball_hits]  

        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        GameObject.__init__(self, canvas, item)

    def hit(self):
        """Ball hits counter decrement."""
        self.ball_hits -= 1
        if self.ball_hits == 0:
            self.delete()  
        else:  
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.ball_hits])



if __name__ == "__main__":
    ROOT = tk.Tk()
    ROOT.title('Breakout')
    GAME = Game(ROOT)
    GAME.mainloop()