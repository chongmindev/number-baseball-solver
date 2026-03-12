# Number Baseball Solver using Information Theory

This project implements a solver for the Number Baseball (Bulls and Cows) game using entropy to select the most informative guesses.

The solver evaluates all possible guesses and selects the one that maximizes expected information gain.

## Features
- Entropy-based optimal guess selection
- Simulation of full games
- Web interface built with Flask
- Visualization of solver behavior

## Live Demo
https://number-baseball-solver.onrender.com

## Repository Structure
solver.py — entropy solver implementation  
app.py — Flask web interface  
templates/ — HTML interface  
static/ — styling  

## Running Locally

```bash
git clone https://github.com/chongmindev/number-baseball-solver
cd number-baseball-solver
pip install -r requirements.txt
python app.py
```

## Method

The solver selects guesses that maximize the Shannon entropy of the feedback distribution:

H(X) = - Σ p(x) log₂ p(x)

Higher entropy guesses partition the remaining solution space more evenly, producing more informative feedback and reducing the number of guesses required to solve the game.

## Author
Chong Min  
Stanford University
