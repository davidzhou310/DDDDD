from dataclasses import replace
import random
import string

def read_from_file(file_name):
    """
    Reads all words from file
    Parameter file_name is the name of the file
    This function returns a list containing all the words
    """
    f = open(file_name, "r")
    all_words = f.read().splitlines()
    f.close()
    return all_words


def ask_for_length():
    """
    Ask for a number as the length of the word
    Returns the number of hand cards L
    """
    word_length = input("Enter a number between 3 - 10 to be length of the word you are going to guess:")
    while True:
        try:
            word_length = int(word_length)
            if word_length in list(range(3,11)):
                return word_length
            word_length = input("Please Enter a valid number between 3 - 10")
        except ValueError:
            word_length = input("Please Enter a valid number between 3 - 10")


def filter_word_list(all_words, length):
    """
    Given a list of words, and a number, returns a list of words with the specific length
    Parameter all_words is the list of all words
    Parameter length is the given length
    """
    ret_list = []
    for word in all_words:
        if len(word) == length:
            ret_list.append(word)
    return ret_list


def set_up(length):
    """
    Creates a main pile of 26 * length cards, represented as a list of lowercase letters, with length of each letter
    Creates a discard pile of 0 cards, represented as an empty list
    This function returns both lists as a tuple, with the main pile as the first item and the discard pile as the second item
    Parameter length is the given length
    """
    main_pile = []
    for _ in range(length):
        for i in range(26):
            main_pile.append(chr(97 + i))
    return (main_pile, []) #[] is the discard pile
    

def shuffle_cards(pile):
    """
    Parameter pile is the given list of words
    This function shuffles the given pile and doesn't return anything
    """
    random.shuffle(pile)


def move_to_discard_pile(discard_pile, card):
    """
    Move the given card to the top of the discard pile
    Parameter discard_pile is the discard pile
    Parameter card is the given letter to be discarded
    This function doesn't return anything
    """
    discard_pile.insert(0, card)
    

def deal_initial_cards(main_pile, discard_pile, length):
    """
    Start the game by dealing two sets of length cards each, from the given
    main_pile
    This function returns a tuple containing two lists, the first one representing
    the human's hand and the second one representing the computer's hand
    """
    human_hand, computer_hand = [], []
    for _ in range(length):
        computer_hand.append(main_pile.pop(0))
        human_hand.append(main_pile.pop(0))
    move_to_discard_pile(discard_pile, main_pile.pop(0))
    return (human_hand, computer_hand)


def get_first_from_pile_and_remove(pile):
    """
    Return and remove the first item of the given list
    Parameter pile is the list from which to remove the first element
    """
    return pile.pop(0)


def check_bricks(main_pile, discard_pile):
    """
    Check whether the main_pile is empty.
    If so, shuffles the discard_pile and moves all the cards to the main_pile. Then turn over the top card of the main_pile to be the start of the new discard_pile.
    Otherwise, do nothing.
    """
    if not main_pile:
        random.shuffle(discard_pile)
        for _ in range(len(discard_pile)):
            main_pile.append(discard_pile.pop())
        discard_pile.append(main_pile.pop(0))


def get_similarity_level(word, target_word):
    """
    Parameter word is a list of letter split by new word after computer discard one card 
    Parameter target_word is a list of target word to win the game
    This function is to get the similarity level of the word compared with the target word: level 1 is having 1 letter same, level 4 is having 4 letters same, level len(word) is exactly same, which means winning
    """
    #initialize a list which index is the similarity level, value is how many word in target list are in this similarity level compare with the checking word
    similarity_list = [0] * (len(word) + 1)
    for target in target_word:
        count = 0 #count how many letters are same
        for j in range(len(word)):
            if word[j] == target[j]:
                count += 1
        similarity_list[count] += 1
    for level, freq in enumerate(reversed(similarity_list)): #sorted it in descending order and return its index as similarity level
        if freq > 0:
            return len(word) - level #since the index has been reversed
    

def computer_play(computer_hand_cards, main_pile, discard_pile, words):
    """
    Parameter computer_hand_cards is the computer's hand cards
    Parameter main_pile is the main pile
    Parameter discard_pile is the discard pile
    Parameter words is a list of target word to win the game
    return the computer_hand_cards
    """
    print("Computer's turn")
    #check if take the card in the discard_pile
    card_obtained = discard_pile[0]
    possible_list = [] #initialize a list that contains all possible word by replacing with any card in hand 
    for i in range(len(computer_hand_cards)):
        new_list = computer_hand_cards.copy()
        new_list[i] = card_obtained  #replace with new card
        possible_list.append(new_list)
    for word in words:
        word_list = list(word)
        #check if take the card on the top of discard pile and discard one card will win the game
        #if so, take from the discard pile
        if word_list in possible_list: 
            discard_pile.pop(0)
            for i in range(len(word_list)): #find the card been replaced 
                if word_list[i] != computer_hand_cards[i]:
                    discarded_card = computer_hand_cards.pop(i)
                    discard_pile.append(discarded_card) #append the discard card back to discard pile
                    computer_hand_cards = word_list #update the hand card 
                    print(f"Computer picked {card_obtained} from the discard pile to replace {discarded_card}")
                    print("Computer's current hand is", computer_hand_cards)
                    return computer_hand_cards
    #else, take the top card from main pile
    #here we evaluate the similarity of word when replacing it with any existing card in hand and keep the one with the highest similarity level
    card_obtained = main_pile.pop(0)
    print(computer_hand_cards)
    possible_list = [] #initialize a new list that contains all possible word by replacing with any card in hand 
    for i in range(len(computer_hand_cards)):
        new_list = computer_hand_cards.copy()
        cur = new_list[i] #card that been replaced
        new_list[i] = card_obtained  #replace with new card
        possible_list.append((cur, new_list)) 
    discard_card = ''
    max_similarity = 0
    for replace, new_word in possible_list:
        similarity = get_similarity_level(new_word, words) # get the similarity 
        if similarity == len(computer_hand_cards):  #which means win if replace this card
            discard_card = replace
            computer_hand_cards = new_word #update the hand cards
            break
        elif similarity > max_similarity:                   
            discard_card = replace
            max_similarity = similarity
            computer_hand_cards = new_word
    move_to_discard_pile(discard_pile, discard_card) # move to discard pile
    print(f"Computer picked {card_obtained} from the main pile to replace {discard_card}")
    print("Computer's hands card is", computer_hand_cards)
    return computer_hand_cards
                

