from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
from collections import namedtuple
from sys import exit

WIDTH= 800
HEIGHT = 600
WHITE = 200, 200, 200
RED = 200, 50, 50
BLUE = 50, 50, 200
GREEN = 50, 200, 50

ball = Rect((WIDTH/2, HEIGHT/2), (20, 20))
Direction = namedtuple('Direction', 'x y')
ball_dir = Direction(5, -5)

paddle = Rect((WIDTH/2, 0.96 * HEIGHT), (150, 15))
block_quantity = 10
block_width = WIDTH / block_quantity
block_height = block_width / 3
BLOCK_COLOURS = RED, GREEN, BLUE

class Block(Rect):
    def __init__(self, colour, rect):
        Rect.__init__(self, rect)
        self.colour = colour

blocks = []
for block_index in range(block_quantity):
    colour = BLOCK_COLOURS[block_index % len(BLOCK_COLOURS)]
    block = Block(colour, ((block_index * block_width, 0), (block_width, block_height)))
    blocks.append(block)

def draw():
    screen.clear()
    screen.fill((20, 20, 20))
    screen.draw.text(message, fontsize=120, center=(WIDTH / 2, HEIGHT / 2), alpha=0.1)
    screen.draw.filled_rect(ball, WHITE)
    screen.draw.filled_rect(paddle, WHITE)

    for block in blocks:
        screen.draw.filled_rect(block, block.colour)

def update():
    global ball_dir
    global message
    message = f"{len(blocks)} BLOCKS LEFT"

    ball.move_ip(ball_dir)

    if ball.x > WIDTH or ball.x <= 0:
        ball_dir = Direction(-1 * ball_dir.x, ball_dir.y)

    if ball.y <= 0:
        ball_dir = Direction(ball_dir.x, ball_dir.y * -1)

    if ball.colliderect(paddle):
        ball_dir = Direction(ball_dir.x, - abs(ball_dir.y))

    to_kill = ball.collidelist(blocks)

    if to_kill >= 0:
        ball_dir = Direction(ball_dir.x, abs(ball_dir.y))
        blocks.pop(to_kill)

    if not blocks:
        message = "YOU WIN"
        clock.schedule(exit, 1)

    elif ball.y > HEIGHT:
        message = "GAME OVER"
        clock.schedule(exit, 1)


def horizontalAxisChange(self, voltageRatio):
    if paddle.left < 0: paddle.left = 10
    elif paddle.right > WIDTH: paddle.right = WIDTH - 10
    else: paddle.x += voltageRatio * 35

# Create
vAxis = VoltageRatioInput()
hAxis = VoltageRatioInput()

# Address
vAxis.setChannel(0)
hAxis.setChannel(1)

# Open
hAxis.openWaitForAttachment(5000)

# Handle
hAxis.setOnVoltageRatioChangeHandler(horizontalAxisChange)
