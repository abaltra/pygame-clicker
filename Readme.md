# Pygame websocket demo

Simple app using Pygame to draw some circles on screen and websockets to draw them on other screens

## How to run
This requires [tornado](https://www.tornadoweb.org/en/stable/) and [pygame](https://www.pygame.org/news) to be installed. I recommend using [virtualenv](https://virtualenv.pypa.io/en/latest/) to avoid polluting your global env.

```shell
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

After all the dependencies are installed, just run the server and a couple clients

```shell
python3 server.py &
python3 client.py &
python3 client.py &
```

And click on one of the windows that pop up. You should see the ripple also show up on the other window.

## Motivation
Was bored lol. Also websockets are really interesting and like most coders I've always wanted to make a game. This could be a starting point, who knows.

## License
Use as you will, have fun :D