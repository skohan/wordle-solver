
# Author: skohan
# Copyright 2022
# https://github.com/skohan

import clean_dict as clean_dict


GREY = 0
YELLOW = 1
GREEN = 2

class Wordle:
    not_allowed_letters = []
    misplaced_letters = {}
    correct_letters = {}


    def is_not_allowed(word: str, letter: str, index: int) -> bool:
        # insuring that correct letters are at appropriate position
        for letter, index in Wordle.correct_letters.items():
            if word[index] != letter:
                print("Invalid word")
                raise Exception("Invalid word")





def welcome_message() -> None:
    print("Welcome")

def success_message() -> None:
    print("Great!")

def failure_message() -> None:
    print("Sorry")

def check() -> bool:
    response = input("is this the word? y/n\n")
    if response.lower() == 'y':
        return True
    
    return False

def guess(current_word: str) -> None:
    print(f'''
    Try this word:
        {current_word.upper()}
    ''')

def whats_wrong() -> list:
    response = input("Enter result from wordle\n")
    return list(map(lambda x: int(x), response.split()))

def contemplate(colors: list, current_word: str) -> None:
    for i, (color, letter) in enumerate(zip(colors, current_word)):
        print(letter, end=" ")
        if color == GREY:
            Wordle.not_allowed_letters.append(letter)
            continue
        if color == YELLOW:
            if Wordle.misplaced_letters.get(letter) == None:
                Wordle.misplaced_letters[letter] = []
            Wordle.misplaced_letters[letter].append(i)
            continue
        
        # GREEN COLOR
        if Wordle.correct_letters.get(letter) == None:
            Wordle.correct_letters[letter] = []
        Wordle.correct_letters[letter].append(i)
        # remove the index of the word from misplaced word
        try:
            Wordle.misplaced_letters.get(letter).remove(i)
        except:
            pass
    print()

def get_words_from_dictionary() -> list:
    return clean_dict.wordlist

def get_all_indexes(word: str, letter: str) -> list:
    return [i for i, ltr in enumerate(word) if ltr == letter]

def valid_word(word: str) -> bool:
    word = word.upper()
    for i, letter in enumerate(word):
        is_green_letter = False
        for correct_letter in Wordle.correct_letters:
            if i in Wordle.correct_letters.get(correct_letter) and letter != correct_letter:
                return False
            else:
                is_green_letter = True
                break
        
        if is_green_letter:
            continue # we don't have to check later

        if letter in Wordle.misplaced_letters:
            if i in Wordle.misplaced_letters.get(letter):
                return False        
                
        # for letter in Wordle.misplaced_letters:
        #     if letter not in word:
        #         return False
        #     indexes = get_all_indexes(word, letter)
        #     for index in indexes:
        #         if index in Wordle.misplaced_letters.get(letter):
        #             return False

        if letter in Wordle.not_allowed_letters:
            return False
        # if letter in Wordle.misplaced_letters:
        #     if i in Wordle.misplaced_letters.get(letter):
        #         return False


    
    return True



def get_better_word(wordlist: list = []) -> str:
    if len(wordlist) == 0:
        wordlist = get_words_from_dictionary()

    valid_words = []
    
    for word in wordlist:
        if valid_word(word):
            valid_words.append(word)

    wordlist = valid_words

    if len(wordlist) == 0:
        print("No valid word found")
        failure_message()
        raise Exception("Valid words for given input not found")
    
    return wordlist[0].upper()



def main():
    '''
        Main entry
    '''

    welcome_message()

    current_word = "WEARY"
    found = False

    for _ in range(6):
        guess(current_word)
        found = check()
        if found:
            success_message()
            return
        colors = whats_wrong()
        if colors.count(GREEN) == 5:
            success_message()
            return
        contemplate(colors, current_word)
        current_word = get_better_word()

    failure_message()
              

if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except:
    #     print("Exiting")