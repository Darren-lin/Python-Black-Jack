'''
Created on Feb 6, 2019
**** FINAL SUBMISSION ****
Darren added some extras to make the game run nicer.
Darren also fixed all the bugs that were mentioned in the last snapshot
Darren added comments to the code to make it easier to understand
The game is running with out any errors and is now done
@author: Darren Lin and Simon Shu
'''


from card import Card
from cards import Cards
from player import Player

# make a BlackjackCard Class inherit from Card
#Returns a numerical value for a card with the function getValue()
class BlackjackCard(Card):
    def getValue(self):
        if self.rank == 'A':
            return(int(11))
        elif self.rank == 'J' or self.rank == 'Q' or self.rank == 'K' or self.rank == '10':
            return(int(10))
        elif self.rank in '23456789':
            return(int(self.rank))
        else:
            raise ValueError('{} is of unknown value'.format(self.rank))      
             
# make a BlackjackHand Class
class BlackjackHand(Cards):
# getTotalWithAce() returns the total of the player's hand with the help of the getvalue function.
# The player's hand total is adjusted based on the amount of Aces in their hand      
    def getTotalWithAce(self): 
        handValue = 0
        aceAmount = 0
        for card in range(len(self.cards)):
            handValue = handValue + int(self.cards[card].getValue())
            if int(self.cards[card].getValue()) == 11: #made it easier to read by indexing the 'A' out instead of "if card == 'A':"
                aceAmount += 1
        while aceAmount > 0 and handValue > 21: #checking if there are any aces in the player's hand and checking if their handValue is over 21 and if it is, the handValue will be adjusted to be less than 21
            handValue = handValue - 10
            aceAmount -= 1
        
        return (handValue)
                      
# bust() returns a boolean based off getTotalWithAce(). 
# Compares the total of the player's hand to 21, if the total is over 21 bust() will return True if not, then False        
    def bust(self):
        if self.getTotalWithAce() > 21:
            return True
        else:
            return False
        
# make a BlackjackPlayer Class
class BlackjackPlayer(Player):
    def __init__(self, name, amount):
        self.name = name
        self.money = amount
        self.hand = BlackjackHand()
        
    def tossHand(self): # gets rid of hand every round
        self.hand = BlackjackHand()
        
    def askHit(self): #Player is asked if he wants to hit or not and while their answer isn't Yes or No/ y or n it will keep asking
        wantToHit = True
        while wantToHit:
            hitTest = input(self.name + ", would you like to hit? (y/n)").lower()
            while hitTest != "y" or hitTest != "n" or hitTest != "Yes" or hitTest != "No":    
                if hitTest == "y":
                    wantToHit = True
                    return True
                if hitTest == "n":
                    wantToHit = False
                    return False
                    break
    
# make a BlackjackDealer Class 
class BlackjackDealer(BlackjackPlayer):
    def askHit(self): #overrides Player's askHit(). If the total of the Dealer's hand is less than 17 he is required to hit.
        if self.hand.getTotalWithAce() < 17:
            return True
        else:   
            return False
        
    def bust(self): # If the Dealer hits and his total is over 21 he busts and the bust method returns True, if he doesn't bust and his total is over 17 but less than 21 it returns False
        if self.hand.getTotalWithAce() > 21:
            return True
        else:
            return False
