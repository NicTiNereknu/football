# Fotbal (Hokej) / Футбол (игра на бумаге) / Paper soccer 
Python version of traditional paper and pencil game, for more information go to [wikipedia](https://en.wikipedia.org/wiki/Paper_soccer).

GUI is created in [PAGE](http://page.sourceforge.net).

#### Three modes:
 - human vs human
 - human vs ai
 - ai vs ai

#### How AI works (code in ```playerAI.play()```): 
 1. AI tries to find all paths for current field situation.
 2. For every path (from 1.) AI simulates opponent's move, how close can opponent reach AI's goal.
 3. AI chooses one path by filtering results by longest path (from 1.) and farthest path's end to AI goal (from 2.).
 
### Main window
![field](field.jpg)

### Settings window
![field](settings.jpg)

### Compile
Game can be compiled with cx_freeze ```python setup.py build```.
