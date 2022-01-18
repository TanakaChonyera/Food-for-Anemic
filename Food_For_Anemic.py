############################################################################
#
#   CS programming project #8
#
#   Algorithm
#
#       Start
#       Function definitions
#       Get file pointer
#       Open file & generate dictionary
#       Display alphabetized food list
#       Display alphabetized mineral list
#       Loop while input incorrect ('q', 'Q' terminates loop)
#           Input minerals (validation checks)
#           Call relevant functions
#               Generate specified set
#               Return set
#           Convert set to list and alphabetize
#           Output alphabetized list
#       Output anti-anemia food list
#       End
#
############################################################################
import csv

def open_file():
    ''' This function repeatedly prompts the user for a filename until the file is
opened successfully. '''

    file_valid = False

    fp = input("Please input a file to use: ")

    while file_valid == False:

        # If no file name entered, set default to 'FOOD.txt'
        if fp == '':
            fp = 'FOOD.txt'
            file_valid = True
            fp = open(fp, 'r')
        else:
            try:

                # If file found, make file pointer
                with open(fp, 'r') as file:
                    file_valid = True
                    fp = open(fp, 'r')

            # If File name not found, raise error and re-prompt for input
            except FileNotFoundError:
                print("Invalid filename, please try again")
                file_valid = False
                fp = input("Please input a file to use: ")

    # Return file pointer
    return fp


def read_file(fp):
    ''' This function opens and reads the “FOOD.txt” file and builds a mineral dictionary,
minerals_D , with a dietary mineral as a key and a set of foods as the value. '''

    # Initialize empty dictionary
    mineral_D = {}

    # Open file
    with fp as file:

        reader = csv.reader(file)

        for line_list in reader:

            # Call build_dictionary function generate dictionary
            build_dictionary(mineral_D, line_list)

    # Return dictionary
    return mineral_D


def food_and_minerals(D):
    ''' This function creates a food list and a nutrition list from minerals_D. Each list is
sorted alphabetically. '''

    # Initialize food_set & nutrition_set as empty sets
    food_set = set()
    nutrition_set = set()

    # Iterate through dictionary
    for key, value in D.items():

        # Add key to dictionary
        nutrition_set.add(key)

        # Add values to dictionary
        for mineral in D[key]:
            food_set.add(mineral)

    # Make mineral and food list
    nutrition_list = list(nutrition_set)
    food_list = list(food_set)

    # Sort mineral and food list
    nutrition_list.sort()
    food_list.sort()

    # Return mineral and food lists
    return food_list, nutrition_list

def build_dictionary(D, line_list):
    ''' This adds a key-value entry to the dictionary minerals_D with dietary minerals as key,
and a set of food as value. '''

    # Iterate through line from file
    for i in range(1, len(line_list)):

        # Generate dictionary
        if line_list[i] in D:
            D[line_list[i]].add(line_list[0])
        else:
            D[line_list[i]] = {line_list[0]}


