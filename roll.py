#double gear dice roller: a realm rerolled (v2.1)
#now it won't suck
#shoutouts to https://regexr.com/
#   TO DO, BUT MAYBE IN v3.0:
#   default flags
#   save to and read from text file
#   more game aliases
#   local variables
#   FLAG LIST:
#   (a)dvantage
#   (d)isadvantage
#   default dice (tN)ype
#   (eN)xploding dice
#   (sN)uccess checks
#   (rN)epeated rolls
#   (i)gnore default flags
#   (h)ide individual rolls

from random import *
import re

def print_input_info(): #basic function for organizational purposes
    print('\nformat: xdy + z + dw... !flags #roll comment here')
    print('q to quit, f for flags and formatting, ![flags] to set default flags.')
    print('e for example inputs.')

def re_nf(pattern, string, group = 1, default = 0): #function to check for numeric flags with regex and a capture group
    match = re.search(pattern, string) #defaults to capture group 1 and return 0 on fail
    if (match != None):
        return int(match.group(group))
    return default

roll_input = '' #input string
roll_str = '' #rolls string
flag_str = '' #flags string
comment_str = '' #comment string
work_int = 0 #working int for stuff
work_str = '' #working string during parsing
work_list = [] #for roll list parsing in multiple steps for neater regex
roll_list = [] #seperated list of rolls. thanks, regex!
roll_total = 0 #the roll total, aka the important thing. can also count successes!
r = 0 #current roll
r1 = 0 #second current roll for advantage
roll_invalid = False #validity error handler
fate_roll = ['-', 'o', '+']

#per-roll flags
f_adv_type = 0 #0 = no advantage, 1 = advantage, 2 = disadvantage
f_default_dice_type = 0 #for default die, ie rolling 2d with default 6 will roll 2d6. 0 means no default
f_exploding_dice = 0 #exploding dice. 0 means off, >= N explodes.
f_success_check = 0 #success checks. 0 means off, >= N counts a success, reports successes instead of total number rolled
f_roll_repeat = 1 # performs whole roll N times
f_hide_individual_rolls = False #use to hide individual rolls instead of showing them. might want this if you roll 100d20

#default flags
df_adv_type = 0 #adv is a bit complicated because there's two states that can't both be set
df_default_dice_type = 0
df_exploding_dice = 0
df_success_check = 0
df_roll_repeat = 1
df_hide_individual_rolls = False
#note that ignore defaults doesn't actually need a flag! it is checked and executed at the same time.

print('-- double gear dice roller: a realm rerolled (v2.0) --')
print_input_info()
print('')

roll_input = input('> ') #take input for the first time

