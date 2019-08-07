# Fotbal (Hokej) / Футбол (игра на бумаге) / Paper soccer 
Python version of traditional paper and pencil game, for more information go to [wikipedia](https://en.wikipedia.org/wiki/Paper_soccer).

GUI created with [PAGE](http://page.sourceforge.net).

#### Three modes:
 - human vs human
 - human vs ai
 - ai vs ai

#### How AI works (code in ```playerAI.play()```): 
 1. AI tries to find longest path with shortest distance to opponents goal.
 2. AI simulates opponents move, how close can opponent reach AI's goal.
 3. AI chooses one path by filtering results from 1. and 2.
 
### Main window
![field](field.jpg)

### Settings window
![field](settings.jpg)

### Compile
Game can be compiled with cx_freeze ```python setup.py build```.
