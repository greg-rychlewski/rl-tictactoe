[Live Demo](http://rl-tictactoe.us-east-2.elasticbeanstalk.com)

**Technologies Used**
---
* AI Logic: Python 3.4
* Frontend: Javascript, HTML, and CSS
* Backend: Python Flask Framework

**Temporal Difference Learning**
---
* Initially, the AI moves randomly unless its next move results in a win.
* Moves leading to a win will become preferred in the future. Similarly, moves leading to a loss or a tie will be avoided, if possible.
* The AI will sometimes make an exploratory move. These moves will ignore what has been learned in the previous games in order to explore alternate strategies.
* [Click here](https://en.wikipedia.org/wiki/Temporal_difference_learning) for more information on temporal difference learning.