def ask_for_the_letter_to_be_replaced(length):
    """
    Ask for the index of the letter that the user wants to replace
    Prompt again if the input index is out of range or invalid
    Parameter length is the number of cards in the human's hand
    This function returns the index of the letter to be replaced
    """
    replaced_index = input("Input the index of the letter to be replaced, e.g. '1':")
    while True:
        try: 
            if int(replaced_index) in list(range(length)):
                return int(replaced_index)
            replaced_index = input("Please enter a valid index")
        except ValueError:
            replaced_index = input("Please enter a valid index")


def ask_yes_or_no(msg):
    """
    Displays msg and get user's response
    Prompt again if the input is invalid
    This function returns True if the user answers 'y' or 'yes', and returns False if the user answers 'n' or 'no'
    """
    user_response = input(msg + "Type 'y/yes' to accept, 'n/no' to discard.")
    while True:
        if user_response in ['y', 'yes']:
            return True
        elif user_response in ['n', 'no']:
            return False
        else:
            user_response = input("Please enter a valid response")


def check_game_over(human_hand_cards, computer_hand_cards, words_with_specific_length):
    """
    Check if the game ends
    If there is a tie, the game ends as well
    Parameter human_hand_cards is the human's current hand (list)
    Parameter computer_hand_cards is the computer's current hand (list)
    Parameter words_with_specific_length is a list containing all the words with the specific length
    Returns True if the human or the computer wins the game, otherwise False
    """
    if ''.join(human_hand_cards) in words_with_specific_length or ''.join(computer_hand_cards) in words_with_specific_length:
        return True
    return False


def main():
    # reads all words from file
    all_words = read_from_file("words.txt")
    print("Welcome to the game!")
    # ask for a number as the length of the word
    word_length = ask_for_length()
    # filter all_words with a length equal to the given length
    winning_words = filter_word_list(all_words, word_length)
    # set up main_pile and discard_pile
    main_pile, discard_pile = set_up(word_length)
    # shuffle main pile
    shuffle_cards(main_pile)
    # deal cards to players, creating human_hand_cards and computer_hand_cards
    # and initialize discard pile
    human_hand, computer_hand = deal_initial_cards(main_pile, discard_pile, word_length)
    # start the game
    while True:
        # check if main_pile is empty by calling check_bricks(main_pile, discard_pile)
        check_bricks(main_pile, discard_pile)
        # computer play goes here
        computer_hand = computer_play(computer_hand, main_pile, discard_pile, winning_words)
        # human play goes here
        print("Your turn")
        print("Your word list is:", human_hand)
        print(f"Pick {discard_pile[0]} from DISCARD PILE or reveal the letter from MAIN PILE")
        card_select = input("Reply 'D' or 'M' to respond:")
        while True:
            if card_select == 'D':
                card_ontained_D = discard_pile.pop(0)
                replace_index = ask_for_the_letter_to_be_replaced(word_length)
                word_discard = human_hand[replace_index]
                human_hand[replace_index] = card_ontained_D #replace the card 
                move_to_discard_pile(discard_pile, word_discard) #move the discard card to discard pile 
                print(f"You replaced {word_discard} with {card_ontained_D}")
                print("Your word list is:", human_hand)
                break
            elif card_select == 'M':
                word_obtained_M = main_pile.pop(0)
                print(f"The letter from MAIN PILE is {word_obtained_M}")
                if ask_yes_or_no("Do you want to accept this letter?"):
                    replace_index = ask_for_the_letter_to_be_replaced(word_length)
                    word_discard = human_hand[replace_index]
                    human_hand[replace_index] = word_obtained_M #replace the card 
                    move_to_discard_pile(discard_pile, word_discard) #move the discard card to discard pile 
                    print(f"You replaced {word_discard} with {word_obtained_M}")
                    print("Your word list is:", human_hand)
                else:
                    print(f"You picked {word_obtained_M} from the main pile and choose to discard it")
                    print("Your word list is:", human_hand)
                    move_to_discard_pile(discard_pile, word_obtained_M)
                break
            else:
                card_select = input("Please enter a valid reponse")
        # check if game is over and print out results
        if check_game_over(human_hand, computer_hand, winning_words):
            human_word, computer_word = ''.join(human_hand), ''.join(computer_hand)
            if human_word in winning_words and computer_word in winning_words:
                print(f"Your word is {human_word}, computer's word is {computer_word}")
                print("Tie!")
                print("Your word is", ''.join(human_hand))

            elif human_word in winning_words:
                print(f"Your word is {human_word}")
                print("You Win!")
                print("Your word is", ''.join(human_hand))
            else:
                print(f"computer's word is {computer_word}")
                print("You Lose!")
            break #end the game
            

if __name__ == "__main__":
    main()
