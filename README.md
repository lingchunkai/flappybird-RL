Simple RL for Flappy bird
=========================

How-to
------

1. Install Python 2.7.X from [here](https://www.python.org/download/releases/)

2. Install PyGame 1.9.X from [here](http://www.pygame.org/download.shtml)

3. Clone this repository and extract it.

4. For single player, run `python flappy.py` from the repo's directory

5. Use <kbd>&uarr;</kbd> or <kbd>Space</kbd> key to play and <kbd>Esc</kbd> to close the game.

  (Note: Install pyGame for same version python as above)

  (For x64 windows, get exe [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame))

6. For RL, you will also need numpy, scipy, matplotlib. Run flappybot.py

Issues
------

1. This work was hacked up for fun, which explains the terrible code quality.

2. Code runs really slow because of inefficient coarse coding - I wanted to go for a more generic linear function approximator but decided to do away with it.

Credits
-------

1) Adapted from: https://github.com/sourabhv/FlapPyBird