import itertools
import math
import random

digits = '0123456789'
ALL_CODES = [''.join(p) for p in itertools.permutations(digits, 4)]

def feedback(guess, code):
    strikes = sum(guess[i] == code[i] for i in range(4))
    balls = sum(d in code for d in guess) - strikes
    return (strikes, balls)

def guess_turn(guess, possible_ans, strikes, balls):
    new_possible = []
    for code in possible_ans:
        s, b = feedback(guess, code)
        if s == strikes and b == balls:
            new_possible.append(code)
    return new_possible

def entropy_of_guess(guess, possible_ans):
    outcomes = {}

    for code in possible_ans:
        outcome = feedback(guess, code)

        if outcome not in outcomes:
            outcomes[outcome] = 0
        outcomes[outcome] += 1

    total = len(possible_ans)
    entropy = 0

    for count in outcomes.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy

def best_guess(possible_ans, guess_space=None):
    if guess_space is None:
        guess_space = possible_ans

    best = None
    best_entropy = -1

    for guess in guess_space:
        e = entropy_of_guess(guess, possible_ans)

        if e > best_entropy:
            best_entropy = e
            best = guess

    return best, best_entropy

def top_k_guesses(possible_ans, guess_space=None, k=2):
    if guess_space is None:
        guess_space = possible_ans

    scored = []
    for guess in guess_space:
        e = entropy_of_guess(guess, possible_ans)
        scored.append((guess, e))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


def play_game():
    possible_ans = ALL_CODES[:]
    turn = 1

    print("Think of a 4-digit number with no repeated digits.")
    print("I will try to guess it.\n")

    while True:
        if turn == 1:
            guess = random.choice(ALL_CODES)
            ent = entropy_of_guess(guess, possible_ans)
        else:
            guess, ent = best_guess(possible_ans, possible_ans)

        print(f"Turn {turn}")
        print(f"My guess: {guess}")
        print(f"Remaining possibilities: {len(possible_ans)}")
        print(f"Entropy: {ent}")

        strikes = int(input("Strikes: "))
        balls = int(input("Balls: "))

        if strikes == 4:
            print("Solved!")
            break

        possible_ans = guess_turn(guess, possible_ans, strikes, balls)

        if len(possible_ans) == 0:
            print("No possibilities remain. Check your inputs.")
            break

        print()
        turn += 1