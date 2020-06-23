import random
import string

good_letters = set()
tried_letters = set();
def change_letter(word, letter):
    res = ""
    good_letters.add(letter)
    for c in word:
        res += c if c in good_letters else '-'
    return res

print("H A N G M A N")
words = 'python', 'java', 'kotlin', 'javascript'
right_answer = random.choice(words)
right_answer_set = set(right_answer)

out = len(right_answer) * "-"

tries = 8
while True:
    mode = input('Type "play" to play the game, "exit" to quit: ').strip()
    print("")
    print(out)
    if mode == "play":
        pass
    elif mode == "exit":
        break
    else:
        break
    while True:
        guess = input('Input a letter: ').strip()
        if len(guess) > 1 or len(guess) == 0:
            print("You should input a single letter\n")
            print(out)
        if guess not in string.ascii_lowercase:
            print("It is not an ASCII lowercase letter\n")
            print(out)
        elif guess in right_answer_set:
            if guess in tried_letters:
                # tries -= 1
                print("You already typed this letter")
                # if tries == 0:
                #     print("You are hanged!")
                #     break
                print("")
                print(out)
                continue
            out = change_letter(right_answer, guess)
            print("")
            print(out)
            tried_letters.add(guess)
            continue
        else:
            if guess in tried_letters:
                # tries -= 1
                print("You already typed this letter")
                # if tries == 0:
                #     print("You are hanged!")
                #     break
                print("")
                print(out)
                continue
            tried_letters.add(guess)
            tries -= 1
            print("No such letter in the word")
            if tries == 0:
                print("You are hanged!")
                break
            print("")
            print(out)
        if '-' not in out:
            print("You guessed the word!\nYou survived!")
            break

# print("""Thanks for playing!
# We'll see how well you did in the next stage""")