while (roll_input != 'q'): #while loop of the dice roller. starts with user input, ends on q
    if (roll_input == ''): #hello from 2021 i found an edge case 2019 alexis sucks at programming
        pass
    
    elif (roll_input == 'f'): #display formatting and flags
        print_input_info()
        print('\nflags:\t\t\tgame aliases:\n')
        print('(a)dvantage\t\tshadowrun\n(d)isadvantage\t\t(shadowrun, !sr)')
        print('default dice (tN)ype\tnew world of darkness\n(eN)xploding dice\t(nwod, acc, !nw, new world of darkness)')
        print('(sN)uccess check\n(rN)epeated rolls\n(i)gnore default flags\n(h)ide individual rolls\n')
        print('flags with N require a number following the flag.\n!e6 would indicate rolls of 6 or greater explode.')
        print('use !ad to roll no advantage while advantage or disadvantage is default.\n')
        print('df + x #comment for fate/fudge dice.\n')
    
    elif (roll_input.lower() == 'shadowrun' or roll_input.lower() == 'sr'): #shadowrun shortcuts to !sr = t6s5
        df_default_dice_type = 6
        df_success_check = 5
        df_adv_type = 0
        df_exploding_dice = 0
        df_roll_repeat = 1
        df_hide_individual_rolls = False
        print('\nshadowrun defaults set.\n')
    
    elif (roll_input.lower() == 'nwod' or roll_input.lower() == 'acc' or roll_input.lower() == 'new world of darkness' or roll_input.lower() == 'nw'): #set nwod
        df_default_dice_type = 10
        df_success_check = 8
        df_adv_type = 0
        df_exploding_dice = 10
        df_roll_repeat = 1
        df_hide_individual_rolls = False
        print('\nnew world of darkness defaults set.\n')
    
    elif (roll_input[0] == '!'): #default flags statement
        #game alias flags. these are first so they can be overriden!
        if (roll_input.find('sr') != -1): #shadowrun - t6s5
            df_default_dice_type = 6
            df_success_check = 5
        if (roll_input.find('nw') != -1): #new world of darkness / acc - t10e10s8
            df_default_dice_type = 10
            df_success_check = 8
            df_exploding_dice = 10
        #the simple flags. str.find() works well enough
        if (roll_input.find('a') != -1): #advantage flag
            df_adv_type = 1
        if (roll_input.find('d') != -1): #disadvantage flag
            if (roll_input.find('a') != -1): #d and a cancel out
                df_adv_type = 0
            else:
                df_adv_type = 2
        elif (roll_input.find('a') == -1): #if no adv or dis, reset df_adv_type
            df_adv_type = 0
        if (roll_input.find('h') != -1): #hide individual rolls flag
            df_hide_individual_rolls = True
        else: df_hide_individual_rolls = False
        #the letter-number flags. uses re_nf() to directly return the number. 0 means off, basically.
        df_exploding_dice = re_nf(r'e(\d+)', roll_input) #exploding dice minimum
        df_success_check = re_nf(r's(\d)+', roll_input) #success check minimum
        df_roll_repeat = re_nf(r'([^s]|^)r(\d+)', roll_input, 2, 1) #repeated roll multiplier
        df_default_dice_type = re_nf(r't(\d+)', roll_input) #default dice type
        print('\ndefault flags set.\n')
    
    elif (roll_input == 'e'): #some example inputs
        print_input_info()
        print('\n> 2d20 + 5\n\nrolls 2 20-sided dice and adds 5 to the total.\n')
        print('> !ae6t6\n\nsets advantage, rolls of 6+ explode, and default die is 6 as default flags\n')
        print('> shadowrun\n\nsets flags for shadowrun rolls to default.\n')
        print('> 10d10 - 5 !hir4 #to hit\n\nrolls 10d10 - 5 four seperate times. (to hit) is noted next to the result.\ndefault flags are ignored, and the indidual rolls are hidden.\n')
        print('> df - 1 #lockpicking check\n\nrolls 4 fate/fudge dice (-0+), subtracts one, and echoes comment \'lockpicking check.\'\n')
    
    elif (roll_input[0].lower() == 'd' and roll_input[1].lower() == 'f'): #fate roll! this is its own code because i didn't want to rewrite the whole thing again for features no one will use
        if (roll_input.find('#') != -1): #looking for a comment
            work_str, comment_str = roll_input.split('#', 1) #parse out comment at first #
        else: #no comment found
            work_str = roll_input
        work_str = work_str.replace(' ', '')
        for i in work_str:
            if (i != 'd' and i != 'f' and i != '+' and i != '-' and i.isdigit() != 1): #if invalid char
                print('\nInvalid fate roll.\n')
                roll_invalid = True
        if (roll_invalid == False):
            r1 = re.search(r'(\+|-)(\d+)', work_str) #will find the operator (+/-) and bonus, or return None if it cannot do that correctly
            print('') #spacing
            for i in range(0, 4): #roll 4 times
                r = randint(1, 3) - 1 # 0-2
                roll_total += r - 1 #-1 - 1
                print(fate_roll[r], end = '') #prints -, 0, or +
            print(f': {roll_total}\n') #a fate roll (with + 3) print will look like ++0-: 1 \n\n 4
            if (r1 != None): #add bonus
                roll_total += int(r1[2]) * -1 if r1[1] == '-' else int(r1[2])
            print(roll_total, end = '')
            print(f' ({comment_str})' if comment_str != '' else '', end = '\n\n')
    
    else: #ok, it's a roll input! or garbage!

        #parse apart the roll by comment first

        if (roll_input.find('#') != -1): #looking for a comment
            work_str, comment_str = roll_input.split('#', 1) #parse out comment at first #
        else: #no comment found
            work_str = roll_input
        
        work_str = work_str.lower() #lowercase it all
        
        #process flags
        
        if (re.search(r'!\w+\W+\w', work_str) != None): #checks for a flag string followed by more rolls
            print_input_info()        
        else:
            if (work_str.find('i') != -1): #reset default flags if i is set
                f_adv_type = 0
                f_default_dice_type = 0
                f_exploding_dice = 0
                f_success_check = 0
                f_roll_repeat = 1
                f_hide_individual_rolls = False
            else: #else, set to default flags
                f_adv_type = df_adv_type
                f_default_dice_type = df_default_dice_type
                f_exploding_dice = df_exploding_dice
                f_success_check = df_success_check
                f_roll_repeat = df_roll_repeat
                f_hide_individual_rolls = df_hide_individual_rolls
            
            if (work_str.find('!') != -1): #check for flag string
                roll_str, flag_str = work_str.split('!') #splits across !
                
                #game alias flags. these are first so they can be overriden!
                
                if (flag_str.find('sr') != -1): #shadowrun - t6s5
                    f_default_dice_type = 6
                    f_success_check = 5
                if (flag_str.find('nw') != -1): #new world of darkness / acc - t10e10s8
                    f_default_dice_type = 10
                    f_success_check = 8
                    f_exploding_dice = 10
                
                #the simple flags. str.find() works well enough
                
                if (flag_str.find('a') != -1): #advantage flag
                    f_adv_type = 1
                if (flag_str.find('d') != -1): #disadvantage flag
                    if (flag_str.find('a') != -1): #d and a cancel out, unless a is set by default, in which case d overrides
                        f_adv_type = 0
                    else:
                        f_adv_type = 2
                if (flag_str.find('h') != -1): #hide individual rolls flag
                    f_hide_individual_rolls = True
                
                #the letter-number flags. uses re_nf() to directly return the number. 0 means off, basically. if re_nf returns zero, aka flag is not set, the present value will not be overwritten.
                
                work_int = re_nf(r'e(\d+)', flag_str) #exploding dice minimum
                f_exploding_dice = work_int if work_int != 0 else f_exploding_dice
                work_int = re_nf(r's(\d)+', flag_str) #success check minimum
                f_success_check = work_int if work_int != 0 else f_success_check
                work_int = re_nf(r'([^s]|^)r(\d+)', flag_str, 2) #repeated roll multiplier
                f_roll_repeat = work_int if work_int != 0 else f_roll_repeat
                work_int = re_nf(r't(\d+)', flag_str) #default dice type
                f_default_dice_type = work_int if work_int != 0 else f_default_dice_type

            else: #no flag string
                roll_str = work_str

            #clean up and process the roll string

            roll_str = roll_str.replace(' ', '') #strip whitespace from roll
            if (re.search(r'd([^f\d]|$)', roll_str) != None and f_default_dice_type > 0): #if a default dice type is set or default fate dice is on,
                roll_str = re.sub(r'(d)([\D]|$)', (r'\g<1>' + str(f_default_dice_type) + r'\g<2>'), roll_str) #replace blank dice
            roll_str = re.sub(r'(\D)d', r'\g<1>1d', roll_str) #turn dX in middle into 1dX
            roll_str = re.sub(r'^d', '1d', roll_str) #dX at start

            #input validation

            for i in roll_str:
                if ((i != '+') and (i != '-') and (i != 'd') and (i.isdigit() != 1)): #if invalid characters in roll, error out
                    roll_invalid = True
            if (roll_invalid == True): #generic error message for invalid char
                print_input_info()
                print('')
            if (re.search(r'd\D', roll_str) != None): #if there are any un-typed dice (which would have been typed by a few lines ago's regex), error out
                roll_invalid = True
                print('Un-typed dice (Xd) cannot be used unless a default dice type is set.\n')
            if (f_exploding_dice == 1): #exploding dice cannot be 1 or it will infinite loop rolling -_-
                roll_invalid = True
                print('Dice cannot explode at 1.\n') #NICE TRY
            
            if (roll_invalid == True):
                roll_invalid = False

            else: #good roll (hopefully)
                print(f'\nrolling {roll_str}', end = '')
                if (f_adv_type == 1): #now print flag statements. uuuughhhhhhhhhhh messy for simple result
                    print(f' with advantage', end = '')
                elif (f_adv_type == 2):
                    print(f' with disadvantage', end = '')
                if (f_exploding_dice > 0):
                    print(f', {f_exploding_dice}+ explodes', end = '')
                if (f_success_check > 0):
                    print(f', versus {f_success_check}', end = '')
                if (f_roll_repeat == 2):
                    print(f', twice', end = '')
                elif (f_roll_repeat > 2):
                    print(f', {f_roll_repeat} times', end = '')
                print(':', end = '')
                print('\n\n' if f_hide_individual_rolls == False else '', end = '')

                #now to actually roll dice let's gooo

                work_list = re.findall(r'([+-])?(\d+)d?(\d+|f)?', roll_str) #grabs the next roll or bonus string, including the (possible) + or - to its left, puts it into a list as individual entries of sign, count/bonus, and type
                roll_list = [dict( #turns the raw tuple list into a clean dictionary list. thank you cecily for writing this bit, oh my gosh
                    {'sign': -1 if match[0] == '-' else 1, #sign is -1 if - or 1 otherwise
                        'count': int(match[1]), #die count / bonus is just casted to int
                     'type' : int(match[2]) if match[2] != '' else '' #if it's a number (Xd>>Y<<), stays a string for now. f stays f, else (only blank) stays blank.
                    }) for match in work_list]
                for i in range(0, f_roll_repeat): #repeats the whole roll a number of times
                    for die in roll_list: #ROLL DICE, BABY
                        if (die['type'] == ''): #static bonus
                            roll_total += (die['sign'] * die['count'])
                        else: #it's a roll. now we have fun!
                            j = 0
                            print(', ' if (f_hide_individual_rolls == False and die != roll_list[len(roll_list) - 1] and die != roll_list[0]) else '', end = '')
                            while (j < die['count']): #roll dice count number of times
                                if (f_adv_type != 0): #dis/adv
                                    r = randint(1, die['type'])
                                    r1 = randint(1, die['type'])
                                    if (f_hide_individual_rolls == False):
                                        if ((r >= r1 and f_adv_type == 1) or (r < r1 and f_adv_type == 2)):
                                            print(f'(*{r}*, {r1})', end = '')
                                        else:
                                            print(f'({r}, *{r1}*)', end = '')
                                    r = r1 if ((r1 >= r and f_adv_type == 1) or (r1 < r and f_adv_type == 2)) else r #the fact that you can do this in python blows my c-based mind
                                else: #no advantage
                                    r = randint(1, die['type'])
                                    print(r if f_hide_individual_rolls == False else '', end = '') #print roll unless don't print roll
                                if (r >= f_success_check and f_success_check > 0): #if it's a successful success check...
                                    roll_total += (die['sign'] * 1) #... increment the roll counter (or decrement if neg dice??)
                                    print('!' if f_hide_individual_rolls == False else '', end = '') #marks ! next to a die if it succeeded. ! is also used for exploding, so success and explode is !!
                                elif (f_success_check == 0): #if it's a failed success check, do nothing. if it's not a success check, add dice the normal way!
                                    roll_total += (die['sign'] * r) #else, add roll*sign to roll counter
                                if (r >= f_exploding_dice and f_exploding_dice > 0): #exploding dice
                                    j -= 1 #decrement counter so it rolls again
                                    print('!' if f_hide_individual_rolls == False else '', end = '') #marks exploded die with !
                                j += 1
                                if (f_hide_individual_rolls == False and j < die['count']): #print spacing between dice
                                    print(' ', end = '') #print a space before next roll if it's not the last roll of an XdY and not the last XdY
                            
                    print(f'\n\n{roll_total}', end = '')
                    print(f' ({comment_str})\n' if comment_str != '' else '\n')
                    roll_total = 0

    roll_input = ''
    roll_str = ''
    flag_str = ''
    comment_str = ''
    work_str = ''
    work_list = []
    roll_list = []
    roll_total = 0
    r = 0
    r1 = 0
    roll_invalid = False
    
    roll_input = input('> ') #start while loop over