# make a BlackjackGame function
def BlackjackGame():
        
    # make the 2 players
    dealer = BlackjackDealer("Dealer", 1)
    print("Welcome to Blackjack!!")
    name = input("What is your name?")
    player = BlackjackPlayer(name, 1)
    print("Hi {}!!".format(name))
    howToplay = input("Do you know how to play? y/n\n").lower() #asking the player if they know how to play
    while howToplay != 'n' and howToplay != 'y' and howToplay != 'yes' and howToplay != 'no':
        howToplay = input("Do you know how to play? y/n\n").lower()
    if howToplay == 'n'or howToplay == 'no':
        print("**** RULES ****")
        print("1. Objective of the game is to get as close to or get a total of 21")
        print("2. All players including the dealer start with 2 cards, however, the players two cards are always face up while the dealer only has one card faced up at the start.")
        print("3. The dealer's hand is revealed to the player after the player finishes hitting")        
        print("4. The value of all the face cards is 10")
        print("5. The value of an Ace card is adjusted automatically to help the total of your hand to be 21 or as close to 21 as possible with out going over")
        print("6. You can either Hit or Stand, hitting means you draw one more card and Standing means you are done hitting or not hitting at all")
        print("7. The total of your hand can not be over 21 or else you bust. If you bust you lose!\n")   
    
    while True: #This will ask for a number response and it will keep asking until one is received. If the player enters in a letter for the amount of rounds it will keep asking until he enters a number.
        try: 
            numRounds = int(input("Please enter a number, how many rounds would you like to play?\n"))
        except ValueError:
            continue
        else:
            break
        
    # make a deck of card
    deck = Cards()  # make empty deck
    # add the 52-cards and shuffle
    SUIT = ['h', 'd', 's', 'c']
    RANK = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    for rank in RANK:
        for suit in SUIT:
            deck.add(BlackjackCard(rank,suit))
    deck.shuffle()
    print("**** SHUFFLING NEW DECK **** ")
    deckAmountLeft = 52 # this tells the player how many cards are left in the deck and with this number we can shuffle the deck when its less than 15
    
    # make rest of the game
    DealerNatBlackjack = False
    PlayerNatBlackjack = False
    playerScore = 0
    dealerScore = 0
    Rounds = 1 # can't have 0 rounds
    while Rounds != int((numRounds)) + 1: # will keep playing until number of rounds asked is hit
        print("\n[ Round", Rounds,"] Score: Dealer" ,dealerScore, "vs.",name, playerScore)
        
        
        # PLayer and Dealer are drawing two cards each
        drawCard = 0
        while drawCard < 2:
            player.addCard(deck.deal())
            dealer.addCard(deck.deal())
            drawCard += 1
        deckAmountLeft -= 4 #deck amount subtracts 4 because there aren't 52 cards in the draw able deck anymore
            
        print("Dealer's hand: [")
        print(dealer.hand.cards[1],"??]")
        print("Your hand:", player.hand,"=>", player.hand.getTotalWithAce()) 
        
        #getting the total of both dealer and player and testing for a natural black jack
        dealerTotal = dealer.hand.getTotalWithAce()
        dealerNatBlackjack = (dealerTotal == 21)
        playerTotal = player.hand.getTotalWithAce()
        playerNatBlackjack = (playerTotal == 21)             
        
        #This is the Player's Hitting code. 
        #by calling the askHit() method under BlackjackPlayer class which returned a True or False
        while True:           
            if playerNatBlackjack == True:
                break # break out of loop if natural Black jack is True because player doesn't need to hit
            playerMove = player.askHit()   
            while playerMove == True:            
                if playerMove == True:
                    player.addCard(deck.deal())
                    deckAmountLeft -= 1 # subtracting from deckAmountLeft each time player hits
                    playerTotal = player.hand.getTotalWithAce()
                    print("Your:",player.hand,"=>",playerTotal)
                    if playerTotal == 21:
                        break # break out of loop if the player total is 21 after hitting
                    if player.hand.bust() == True:
                        break # break out of loop if the player busts while hitting
                    playerMove = player.askHit()
            if playerMove == False: # if the player doesn't want to hit or hit anymore
                playerTotal = player.hand.getTotalWithAce()
                print("Your:",player.hand,"=>",playerTotal)
                if player.hand.bust() == False and playerMove == False:
                    playerTotal = player.hand.getTotalWithAce()
                if player.hand.bust() == True:
                    playerTotal = player.hand.getTotalWithAce()
            break #breaks out of the loop after player is finished hitting
                
        playerTotal = player.hand.getTotalWithAce()
        dealerTotal = dealer.hand.getTotalWithAce()
        
        print("Dealer:", dealer.hand,"=>", dealerTotal) # prints all of the dealer's hand with out "??"
        while dealerTotal < 17:
            if playerNatBlackjack == True:
                break # breaks out of hitting loop if dealer has a natural blackjack
            dealer.addCard(deck.deal())
            deckAmountLeft -= 1 # subtracts 1 from Deck amount each time dealer needs to hit
            dealerTotal = dealer.hand.getTotalWithAce()
            print("Dealer:", dealer.hand,"=>", dealerTotal)
            if dealer.hand.bust() == True:
                break #if the dealer busts while hitting break out of the loop
            
        # Comparing the total of player and dealer after they are done hitting       
        if dealerTotal > 0:
            if dealerTotal < playerTotal and playerTotal <= 21:
                print(name, "wins", int(playerTotal), "vs.", int(dealerTotal))
                playerScore += 1
            elif dealerTotal > playerTotal and dealerTotal <= 21:
                print("Dealer wins", int(dealerTotal), "vs.", int(playerTotal))
                dealerScore += 1
            elif dealerTotal == playerTotal:
                print("Tie!!", playerTotal, "vs." ,dealerTotal)
            elif player.hand.bust() == True and dealerTotal <= 21:
                print("Dealer wins!!", name, "busts with", playerTotal)
                dealerScore += 1
            elif dealer.hand.bust() == True and playerTotal <= 21:
                print(name, "wins!! Dealer busts with", dealerTotal)
                playerScore += 1
            elif DealerNatBlackjack == True and playerTotal < 21:
                print("Blackjack!! Dealer wins!! 21 vs.", int(playerTotal))
                dealerScore += 1
            elif PlayerNatBlackjack == True and dealerTotal < 21:
                print("Blackjack!! ", name, "wins!! 21 vs.", int(dealerTotal)) 
                playerScore += 1
            elif PlayerNatBlackjack == True and DealerNatBlackjack == True:
                print("Push", playerTotal, "vs." ,dealerTotal)
            elif player.hand.bust() == True and dealer.hand.bust() == True:
                print("Both busted", playerTotal, "vs." ,dealerTotal)
        print(deckAmountLeft, "cards are left in the deck") # tells the player how many cards are left in the deck
        #tosses hand after every round
        player.tossHand()
        dealer.tossHand()                    
        Rounds += 1 #changes round
        
        # if the deckAmount is less than 15, create a new deck and shuffle. changes deck amount to 52 again because its a new deck
        if deckAmountLeft < 15:
            deck = Cards()
            for rank in RANK:
                for suit in SUIT:
                    deck.add(BlackjackCard(rank,suit))
            deck.shuffle()
            deckAmountLeft = 52
            print("**** SHUFFLING NEW DECK **** ")
            
    print("------------------------------------ ")
    print("| Final Score: Dealer", dealerScore ,"vs.",name, playerScore)
    print("------------------------------------ ")
        
def main():
    BlackjackGame()
    
    
if __name__ == "__main__":
    main()
    
        

