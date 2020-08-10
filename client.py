# Simple pygame program

# Import and initialize the pygame library
import pygame
import random
import math
import json

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect

class Circle:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.r = 2
        print(f"circle created at {self.pos[0]}, {self.pos[1]}")

class Game:
    def __init__(self, url, timeout):
        pygame.init()
        # Each client needs its own id to identify the sender of the message. We can definitely make a better one with something like a Guid, but this'll do
        self.id = random.randint(1, 100);

        self.S_WIDTH = 500
        self.S_HEIGHT = 500
        self.SCREEN_CROSS = math.sqrt(self.S_WIDTH**2 + self.S_HEIGHT**2)

        # Set up the drawing window
        self.screen = pygame.display.set_mode([self.S_WIDTH, self.S_HEIGHT])
        self.running_circles = []

        # Run until the user asks to quit
        self.running = True

        self.url = url

        self.timeout = timeout
        self.ioloop = IOLoop.instance()

        # Let the game loop be ran by IOLoop so we can also use websockets
        self.ioloop.run_sync(lambda: self.run())

    def msg(self, msg):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message(json.dumps(msg))

    @gen.coroutine
    def handle_msg(self, msg):
        print(f"received {msg}")
        d = json.loads(msg)
        
        if d['id'] == self.id:
            # If we sent this message, just ignore it
            print(f"message id {d['id']} matches instance id {self.id}. Skipping")
            return

        c = Circle((d['x'], d['y']), (d['r'], d['g'], d['b']))
        print("appending new circle")
        self.running_circles.append(c)

    @gen.coroutine
    def run(self):
        self.ws = yield websocket_connect(self.url, on_message_callback=self.handle_msg)
        while self.running:
            # Fill the background with white
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                # Did the user just click the screen?
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos();

                    # Create new circle with random color
                    c = Circle(pos, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

                    # Notify the server
                    self.msg({ 'id': self.id, 'x': c.pos[0], 'y': c.pos[1], 'r': c.color[0], 'g': c.color[1], 'b': c.color[2] })

                    # Add it to local set
                    self.running_circles.append(c)
                                
                # Did the user click the window close button?
                if event.type == pygame.QUIT:
                    self.quit()
                    return;

            # Draw all circles
            for i, circle in enumerate(self.running_circles):
                pygame.draw.circle(self.screen, circle.color, circle.pos, math.floor(circle.r), 2)
                circle.r += 0.1
                if (circle.r > self.SCREEN_CROSS):
                    # If the radius is larger than the cross section of the screen, the circle is def out of view. Remove it
                    print(f"Removing cicle started in {circle.pos}")
                    self.running_circles.pop(i)

            # Flip the display
            pygame.display.flip()

            # Need to yield control back to current loop. Without this IOLoop won't be able to receive new messages from the service. It took me way too long to figure this out.
            yield None

    def quit(self):
        self.running = False
        pygame.quit()

if __name__ == "__main__":
    game = Game("ws://localhost:8888/ws", 5)