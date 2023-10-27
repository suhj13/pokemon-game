import time
import os
import numpy as py
import pandas as pd
import sys

# Must consider type advantages when dealing with how much damage an attack does
# Accessing type advantages excel sheet to apply a multiplier
# Pulled data using Pandas
# Rows are self's type and columns are Pokemon 2's type
df1 = pd.read_excel('database.xlsx', 'typeAdvantages')
# The variable columns gives the header of each column which is excluded in the 2D-array stored in version
columns = list(df1)
version = df1.values

# Pokemon dataframe
df2 = (pd.read_excel('database.xlsx', 'Pokemon')).fillna(py.nan).replace([py.nan], ['None'])

# Pokemon moves
df3 = pd.read_excel('database.xlsx', 'Moves')

# Print a character at a time
def delay_print(s):
    for m in s:
        sys.stdout.write(m)
        sys.stdout.flush()
        time.sleep(0.05)

# Pokemon class
class Pokemon:
    def __init__(self, name, type1, type2, moves, EVs , health = '========================='):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.moves = moves
        self.attack = EVs['ATTACK']
        self.defense = EVs['DEFENSE']
        self.speed = EVs['SPEED']
        self.health = health
        self.bars = 25
        self.status = 0
        self.turnstate = 1

    def damage(self, Pokemon2, move):
        delay_print(f"{self.name} used {move[0]}! ")
        time.sleep(1)

        index1 = 0
        index2 = 0 
        index3 = 0
        for i in range(len(version)):
            if move[1] == version[i][0]:
                break
            index1 += 1

        for j in range(len(columns)):
            if Pokemon2.type1 == columns[j]:
                break
            index2 += 1
        
        for k in range(len(columns)):
            if Pokemon2.type2 == columns[k]:
                break
            index3 += 1
        
        multiplier1 = version[index1][index2]
        multiplier2 = version[index1][index3]

        multiplier = multiplier1 * multiplier2

        Pokemon2.defense /= multiplier
        move[2] *= multiplier
         
        #Pokemon 2 is strong against self
        if multiplier == 0.5:
            string_attack = "It's not very effective...\n"
        
        elif multiplier == 1:
            string_attack = "The opponent is hurt.\n"
        
        # Pokemon 2 is weak against self
        elif multiplier == 2:
            string_attack = "It's super effective!\n"

        string_damaged = "\n" + Pokemon2.name + " has been hit. "
        delay_print(string_damaged)
        delay_print(string_attack)

        # Determine damage
        Pokemon2.bars -= .01*move[2]*self.attack
        Pokemon2.health = ""

        # Add back bars plus defense boost
        for i in range(int(Pokemon2.bars +.1*Pokemon2.defense)):
            Pokemon2.health += "="
        
        # Reset both values
        Pokemon2.defense *= multiplier
        move[2] = int(move[2]/multiplier)

    def fight (self, Pokemon2):
        # Allow the Pokemon to interact with each other

        # Print battle info
        print("POKEMON BATTLE")
        print(f"\n{self.name}")
        print("TYPE/", self.type1, self.type2)
        print("ATTACK/", self.attack)
        print("DEFENSE/", self.defense)
        print("LVL/", 3*(1+(self.attack+self.defense)/2))
        print("\nVS.")
        print(f"\n{Pokemon2.name}")
        print("TYPE/", Pokemon2.type1, Pokemon2.type2)
        print("ATTACK/", Pokemon2.attack)
        print("DEFENSE/", Pokemon2.defense)
        print("LVL/", 3*(1+(Pokemon2.attack+Pokemon2.defense)/2))

        time.sleep(2)
        
        print(f"\n{self.name}\t\tHLTH\t{self.health}")
        print(f"{Pokemon2.name}\t\tHLTH\t{Pokemon2.health}\n")

        # Continue while pokemon have health
        while (self.bars > 0 ) and (Pokemon2.bars > 0):

            if (self.speed < Pokemon2.speed):
                self.turnstate = 0

            state1 = input('What would you like to do Team1?: ')
            if (state1 == 's'):
                self.status = 1
                
            else:
                for i,x in enumerate(self.moves):
                    print(f"{i+1}.", x[0], x[1], x[2])
                index1 = int(input('Pick a move: '))
                global move1 
                move1 = self.moves[index1-1]

            state2 = input('What would you like to do Team2?: ')
            if (state2 == 's'):
                Pokemon2.status = 1
                
            else:
                for i,x in enumerate(Pokemon2.moves):
                    print(f"{i+1}.", x[0], x[1], x[2])
                index2 = int(input('Pick a move: '))
                global move2
                move2 = Pokemon2.moves[index2-1]

            # Self's turn if self is faster than Pokemon2
            if (self.turnstate == 1 and state1 != 's'):
                
                self.damage(Pokemon2, move1)
                
                time.sleep(1)

                print(f"\n{self.name}\t\tHLTH\t{self.health}")
                print(f"{Pokemon2.name}\t\tHLTH\t{Pokemon2.health}")

                # Check to see if Pokemon2 has fainted
                if Pokemon2.bars <= 0:
                    delay_print("\n..." + Pokemon2.name + " has fainted.\n")
                    break
            elif (state1 == 's'):
                break

            # Pokemon 2s turn
            if (Pokemon2.turnstate == 1 and state2 != 's'):

                print(f"It's {Pokemon2.name}'s turn.")
                Pokemon2.damage(self, move2)
                
                time.sleep(1)

                print(f"\n{self.name}\t\tHLTH\t{self.health}")
                print(f"{Pokemon2.name}\t\tHLTH\t{Pokemon2.health}")

                # Check to see if self has fainted
                if self.bars <= 0:
                    delay_print("\n..." + self.name + " has fainted.\n")
                    break
            elif (state2 == 's'):
                break

            # Self's turn if self is slower than Pokemon2
            if (self.turnstate == 0 and state1 != 's'):
                
                self.damage(Pokemon2, move1)
                
                time.sleep(1)

                print(f"\n{self.name}\t\tHLTH\t{self.health}")
                print(f"{Pokemon2.name}\t\tHLTH\t{Pokemon2.health}")

                # Check to see if Pokemon2 has fainted
                if Pokemon2.bars <= 0:
                    delay_print("\n..." + Pokemon2.name + " has fainted.\n")
                    break
            elif (state1 == 's'):
                break
            
            self.turnstate = 1
            Pokemon2.turnstate = 1