def search(minerals_str, minerals_list, D):
    ''' This function takes in an input string , minerals_str, of three dietary minerals
separated by one of two operators: | (or) or & (and). '''

    # Initialize sets and flags
    food_set = set()
    mineral_1_set = set()
    mineral_1_set_used = False
    mineral_2_set = set()
    mineral_2_set_used = False
    mineral_3_set = set()
    mineral_3_set_used = False
    operator = ''

    # Determine operator and generate search list
    for i in range(len(minerals_str)):

        if minerals_str[i] == '&':
            search_for_list = minerals_str.split('&')
            operator = '&'
            break
        elif minerals_str[i] == '|':
            search_for_list = minerals_str.split('|')
            operator = '|'
            break

    # Validity check - no operator
    if operator == '':
        return None
    else:
        pass

    # Validity check - length of list
    if len(search_for_list) != 3:

        return None

    else:

        # Remove spaces from items in list and make all characters lowercase
        for n in range(len(search_for_list)):
            search_for_list[n] = search_for_list[n].lower()
            search_for_list[n] = search_for_list[n].strip()

        # Validity check - valid minerals
        for mineral in search_for_list:

            if mineral not in minerals_list:

                return None

            else:

                continue

    # Iterate through dictionary
    for key, value in D.items():

        # Generate set of foods with first mineral search criteria and raise flag
        if search_for_list[0] == key:
            mineral_1_set.update(value)
            mineral_1_set_used = True

        # Generate set of foods with second mineral search criteria and raise flag
        elif search_for_list[1] == key:
            mineral_2_set.update(value)
            mineral_2_set_used = True

        # Generate set of foods with third mineral search criteria and raise flag
        elif search_for_list[2] == key:
            mineral_3_set.update(value)
            mineral_3_set_used = True

    # Result for operator & (and)
    if operator == '&':

        # Determine result for 2 or 3 minerals
        if mineral_1_set_used and mineral_2_set_used and mineral_3_set_used:
            food_set.update(mineral_1_set & mineral_2_set & mineral_3_set)
        else:
            food_set.update(mineral_1_set & mineral_2_set)

    # Result for operator & (or)
    elif operator == '|':

        # Determine result for 2 or 3 minerals
        if mineral_1_set_used and mineral_2_set_used and mineral_3_set_used:
            food_set.update(mineral_1_set | mineral_2_set | mineral_3_set)
        else:
            food_set.update(mineral_1_set | mineral_2_set)

    # Return food set
    return food_set


def anti_anemia(D):
    ''' This function returns a set foods with iron. '''

    # Return set of foods with iron
    return D['iron']


#Main function
def main():
    ''' This function opens and reads the file, and then displays the foods and minerals read from the file '''

    # Get file pointer and generate dictionary
    fp = open_file()
    minerals_D = read_file(fp)

    anti_anemia_display = ''

    valid_input = False

    # Get food and mineral list
    food_list, nutrition_list = food_and_minerals(minerals_D)

    print("\nWe consider these {}:".format('foods'))

    # Display food list
    for i in range(len(food_list)):
        print(food_list[i])

    print("\nWe consider these {}:".format('minerals'))

    # Display mineral list
    for j in range(len(nutrition_list)):
        print(nutrition_list[j])

    while True:

        print("\nSpecify three types of minerals separated by &(and) or |(or)")
        minerals_str = input("Please enter 3 minerals using a single operand type (or q to quit): ")

        operators_and = 0
        operators_or = 0

        # Validity check - correct and single type of operator
        for m in range(len(minerals_str)):

            if minerals_str[m] == '&':
                search_for_list = minerals_str.split('&')
                valid_input = True
                operators_and += 1
            elif minerals_str[m] == '|':
                search_for_list = minerals_str.split('|')
                valid_input = True
                operators_or += 1

        # Quit program
        if minerals_str.lower() == 'q':
            break

        elif valid_input and (operators_and == 2 or operators_or == 2):

            # Generate food set
            food_set = search(minerals_str, nutrition_list, minerals_D)

            if food_set is None:

                print("Error in input.")

            else:

                # Make food list and sort
                food_list = list(food_set)
                food_list.sort()

                # Display food list
                for k in range(len(food_list)):
                    print(food_list[k])
        else:
            print("Error in input.")

    # Get anit-anemia set of foods, make list and sort
    anti_anemia_set = anti_anemia(minerals_D)
    anti_anemia_list = list(anti_anemia_set)
    anti_anemia_list.sort()

    # Adjustments for correct output
    for l in range(len(anti_anemia_list) - 1):
        anti_anemia_display += anti_anemia_list[l] + ', '

    anti_anemia_display += anti_anemia_list[len(anti_anemia_list) - 1]

    # Display anti-anemia foods
    print("\nFoods that contain iron, please eat these foods if you are anemic: ")
    print(anti_anemia_display)


#DO NOT DELETE THE NEXT TWO LINES
if __name__ == "__main__":
    main()
