## Dots and Boxes

![Image of Game Board](https://github.com/swang99/README-img/blob/main/Dots%20and%20Boxes.png)

The classic 2 player pen-and-paper game made in Python.

### Game instructions
1. Run dotsandboxes.py. The game window should open.
1. Two players take turns selecting an edge that connects two dots.
2. When a player completes the fourth edge of a 1x1 box, they earn one point and take another turn. The respective square will be shaded in the player-assigned color. 
3. The game ends when all edges are taken, and the player with the most points wins. 
4. Press 'r' to restart.
5. The default board size is 3x3, though the game supports larger sizes. In the main method, adjust constant DIM to change the board dimension. A board larger than 6x6 will require decreasing cell size constant CELL.  

### Files
dotsandboxes.py - Contains the game interface and logic.

edges.py - Contains a class which draws the board and blits the game's text.

### System requirements
`pygame`