# Pulling all necessary data from excel based on user input
def getData():
    i1 = 0
    name = input("Pick a Pokemon: ")
    for i in range(len(df2.values)):
        if name == df2.values[i][0]:
            break
        i1 += 1
    type1 = df2.values[i1][1]
    type2 = df2.values[i1][2]
    moveset = []
    moves =[]

    for i in range(3,7):
        moveset.append(df2.values[i1][i]) 
    index=0
    for i in moveset:
        for j in df3["Move name"]:
            if (i==j):
                temp = []
                for k in range(len(df3.values[index])):
                    temp.append(df3.values[index][k])
                moves.append(temp)
            index += 1
        index = 0
    Pokemon_ = Pokemon(name, type1, type2, moves, {'ATTACK': df2.values[i1][7], 'DEFENSE': df2.values[i1][8] , 'SPEED': df2.values[i1][9]})
    return(Pokemon_)

# Switching function
def switch(arr, index):    
    arr[index], arr[0] = arr[0], arr[index]
    return arr

if __name__ == "__main__":
    team1 = []
    team2 = []

    # Creating teams
    for i in range(2):
        team1.append(getData())
    for j in range(2):
        team2.append(getData())
        
    # Printing out teams
    print("\nTeam 1")
    for i, pokemon in enumerate(team1):
        print(f"{i+1} ", pokemon.name) 
    print("\nTeam 2")
    for j, pokemon in enumerate(team2):
        print(f"{j+1} ", pokemon.name)
    
    while((len(team1) > 0 ) and (len(team2) > 0)):
        team1[0].fight(team2[0])

        if ((team1[0].status == 1) and (team2[0].status != 1)):
            for i, pokemon in enumerate(team1):
                print(f"{i+1} ", pokemon.name)
            member = int(input('Who would you like to switch to?: ')) - 1
            switch(team1,member)
            team2[0].damage(team1[0], move2)
            team1[0].status = 0
            
        elif ((team1[0].status != 1) and (team2[0].status == 1)):
            for i, pokemon in enumerate(team2):
                print(f"{i+1} ", pokemon.name)
            member = int(input('Who would you like to switch to?: ')) - 1
            switch(team2,member)
            team1[0].damage(team2[0], move1)
            team2[0].status = 0
            
        elif ((team1[0].status == 1) and (team2[0].status == 1)):
            for i, pokemon in enumerate(team1):
                print(f"{i+1} ", pokemon.name)
            member = int(input('Who would you like to switch to?: ')) - 1
            switch(team1,member)
            for i, pokemon in enumerate(team2):
                print(f"{i+1} ", pokemon.name)
            member = int(input('Who would you like to switch to?: ')) - 1
            switch(team2,member)
            team1[0].status = 0
            team2[0].status = 0

        else:
            if (team1[0].bars <= 0):
                print('\n')
                for i, pokemon in enumerate(team1):
                    print(f"{i+1} ", pokemon.name, pokemon.health) 
                member = int(input('\nWho would you like to switch to?: ')) - 1
                switch(team1,member)
                team1.remove(team1[member])

            elif (team2[0].bars <= 0):
                print('\n')
                for i, pokemon in enumerate(team2):
                    print(f"{i+1} ", pokemon.name, pokemon.health) 
                member = int(input('\nWho would you like to switch to?: ')) - 1
                switch(team2,member)
                team2.remove(team2[member])
