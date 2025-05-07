from termcolor import colored
import random
import sys

testWord = "tests"

print("Guess a word...")

for attempt in range(1,7):
    guess = input().lower()

    for i in range(min(len(guess), 5)):
        if guess[i] == testWord[i]:
            print(colored(guess[i], 'green'), end="")
        elif guess[i] in testWord:
            print(colored(guess[i], 'yellow'), end="")
        else:
            print(colored(guess[i],'red'), end="")
    print()
    
    if guess == testWord:
        print("You guessed the word in %i guesses." %attempt)
    elif attempt == 6:
        print("You didn't guess the word, it was '%s'" %testWord)
