"""
School management system, Ritchie Yapp (leader - user interface, encryption and decryption, passcodes and reset), Thaddeus hooi (database amend and delete), Eleazar Chee (database create and search), Jia En (FAQ section)
"""

import random
import base64
import time
import os.path

encryption_data = ""
dafinal = ""
useless_input = ""
newstrink = ""
newestString = ""
lifesave = 0
dAccess = 0
initState = 0

#THIS FUNCTION ENCRYPTS ALL DATA INSIDE A TEXT FILE STORING DATA
#THE FUNCTION HASHES THE PLAIN TEXT BY REARRANGING CHARACTERS BY A RANDOMLY GENERATED LIST OF INDEXES
#THIS IS FOLLOWED BY USING base64 TO MAKE THE APPENDED LIST OF INDEXES AND PERPENDED REARRANGED DATA STRING UNREADABLE AND THEREFORE HARD TO REVERSE
#A THIRD ENCRYPTION METHOD IS USED IN THE EVENT THAT ANY INTRUDERS CAN SEE THAT IT USES A base64 ENCRYPTION
#THE THIRD ENCRYPTION METHOD USES CEASAR CIPHER, THE SHIFTING OF ASCII CHARCTERS BY RANDOM INDEX WHICH IS APPENDED AT THE END SO THAT IT IS REVERSABLE BY DECRYPTION
#generate random algorithm
def generate_alg(encryption_data):
    encryption_alg = []
    while len(encryption_alg) != len(encryption_data):##repeat until full width 
        random_number = None #0 makes the below statements equate to true
        while random_number not in encryption_alg:
            random_number = random.randint(0, len(encryption_data)-1)
            if random_number not in encryption_alg:
                encryption_alg.append(random_number)##append only if the number is not repeated
    return encryption_alg
    


def encryption():
    appendinglist = []
    encryptiondata = "-"
    fh = open("profile.txt", "r+")
    encryptionbata = fh.readlines()
    fh.close()
    for x in range(len(encryptionbata)):
        encryption_data = encryptionbata[x]
        random_number = 0
        new_data = 0
        
        #random algorithm           
        original_alg = []
        encryption_alg = original_alg
        for x in range(len(encryption_data)):
            original_alg.append(x) ##to check its actually rearranged
        if len(encryption_data) > 1: ##impossible to rearrange len(1)    
            while original_alg == encryption_alg: #if both algs are the same
                encryption_alg = generate_alg(encryption_data)
        #string slicing--------------------------------E
        new_data = ""
        read_string = 0
        for x in range(len(encryption_data)): #write new string with rearranged 
            new_data += encryption_data[encryption_alg[x]]  
        for x in range(len(encryption_data)):
            new_data += str(encryption_alg[x])
            new_data += ","
            read_string += len(str(encryption_alg[x])) + 1  
        new_data += "."
        new_data += str(read_string)#for reading the algorithm properly

        #b64---------------------------------------------------E
        enc_byte = 0
        enc_byte = base64.b64encode(new_data.encode("utf-8"))#convert to type bytes
        enc_str = 0
        encodedString = str(enc_byte, "utf-8")#convert to type str (utf-8 encoding required to avoid any exceptions for chars bigger than 0x7F)
        #caesar------------------------------------------------E
        newString = ""
        newstrink = ""
        global appendingstring
        randomno = random.randint(-5,5) #index difference
        for x in range(len(encodedString)):
            letter = encodedString[x]
            newString += chr(ord(letter) + randomno)
        newstrink = newString + str(randomno) + str(len(str(randomno)))
        appendinglist.append(newstrink)
    appendingstring = "\n".join(appendinglist)

    fh = open("profile.txt", "w")
    fh.write(appendingstring)
    fh.close()

#THIS FUNCTION IS TO DECRYPT ALL STORED DATA TO BE READ AND OUTPUT AS READABLE PLAIN TEXT
#THIS REVERSES THE ALGORITHM USED IN encryption()
    
def decryption():
    fh = open("profile.txt", "r+")
    apple = ""
    store = fh.readlines()
    fh.close()
    for x in range(len(store)):
        newstrink = store[x]
        #caesar-----------------------------------------------D
        newestString = ""
        slicingindex = 0
        if newstrink[-1] == "\n":
            slicingindex = int(newstrink[-2])
            randomno = int(newstrink[-2-slicingindex:-2])##based on slicing index determines offset
            for x in range(len(newstrink[:-2-slicingindex])):
                letter = newstrink[x]
                newLetter = chr(ord(letter) - randomno) ##generates new letter by changing ascii
                newestString += newLetter ##appends new letter to string
        else:
            slicingindex = int(newstrink[-1])
            randomno = int(newstrink[-1-slicingindex:-1])
            for x in range(len(newstrink[:-1-slicingindex])):
                letter = newstrink[x]
                newLetter = chr(ord(letter) - randomno) ##generates new letter by changing ascii
                newestString += newLetter ##appends new letter to string
        #b64------------------------------------------------D
        n3wstring = ""
        bruhstring = ""
        bruhstring = base64.standard_b64decode(newestString)##data in type bytes
        n3wstring = str(bruhstring, "utf-8")##data in type str

        #stringslicing----------------------------------------D
        dafinal = "" ##final decrypted data
        read_pos = 0 ##this variable reads the length of the algorithm to determine extract_pos
        extract_pos = 0 ##this position divides the algorithm and data
        string_alg = "" ##the extracted slicing algorithm in type str
        the_other = 0 ##half of the string to extract data or algorithm
        the_other = int(len(n3wstring) / 2)
        ##extract algorithm
        appending_no = ""##transferring data from type str to list
        read_pos = n3wstring.index(".", the_other)
        extract_pos = 0 - int(n3wstring[read_pos+1:]) - len(n3wstring[read_pos+1:]) - 1   
        string_alg = n3wstring[extract_pos:- len(n3wstring[read_pos+1:]) - 1]   
        string_index = [] ##algorithm in type list
        for x in range(len(str(string_alg))):
            if string_alg[x].isdigit():
                appending_no += string_alg[x]
            else:
                string_index.append(appending_no)##once it reaches the comma it appends the number 
                appending_no = ""
        pos = 0
        for x in range(len(string_index)):
            ##find the proper letter
            pos = string_index.index(str(x))
            ##append the letter
            dafinal += n3wstring[pos]
        apple += dafinal
    fh = open("profile.txt", "w")
    fh.write(apple)
    fh.close()

    
def error_input():
    print("Please enter a valid input")


#THIS IS THE INTERFACE TO PROVIDE THE USER PASSCODE AS PROVIDED IN THE FIRST TIME USE (when the database is empty)
#THIS IS CALLED IN ORDER TO ACCESS THE DATABASE MENU --------------------------------------------------------------

def security():
    passcode = 0
    print("\n\n\n▬▬▬▬▬SECURITY▬▬▬▬▬")
    print("You are required to input your passcode")
    passcode = input("\nInput your passcode (enter '0' to return, '1' to reset) → ")
    decryption()
    fh = open("profile.txt", "r")
    store = fh.readlines()
    fh.close()
    encryption()
    if passcode == "0": #exit
        main(0)
    if passcode == "1":
        reset()
        decryption()
        fh = open("profile.txt", "r") #update new passcode variable
        store = fh.readlines()
        the = store[0][:-2] #stored passcode without \n
        fh.close()
        encryption()
        passcode = input("\nInput your passcode (enter '0' to return, '1' to reset) → ")
    the = store[0][:-2] #stored passcode without \n
    if passcode != the:
        print("\nYour passcode is incorrect")
    while passcode != the:
        time.sleep(0.5)
        passcode = input("You are required to input the correct passcode (enter '0' to return, '1' to reset) → ")
        if passcode != the:
            print("\nYour passcode is incorrect")
        if passcode == "0":
            main(0)
        if passcode == "1":
            reset()
            decryption()
            fh = open("profile.txt", "r") #update new passcode variable
            stinky = fh.readlines()
            the = stinky[0] #stored passcode
            the = the[:-2] #stored passcode without \n
            fh.close()
            encryption()
            
#initialization of passcode
def init():
    passcode = 0
    question = 0
    check = 0
    requirements = 0
    finalreq = 0
    print("▬▬▬▬▬INITIALIZATION▬▬▬▬▬")
    print("NOTE: Initialization is required for the first use, this will not be required until the data is reset")
    while finalreq == 0: #ensure string is according to requirements
        while requirements == 0:
            death = 0
            stop = 0 #prevents checking of other conditions if one is false
            passcode = input("\nEnter a passcode consisting of at least 8 characters, 1 uppercase letter, 1 lowercase letter and 1 special character → ")
            if len(passcode) < 8:
                requirements = 0
                stop = 1
                print("Your passcode is below 8 characters, please try again")
            if stop == 0:
                death = 0
                for x in range(len(passcode)):
                    if passcode[x].isupper() == True:
                        death += 1 #counts no of uppercase
                if death == 0:
                    print("Your passcode does not have an uppercase letter, please try again")
                    requirements = 0
                    stop = 1
            if stop == 0:
                death = 0
                for x in range(len(passcode)):
                    if passcode[x].islower() == True:
                        death += 1 #counts no of lowercase
                if death == 0:
                    print("Your passcode does not have a lowercase letter, please try again")
                    requirements = 0
                    stop = 1   
            if stop == 0:
                death = 0
                for x in range(len(passcode)):
                    if passcode[x].isalnum() == False:
                        death += 1 #counts no of special
                if death == 0:
                    print("Your passcode does not have a special character, please try again")
                    requirements = 0
                    stop = 1
            if stop == 0:
                requirements = 1
                
        question = input("\nPlease enter your security question to be printed in case you forget your passcode → ")
        answer = input("\nPlease enter your answer to the security question → ")
        print("\n\n\nConfirm your question is correct and the answer can be remembered? It cannot be resetted.")
        print("Question: {}".format(question))
        print("Answer: {}".format(answer))
        check = input("Enter \'Y\' or \'N\' → ")
        while (check[0] == "Y" or check[0] == "N" or check[0] == "y" or check[0] == "n") == False:
            check = input("Enter \'Y\' or \'N\' ONLY→ ")
        if check == "Y":
            print("\n\n\nYour passcode has been saved, it is required to access the database\nYou will also need to input the security answer to the security question you have initialized earlier in case you forget your passcode")
            time.sleep(3)
            finalreq = 1
        else:
            requirements = 0
                    
    fh = open("profile.txt" , 'w')
    fh.write(passcode + "a")
    fh.write('\n')
    fh.write(question)
    fh.write('\n')
    fh.write(answer)
    fh.close()
    encryption()


def main(initState):
    print("\n\n\n▬▬▬▬▬▬MAIN▬MENU▬▬▬▬▬▬\nWelcome to the school management system!\nHere you can access the database for student and teacher information,\nOr you may ask me a Python related question and I will answer right away!")
    init
    if initState == 1:
        time.sleep(3)
    print("\n\nPlease enter '1' to manage the database\nEnter '2' to use the Chat Bot for asking Python related questions\nEnter '0' to exit")
    #input
    user_selection = input("Enter a number from 0 to 2 here → ")
    while user_selection != "1" and user_selection != "2" and user_selection != "0" and user_selection != "encrypt" and user_selection != "decrypt":
        error_input()
        time.sleep(0.5)
        user_selection = input("\nEnter only 0 to 2 here → ")
    #accessing parts
    if user_selection == "1":
        print("You have accessed the database")
        global dAccess
        dAccess = 0
        database()
    elif user_selection == "2":
        print("You have accessed the chat bot")
        chatbot()
    elif user_selection == "decrypt": #sneaky sneaky
        print("file has been decrypted")
        time.sleep(0.5)
        decryption()
        main(0)
    elif user_selection == "encrypt": #SNEEEEEEAKY FUNCTION 
        print("file has been encrypted")
        time.sleep(0.5)
        encryption()
        main(0)
    else:
        print("See you next time")
        raise SystemExit


#RESETS USER PASSCODE THROUGH SECURITY QUESTIONS PROVIDED IN THE INITIALIZATION ----------------------------------------------------------------------

def reset():
    global stinky 
    leanswer = ""
    newasscode = ""
    ugh = 0
    requirements = 0
    ANOTHER = 0
    decryption()
    fh = open("profile.txt", "r")
    stinky = fh.readlines()
    fh.close()
    encryption()
    stinkystring = ""
    stinkystring = stinky[1]
    stinkystring = stinkystring[:-1]
    print("\nYou will now answer your security question to reset your passcode")
    print("Question → ", stinkystring)
    stinkystring = stinky[2]
    if stinkystring[-1] == "\n":
        stinkystring = stinkystring[:-1]
    while ugh == 0:
        leanswer = input("\nAnswer (enter 0 to exit) → ")
        if leanswer == stinkystring:
            while ugh == 0:
                requirements = 0
                while requirements == 0:
                    death = 0
                    stop = 0 #prevents checking of other conditions if one condition equates to  false
                    newasscode = input("\nEnter a passcode consisting of at least 8 characters, 1 uppercase letter, 1 lowercase letter and 1 special character → ")
                    if len(newasscode) < 8:
                        requirements = 0
                        stop = 1
                        print("Your passcode is below 8 characters, please try again")
                    if stop == 0:
                        death = 0
                        for x in range(len(newasscode)):
                            if newasscode[x].isupper() == True:
                                death += 1 #counts no of uppercase
                        if death == 0:
                            print("Your passcode does not have an uppercase letter, please try again")
                            requirements = 0
                            stop = 1
                    if stop == 0:
                        death = 0
                        for x in range(len(newasscode)):
                            if newasscode[x].islower() == True:
                                death += 1 #counts no of lowercase
                        if death == 0:
                            print("Your passcode does not have a lowercase letter, please try again")
                            requirements = 0
                            stop = 1   
                    if stop == 0:
                        death = 0
                        for x in range(len(newasscode)):
                            if newasscode[x].isalnum() == False:
                                death += 1 #counts no of special
                        if death == 0:
                            print("Your passcode does not have a special character, please try again")
                            requirements = 0
                            stop = 1
                    if stop == 0:
                        requirements = 1
                print("\n\n\nIs this your correct passcode? ", newasscode)
                check = input("Enter \'Y\' or \'N\' → ")
                while (check.upper()[0] == "Y" or check.upper()[0] == "N") == False:
                    check = input("Enter \'Y\' or \'N\' ONLY → ")
                if check == "Y":
                    stinky[0] = newasscode + "a" + "\n"
                    ugh = 1
        else:
            if leanswer == "0":
                main(0)
            print("Your answer is incorrect, do again")
    fh = open("profile.txt", "w")
    decryption()
    for x in range(len(stinky)):
        fh.write(stinky[x])
    fh.close()
    encryption()


    
#DATABASE INTERFACE
def database():
    global dAccess
    if dAccess == 0:
        security()
        dAccess = 1
    check_selection = 0
    user_selection = ""
    print("\n\n\n▬▬▬▬▬▬▬DATABASE▬▬▬▬▬▬▬")
    print("Enter '1' to create a record")
    print("Enter '2' to amend a record")
    print("Enter '3' to search for a record")
    print("Enter '4' to delete a record")
    print("Enter '0' to return to the main menu")
    requirements = 0
    menu_range = 4
    while requirements == 0:
        user_selection1 = input("Enter option → ")
        if user_selection1.isdigit() == False:
            requirements =  0
            error_input()
        elif (0 > int(user_selection1) or int(user_selection1) > menu_range) == True:
            requirements = 0
            error_input()
        else:
            requirements = 1
            
    if user_selection1 == "0":
        check_selection = 1
        main(0)
    elif user_selection1 == "1":
        check_selection = 1
        store()
    elif user_selection1 == "2":
        check_selection = 1
        amend()
    elif user_selection1 == "3":
        check_selection = 1
        search()
    elif user_selection1 == "4":
        delete()
        check_selection = 1

#CHATBOT (FAQ SECTION) IS MAINLY DONE BY ANOTHER COLLABORATING STUDENT --- I (RITCHIE YAPP) HAVE ONLY CORRECTED SOME ERRORS IN THIS SECTION, THEREFORE PLEASE IGNORE THIS IF YOU WISH

def chatbot():
    import time
    siri=0
    def error_input():
        time.sleep(1)
        print("Sorry! Chat Bot can't identify what u wish to ask.\n Please enter again!")
    def return_chatbot():
        time.sleep(1)
        print("\nReturning back to chatbot...\n")
        time.sleep(1)
        main_menu()
    def general_return():
        time.sleep(1)
        print("\nReturning to general FAQ\n")
        time.sleep(1)
        general_faq()
    
    def general_faq():
        uno = 0
        print("\nCoding school Chat Bot\n----------------------\n\n\nYou have picked General Python FAQs!\nHere are some examples of the questions you can ask about General Python:\n-what is idle?\n-what can we do with coding?\netc...")
        siri=input("\nWhat is your question? ")
        while all(x.isalpha() or x.isspace() for x in siri):
            uno += 1
            s=siri.split()
            for x in range(len(s)):
                s[x] = s[x].lower()
                print(s)
            if ('coding' or 'code' or 'codes') in s == True:
                print("answer: coding is the process of using codes to program the computer to execute what you want it to do, and you can make software,websites,mobile apps and more…")
                uno = 1
                general_return()
            elif 'work' in s or 'function' in s:
                print("answer: use programming language.")
                uno = 1
                general_return()
            elif 'idle' in s == True:
                print("answer: A software for building applications that combines common developer tools into a single graphical user interface, usually for learning purposes")
                uno = 1
                general_return()
            elif ('key' in s) or ('features' in s) or ('key' in s and 'features' in s):
                print("answer:1.writing python is way faster than other compiled languages.\n2.Python is also suitable for object orientated programming.\n3.Python always you to declare any types of variables whatever you like.\n4.Python iw an interpreted language that does not need to be compiled before it is run.")
                uno = 1
                general_return()
            elif ('language' in s) or ('programming' in s) or ('scripting' in s):
                print("answer:Python is capable of scripting, it is considered as a general-purpose programming language.")
                uno = 1
                general_return()
            elif 'back' in s or 'exit' in s or 'return' in s:
                return_chatbot()
            else:
                error_input()
                time.sleep(1)
                general_faq()
                if uno != 1:
                    for x in range(s):
                        if 'code' in s or 'mean' in s or 'codes' in s or 'meaning' in s:
                            print("1.answer: coding is the process of using codes to program the computer to execute what you want it to do.")                                    
                        elif 'work' in s or 'function' in s:
                            print("2.answer: use programming language.")
                        elif 'define' in s or 'idle' in s or 'mean' in s:
                            print("3.answer: Idle is Python’s Integrated Development and Learning Environment, providing editing,running and testing codes.")
                            general_return()
                        elif 'back' in s or 'exit' in s or 'return' in s:
                            return_chatbot()
                        else:
                            general_faq()
                    
        else:
            error_input()
            time.sleep(1)
            general_faq()

    def programming_return():
        uno = 0
        time.sleep(1)
        print("\nReturning back to programming FAQ\n")
        time.sleep(1)
        programming_faq()

    def programming_faq():
        uno = 0
        print("\nCoding school Chat Bot\n----------------------\nYou have picked Programming FAQs!")
        siri=input("What is your question? ")
        while all(x.isalpha() or x.isspace() for x in siri):
            uno += 1
            s=siri.split()
            for answer in s:
                if ('errors' in s) or ('wrong') in s:
                    print("1.answer: logical errors,syntax errors,semantic errors.")
                    uno = 1
                    programming_return()
                elif ('syntax' in s and 'errors' in s) or ('syntax' in s):
                    print("2.answer: syntax error is typos, incorrect indentation, or incorrect arguments.")
                    uno = 1
                    programming_return()
                elif ('capital' in s):
                    print("3.answer: python idle is case-sensitive thus all must be lowercase or all must be uppercase.")
                    uno = 1
                    programming_return()
                elif ('output' in s) or ('show' in s):
                    print("4.answer: use print() and type in brackets what u wish to output.")
                    uno = 1
                    programming_return()
                elif 'spacing' in s or 'spacings' in s or 'spaces' in s:
                    print("5.answer: use underscores instead")
                    uno = 1
                    programming_return()
                elif 'names' in s or 'value' in s:
                    print("6.answer: assign it as a variable or constant using ‘=’")
                    uno = 1
                    programming_return()
                elif 'different lines' in s or 'different' in s or 'separate' in s:
                    print("7.answer: use ‘/n’ into your print()")
                    uno = 1
                    programming_return()
                elif 'convert' in s or 'change' in s or 'different data type' in s:
                    print("8.answer: use type(int(“”))")
                    uno = 1
                    programming_return()
                elif 'range' in s:
                    print("9.answer: use range() and type the range of numbers you would like to use or use ‘for i in range(x):’ i is a variable and x is the range of numbers")
                    uno = 1
                    programming_return()
                elif 'input' in s or 'enter' in s:
                    print("10.answer: use input() and type what u wish to input into the brackets")
                    uno = 1
                    programming_return()
                elif 'length' in s or 'number of letters' in s:
                    print("11.answer: use len() and type in the brackets the word or number")
                    uno = 1
                    programming_return()
                elif 'make list' in s or 'make a list' in s:
                    print("12.answer: use list=[] and type in the brackets")
                    uno = 1
                    programming_return()
                elif 'equals' in s:
                    print("14.answer: use ‘==’ to show that two values that are equivalence True and False when they are not equivalence")
                    uno = 1
                    programming_return()
                elif ('not' in s and 'equal' in s) or ('not' in s and 'equals' in s) == True:
                    print("15.answer: use ‘!=’ to show that two values that are not equivalence True and False when they are equivalence")
                    uno = 1
                    programming_return()
                elif 'math' in s:
                    print("16.answer:before using the operators, type in ‘input math’ at line 1. ‘+’ to add, ‘-’ to subtract, ’’ to multiply, ‘/’ to divide, ‘//’ to get the value after dividing rounded down to nearest integer, ‘*’ to get the power of the value, ‘%’ to get the remainder of a divided value.")
                    uno = 1
                    programming_return()
                elif 'back' in s or 'exit' in s:
                    uno = 1
                    return_chatbot()
            else:
                error_input()
                time.sleep(1)
                programming_faq()
                if uno != 1:
                    for x in range(s):
                        if 'error' in s or 'wrong' in s or 'incorrect' in s:
                            print("1.answer: logical errors,syntax errors,semantic errors.")
                            programming_return()
                        elif 'syntax' in s:
                            print("2.answer: syntax error is typos, incorrect indentation, or incorrect arguments.")
                            programming_return()
                        elif 'capital' in s or 'caps' in s:
                            print("3.answer: python idle is case-sensitive thus all must be lowercase or all must be uppercase.")
                            programming_return()
                        elif 'output' in s:
                            print("4.answer: use print() and type in brackets what u wish to output.")
                            programming_return()
                        elif 'spacing' in s or 'spacings' in s or 'spaces' in s or 'space' in s:
                            print("5.answer: use underscores instead")
                            programming_return()
                        elif 'name' in s or 'value' in s:
                            print("6.answer: assign it as a variable or constant using ‘=’")
                            programming_return()
                        elif 'differ' in s or 'separate' in s:
                            print("7.answer: use ‘/n’ into your print()")
                            programming_return()
                        elif 'convert' in s or 'change' in s or 'differ' in s:
                            print("8.answer: use type(int(“”))")
                            programming_return()
                        elif 'range' in s:
                            print("9.answer: use range() and type the range of numbers you would like to use or use ‘for i in range(x):’ i is a variable and x is the range of numbers")
                            programming_return()
                        elif 'input' in s or 'enter' in s:
                            print("10.answer: use input() and type what u wish to input into the brackets")
                            programming_return()
                        elif 'length' in s or 'number' in s or 'amount' in s:
                            print("11.answer: use len() and type in the brackets the word or number")
                            programming_return()
                        elif 'make' in s or 'list' in s:
                            print("12.answer: use list=[] and type in the brackets")
                            programming_return()
                        elif 'equal' in s or 'equals' in s:
                            print("14.answer: use ‘==’ to show that two values that are equivalence True and False when they are not equivalence")
                            programming_return()
                        elif 'not equal' in s or 'not equals' in s:
                            print("15.answer: use ‘!=’ to show that two values that are not equivalence True and False when they are equivalence")
                            programming_return()
                        elif 'math' in s:
                            print("16.answer:before using the operators, type in ‘input math’ at line 1. ‘+’ to add, ‘-’ to subtract, ’’ to multiply, ‘/’ to divide, ‘//’ to get the value after dividing rounded down to nearest integer, ‘*’ to get the power of the value, ‘%’ to get the remainder of a divided value.")
                            programming_return()
                        elif 'back' in s or 'exit' in s or 'return' in s:
                            return_chatbot()
                        else:
                            general_faq()
                        
        else:
            error_input()
            time.sleep(1)
            programming_faq()

        
    def dnh_return():
        time.sleep(1)
        print("\nReturning back to design and history FAQ\n")
        time.sleep(1)
        dnh_faq()  

    def dnh_faq():
        uno = 0
        print("Coding school Chat Bot\n------------------------------\nYou have picked Design & History FAQs!")
        siri=input("What is your question?")
        while all(x.isalpha() or x.isspace() for x in siri):
            uno += 1
            s=siri.split()
            for answer in s:
                if 'loops' in s:
                    print("1.answer: ‘for_in:’ loop and ‘while__:’ loop")
                    uno = 1
                    dnh_return()
                elif 'decisions' in s or 'asks' in s:
                    print("2.answer: use if-elif-else to make decisions")
                    uno = 1
                    dnh_return()
                elif 'comma' in s or 'commas' in s:
                    print("Python allows you to add commas at the end of list and tuples,\n[1, 2, 3,]\n('a', 'b', 'c',)\nd = {\n    'A': [1, 5],\n    'B': [6, 7],\n}")
                    uno = 1
                    dnh_return()
                elif 'back' in s or 'exit' in s or 'return' in s:
                    return_chatbot()
            else:
                error_input()
                time.sleep(1)
                dnh_faq()
                if uno != 1:
                    for x in range(s):
                        if 'loops' in s or 'loop' in s:
                            print("1.answer: ‘for_in:’ loop and ‘while__:’ loop")
                            dnh_return()
                        elif 'decisions' in s or 'asks' in s or 'decision' in s or 'ask' in s:
                            print("2.answer: use if-elif-else to make decisions")
                            dnh_return()
                        elif 'exit' in s or 'back' in s or 'return' in s:
                            return_chatbot()
                        else:
                            dnh_faq()
                    
        else:
            error_input()
            time.sleep(1)
            dnh_faq()
                       
    def main_menu():
        menu_selection = 0
        print("Coding school Chat Bot\n----------------------\nHello this is Chat Bot, here to answer all the doubts and questions you have on coding!\n\n1. General Python FAQ\n2. Programming FAQ\n3. Design & History FAQ\n4. Exit\n")
        menu_selection = input("Enter option:")
        menu_range = 4
        if menu_selection.isalpha()==True:
            menu_selection=0
            error_input
        while 1 > int(menu_selection) or int(menu_selection) > menu_range:
            error_input()
            menu_selection = input("Enter option:")
            #check
            if menu_selection.isdigit() == False:
                menu_selection = 0
            if (1 > int(menu_selection) or int(menu_selection) > menu_range) == True:
                error_input()
        #process
        if int(menu_selection) == 1:
            time.sleep(1)
            general_faq()
        elif int(menu_selection) == 2:
            time.sleep(1)
            programming_faq()
        elif int(menu_selection) == 3:
            time.sleep(1)
            dnh_faq()
        elif int(menu_selection) == 4:
            time.sleep(1)
            print("Hope I have answered all your questions!\nexiting program...")
            main(0)
       
    main_menu()

#STORE--------------------------------------------------------------------------------------------------
def store():
    decryption()
    fh= open("profile.txt" , 'a')
    print("\n\n\n▬▬▬▬▬CREATE▬DATA▬▬▬▬▬")
    print("Please enter the necessary data below")
    print(".")
    time.sleep(1)
    global level

    #get level (glvl)
    def glvl():
        while True:
            try:
                level = int(input("What is your level: Secondary "))
                break
            except ValueError:
               print ("That is not a number do again")
            
        while (level<1) or (level>5):
            print("Your level is not valid, please try again")
            while True:
                try:
                    level = int(input("What is your level: Secondary "))
                    break
                except ValueError:
                   print ("That is not a number do again")

        return level


    #get class (gclss):
    def gclss():
        level = str(glvl())
        print("1.Charity\n2.Integrity\n3.Humility\n4.Respect\n5.Love\n6.Faith\n7.Hope")
        while True:
            try:
                jar = int(input("Please enter the number of your corresponding class: "))
                break
            except ValueError:
               print ("That is not a number do again")

        while (jar<1) or (jar>7):
            print("That input is not valid, please try again")
            while True:
                try:
                    jar = int(input("Please enter the number of your corresponding class: ")) 
                    break
                except ValueError:
                   print ("That is not a number do again")
           
        level = str(level)
        if jar == 1:
            Class = str(level+"cha")
        elif jar == 2:
            Class = str(level+ "int")
        elif jar == 3:
            Class = str(level+"hum")
        elif jar == 4:
            Class = str(level+"res")
        elif jar == 5:
            Class = str(level+"lov")
        elif jar == 6:
            Class = str(level+"fai")
        else:
            Class = str(level+"hop")

        return Class


    #get index number (gindx)
    def gindx():
        while True:
            try:
                number = int(input("Enter your index number: "))
                break
            except ValueError:
               print ("That is not a number do again")
        indexno = ("%02d" % number)
        indexno = str(indexno)

        while (number<1) or (len(indexno)!=2):
            print("Index number has to be 1-2 digits long")
            while True:
                try:
                    number = int(input("Enter your index number: "))
                    break
                except ValueError:
                   print ("That is not a number do again")
            indexno = ("%02d" % number)
            indexno = str(indexno)
            
        return indexno

    #user's date of birth(dtfbrth)
    def dtfbrth():
        print("Date of Birth")
        while True:
            try:
                year = int(input("Year(YYYY): "))
                break
            except ValueError:
                print ("That is not a number do again")
        while year<2002 or year>2010:
            print("That is not a valid year try again")
            while True:
                try:
                    year = int(input("Year(YYYY): "))
                    break
                except ValueError:
                    print ("That is not a number do again")

                    
        while True:
            try:
                month = int(input("Month(MM): "))
                break
            except ValueError:
                print("try again, please enter the number of the month")
        while (month<1) or (month>12):
            print("that is not a valid month")
            while True:
                try:
                    month = int(input("Month(MM): "))
                    break
                except ValueError:
                    print("please enter the number of the month")

        date = 0
        if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
            while (date<1) or (date>31):
                while True:
                    try:
                        date =  int(input("Day(DD): "))
                        break
                    except ValueError:
                        print("Please enter a number")
                if (date<1) or (date>30):
                    print("that's not a valid day in relation to your month")
                            
        elif month == 4 or 6 or 9 or 11:
            while (date<1) or (date>30):
                while True:
                    try:
                        date =  int(input("Day(DD): "))
                        break
                    except ValueError:
                        print("Please enter a number")
                if (date<1) or (date>30):
                    print("that's not a valid day in relation to your month")
                    
        mumbai = year % 4
        if month == 2:
            if mumbai == 0:
                while (date<1) or (date>29):
                    print("that's not a valid day in relation to your month")
                    while True:
                        try:
                            date =  int(input("Day(DD): "))
                            break
                        except ValueError:
                            print("Please enter a number")
                    if (date<1) or (date>29):
                        print("that's not a valid day in relation to your month")

            else:
                while (date<1) or (date>28):
                    print("that's not a valid day in relation to your year and month")
                    while True:
                        try:
                            date =  int(input("Day(DD): "))
                            break
                        except ValueError:
                            print("Please enter a number")
            
                    
                    
        month = str("%02d" % month)
        date = str(date)
        year = str(year)
        donk = str(date+"/"+month+"/"+year)
        return (donk)

        


    #save data (savdat)
    def savdat():
        fullname= input("full name(Birth certificate): ")
        while fullname == "":
            print("this is a compulsory question")
            fullname= input("full name(Birth certificate): ")
        with open('profile.txt') as f:
            normal = f.readlines()
        check = normal[3::12]
        checkmate = str(fullname+"\n") in check
        while checkmate == True:
            print("that is not a valid name, try again")
            fullname= input("full name(Birth certificate): ")
            while fullname == "":
                print("this is a compulsory question")
                fullname= input("full name(Birth certificate): ")
            check = normal[3::12]
            checkmate = str(fullname+"\n") in check

        dob = dtfbrth()

        gender = input("gender: ")
        while gender == "":
            print("this is a compulsory question")
            gender = input("gender: ")
        with open('profile.txt') as f:
            normal = f.readlines()
        check = normal[3::12]
        checkmate = str(gender +"\n") in check
        while checkmate == True:
            print("that is not a valid gender (YES SHUT UP NOT VALID), try again")
            gender = input("gender: ")
            while gender == "":
                print("this is a compulsory question")
                gender = input("gender: ")
            check = normal[3::12]
            checkmate = str(gender +"\n") in check

        nation = input("nationality: ")
        while nation == "":
            print("this is a compulsory question")
            nation = input("nationality: ")
        with open('profile.txt') as f:
            normal = f.readlines()
        check = normal[3::12]
        checkmate = str(nation +"\n") in check
        while checkmate == True:
            print("that is not a valid nationality, try again")
            nation = input("nationality: ")
            while nation == "":
                print("this is a compulsory question")
                nation = input("nationality: ")
            check = normal[3::12]
            checkmate = str(nation +"\n") in check
                
        address = input("address: ")
        while address == "":
            print("this is a compulsory question")
            address = input("address: ")
        with open('profile.txt') as f:
            normal = f.readlines()
        check = normal[3::12]
        checkmate = str(address +"\n") in check
        while checkmate == True:
            print("that is not a valid ADDRESS, try again")
            address = input("address: ")
            while address == "":
                print("this is a compulsory question")
                address = input("address: ")
            check = normal[3::12]
            checkmate = str(address +"\n") in check
                
        medcon = input("any medical conditions: ")
        while medcon =="":
            print("this is a compulsory question")
            medcon = input("any medical conditions: ")
        with open('profile.txt') as f:
            normal = f.readlines()
        check = normal[3::12]
        checkmate = str(medcon +"\n") in check
        while checkmate == True:
            print("that is not a valid input, try again")
            medcon = input("any medical conditions: ")
            while medcon =="":
                print("this is a compulsory question")
                medcon = input("any medical conditions: ")
            check = normal[3::12]
            checkmate = str(medcon +"\n") in check   

        while True:
            try:
                stdntno = int(input("student phone number: "))
                break
            except ValueError:
                print ("THAT IS NOT A NUMBER DO AGAIN")
        studenthp = str(stdntno)
        while (len(studenthp) < 8) or (stdntno<1):
            print ("that is not a valid phone number")
            while True:
                try:
                    stdntno = int(input("student phone number: "))
                    break
                except ValueError:
                    print ("THAT IS NOT A NUMBER DO AGAIN")
            studenthp = str(stdntno) 

        parentname = input("Parent/Guardian's name: ")
        while parentname == "":
             print("this is a compulsory question")
             parentname = input("Parent/Guardian's name: ")
        with open('profile.txt') as f:
            normal = f.readlines()
        check = normal[3::12]
        checkmate = str(parentname +"\n") in check
        while checkmate == True:
            print("that is not a valid input, try again")
            parentname = input("Parent/Guardian's name: ")
            while parentname == "":
                 print("this is a compulsory question")
                 parentname = input("Parent/Guardian's name: ")
            check = normal[3::12]
            checkmate = str(parentname +"\n") in check
            
        while True:
            try:
                prnthpno = int(input("parent/guardian's phone number: "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")
        parenthp = str(prnthpno)
        while (len(parenthp) < 8) or (prnthpno < 1):
            print ("that is not a valid phone number")            
            while True:
                try:
                    prnthpno = int(input("parent/guardian's phone number: "))
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")
            parenthp = str(prnthpno)

        fh= open('profile.txt','a')
        fh.write('\n')
        fh.write(fullname)
        fh.write('\n')
        fh.write(dob)
        fh.write('\n')
        fh.write(gender)
        fh.write('\n')
        fh.write(nation)
        fh.write('\n')
        fh.write(address)
        fh.write('\n')
        fh.write(medcon)
        fh.write('\n')
        fh.write(studenthp)
        fh.write('\n')
        fh.write(parentname)
        fh.write('\n')
        fh.write(parenthp)
        fh.close()
        time.sleep(1)
        print("your data has been saved")

        
    #check if tag is in file(citiif)
    def citiif(string_to_search):
        ritchiepenis = open('profile.txt', 'r').readlines()
        if string_to_search in ritchiepenis[3::12]:
            return True
        return False

    def fpotif(file_name, string_to_search):
        dorrito = open(file_name, 'r').readlines()
        chewchewchew = dorrito.index(string_to_search)
        return chewchewchew


    user_class = gclss()
    user_indexno = gindx()    
    search_tag= str(user_class+user_indexno+"\n")
    broccoli = 0
        
    while citiif(search_tag)==True:
        print("sorry but index number", user_indexno, "from class", user_class, "has already registered")
        ginger = input("would you like to try again or exit? press any button to try again or 1 to exit ")
        if ginger == "1":
            print("goodbye")
            broccoli = 1
        else:
            print(".\nenter another class and/or index number")
            user_class = gclss()
            user_indexno = gindx()
            search_tag= str(user_class+user_indexno+"\n")


    if citiif("deleted line"+"\n") == True:
        fleas = fpotif('profile.txt',("deleted line"+"\n"))
        koon = open('profile.txt', 'r').read().splitlines()
        search_tag = search_tag.rstrip()
        koon[fleas] = search_tag
        koon[fleas+1] = user_class
        koon[fleas+2] = user_indexno
        open('profile.txt','w').write("\n".join(koon))

        fullname= input("full name(Birth certificate): ")
        while fullname == "":
            print("this is a compulsory question")
            fullname= input("full name(Birth certificate): ")
        with open('profile.txt') as f:
            normal = f.readlines()
        check = normal[3::12]
        checkmate = str(fullname+"\n") in check
        while (checkmate == True):
            print("that is not a valid name, try again")
            fullname= input("full name(Birth certificate): ")
            while fullname == "":
                print("this is a compulsory question")
                fullname= input("full name(Birth certificate): ")
            check = normal[3::12]
            checkmate = str(fullname+"\n") in check
        koon[fleas+3] = str(fullname)
        open('profile.txt','w').write("\n".join(koon))

        dob = dtfbrth()
        koon[fleas+4] = str(dob)
        open('profile.txt','w').write("\n".join(koon))

        gender = input("gender: ")
        while gender == "":
            print("this is a compulsory question")
            gender = input("gender: ")
        with open('profile.txt') as f:
            normal = f.readlines()
        check = normal[3::12]
        checkmate = str(gender +"\n") in check
        while (checkmate == True):
            print("that is not a valid gender (YES SHUT UP NOT VALID), try again")
            gender = input("gender: ")
            while gender == "":
                print("this is a compulsory question")
                gender = input("gender: ")
            check = normal[3::12]
            checkmate = str(gender +"\n") in check
        koon[fleas+5] = str(gender)
        open('profile.txt','w').write("\n".join(koon))

        nation = input("nationality: ")
        while nation == "":
            print("this is a compulsory question")
            nation = input("nationality: ")
        with open('profile.txt') as f:
            normal = f.readlines()
        check = normal[3::12]
        checkmate = str(nation +"\n") in check
        while (checkmate == True):
            print("that is not a valid nationality, try again")
            nation = input("nationality: ")
            while nation == "":
                print("this is a compulsory question")
                nation = input("nationality: ")
            check = normal[3::12]
            checkmate = str(nation +"\n") in check    
        koon[fleas+6] = str(nation)
        open('profile.txt','w').write("\n".join(koon))

        address = input("address: ")
        while address == "":
            print("this is a compulsory question")
            address = input("address: ")
        with open('profile.txt') as f:
            normal = f.readlines()
        check = normal[3::12]
        checkmate = str(address +"\n") in check
        while (checkmate == True):
            print("that is not a valid ADDRESS, try again")
            address = input("address: ")
            while address == "":
                print("this is a compulsory question")
                address = input("address: ")
            check = normal[3::12]
            checkmate = str(address +"\n") in check
        koon[fleas+7] = str(address)
        open('profile.txt','w').write("\n".join(koon))
        
        medcon = input("any medical conditions: ")
        while medcon =="":
            print("this is a compulsory question")
            medcon = input("any medical conditions: ")
        with open('profile.txt') as f:
            normal = f.readlines()
        check = normal[3::12]
        checkmate = str(medcon +"\n") in check
        while (checkmate == True):
            print("that is not a valid input, try again")
            medcon = input("any medical conditions: ")
            while medcon =="":
                print("this is a compulsory question")
                medcon = input("any medical conditions: ")
            check = normal[3::12]
            checkmate = str(medcon +"\n") in check   
        koon[fleas+8] = str(medcon)
        open('profile.txt','w').write("\n".join(koon))

        while True:
            try:
                stdntno = int(input("student phone number: "))
                break
            except ValueError:
                print ("THAT IS NOT A NUMBER DO AGAIN")
        studenthp = str(stdntno)
        while (len(studenthp) < 8) or (stdntno<1):
            print ("that is not a valid phone number")
            while True:
                try:
                    stdntno = int(input("student phone number: "))
                    break
                except ValueError:
                    print ("THAT IS NOT A NUMBER DO AGAIN")
            studenthp = str(stdntno)
        koon[fleas+9] = str(studenthp)
        open('profile.txt','w').write("\n".join(koon))


        parentname = input("Parent/Guardian's name: ")
        while parentname == "":
             print("this is a compulsory question")
             parentname = input("Parent/Guardian's name: ")
        with open('profile.txt') as f:
            normal = f.readlines()
        check = normal[3::12]
        checkmate = str(parentname +"\n") in check
        while (checkmate == True):
            print("that is not a valid input, try again")
            parentname = input("Parent/Guardian's name: ")
            while parentname == "":
                 print("this is a compulsory question")
                 parentname = input("Parent/Guardian's name: ")
            check = normal[3::12]
            checkmate = str(parentname +"\n") in check
        koon[fleas+10] = str(parentname)
        open('profile.txt','w').write("\n".join(koon))


        while True:
            try:
                prnthpno = int(input("parent/guardian's phone number: "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")
        parenthp = str(prnthpno)
        while (len(parenthp) < 8) or (prnthpno<1):
            print ("that is not a valid phone number")            
            while True:
                try:
                    prnthpno = int(input("parent/guardian's phone number: "))
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")
            parenthp = str(parentno) 
        koon[fleas+11] = str(parenthp)
        open('profile.txt','w').write("\n".join(koon))
        
        broccoli = 9




    if broccoli == 0:
        fh = open("profile.txt", "a")
        search_tag = search_tag.rstrip()
        fh.write('\n')
        fh.write(search_tag)
        fh.write('\n')
        fh.write(user_class)
        fh.write('\n')
        fh.write(user_indexno)
        fh.close()
        savdat()

    #exit to main menu
    encryption()
    database()        

def search():
    print("\n\n\n▬▬▬▬▬SEARCH▬DATA▬▬▬▬▬")
    decryption()
    #check if tag is in file (citiif)
    def citiif(string_to_search):
        delahoya = open('profile.txt').readlines() 
        if string_to_search in delahoya[3::12]: #search for tag every 12th line in the file
            return True
        return False

    #find position of tag in file (fpotif)
    def fpotif(file_name, string_to_search):
        line_number = 0
        with open(file_name, 'r') as rob:
            for line in rob:
            # For each line, check if line contains the string
                line_number += 1
                if string_to_search in line:
                        # When line of tag is found 
                        return line_number
        return line_number
                

    global level

    #get level (glvl)
    def glvl():
        while True:
            try:
                level = int(input("What is your level: Secondary "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")
            
        while (level<1) or (level>5):
            print("your level is not valid, please try again")
            while True:
                try:
                    level = int(input("What is your level: Secondary "))
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")

        return level


    #get class (gclss):
    def gclss():
        level = str(glvl())
        print("1.Charity\n2.Integrity\n3.Humility\n4.Respect\n5.Love\n6.Faith\n7.Hope")
        while True:
            try:
                jar = int(input("Please enter the number of your corresponding class: "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")

        while (jar<1) or (jar>7):
            print("that input is not valid, please try again")
            while True:
                try:
                    jar = int(input("Please enter the number of your corresponding class: ")) 
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")
           
        level = str(level)
        if jar == 1:
            Class = str(level+"cha")
        elif jar == 2:
            Class = str(level+ "int")
        elif jar == 3:
            Class = str(level+"hum")
        elif jar == 4:
            Class = str(level+"res")
        elif jar == 5:
            Class = str(level+"lov")
        elif jar == 6:
            Class = str(level+"fai")
        else:
            Class = str(level+"hop")

        return Class


    #get index number (gindx)
    def gindx():
        while True:
            try:
                number = int(input("enter your index number: "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")
        indexno = ("%02d" % number)
        indexno = str(indexno)

        while (number<1) or (len(indexno)!=2):
            print("index number has to be 2 digits long")
            while True:
                try:
                    number = int(input("enter your index number: "))
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")
            indexno = ("%02d" % number)
            indexno = str(indexno)
            
        return indexno

    chad = 3
    Class = gclss()
    indexno = gindx()
    search_tag= str(Class+indexno+"\n")

    if citiif(search_tag) == True:
        chad = 1   
      

    if citiif(search_tag) == False:
        print("Sorry but we don't have your data")
        ginger = input("enter any button to try again or 1 to exit ")
        if ginger == "1":
            print("goodbye") 
            #exit to menu
        else:
            time.sleep(1)
            while citiif(search_tag) == False:            
                Class = gclss()
                indexno = gindx()
                search_tag= str(Class+indexno+"\n")
                if citiif(search_tag) == True:
                    chad = 1
                    break
                else:
                    print("Sorry, we still can't identify you, do you want to exit?")
                    squidward = input("Enter 1 to exit or any other button to try again: ")
                    if squidward == "1":
                        chad = 2
                        break

    if chad == 1:            
        print("please hold while we retrieve your information")
        time.sleep(1)
        print(".")
        user_tag = fpotif('profile.txt', search_tag)
        fiver = open('profile.txt')
        linus = fiver.readlines()
        time.sleep(1)
        print("Hello", linus[user_tag+2],
              "\nThis is your data:",
              "\n\nClass:" , linus[user_tag],
              "\nIndex number:", linus[user_tag+1],
              "\nFull name:" , linus[user_tag+2],
              "\nDate of birth (DD/MM/YYYY):" , linus[user_tag+3],
              "\ngender:" , linus[user_tag+4],
              "\nnationality:", linus[user_tag+5],
              "\naddress:", linus[user_tag+6],
              "\nmedical conditions:", linus[user_tag+7],
              "\nstudent's handphone number:", linus[user_tag+8],
              "\nparent/guardian's name:", linus[user_tag+9],
              "\nparent/guardian's handphone number:", linus[user_tag+10])
        time.sleep(1)

    encryption()
    database()

def amend():
    print("\n\n\n▬▬▬▬▬AMEND▬DATA▬▬▬▬▬")
    decryption()
    #search:
    #check if tag is in file (citiif)
    def citiif(string_to_search):
        delahoya = open('profile.txt').readlines() #makes a list of every line (tag)
        if string_to_search in delahoya[3::12]: #search for tag in list - every 12 lines
            return True
        return False

    #find position of tag in file (fpotif)
    def fpotif(file_name, string_to_search):
        line_number = 0
        with open(file_name, 'r') as rob:
            for line in rob:
            # For each line, check if line contains the string
                line_number += 1
                if string_to_search in line:
                        # When line of tag is found 
                        return line_number
        return line_number
                
    global level

    #get level (glvl)
    def glvl():
        while True:
            try:
                level = int(input("What is your level: Secondary "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")
            
        while (level<1) or (level>5):
            print("your level is not valid, please try again")
            while True:
                try:
                    level = int(input("What is your level: Secondary "))
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")

        return level

    #get class (gclss):
    def gclss():
        level = str(glvl())
        print("1.Charity\n2.Integrity\n3.Humility\n4.Respect\n5.Love\n6.Faith\n7.Hope")
        while True:
            try:
                jar = int(input("Please enter the number of your corresponding class: "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")

        while (jar<1) or (jar>7):
            print("that input is not valid, please try again")
            while True:
                try:
                    jar = int(input("Please enter the number of your corresponding class: ")) 
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")
           
        level = str(level)
        if jar == 1:
            Class = str(level+"cha")
        elif jar == 2:
            Class = str(level+ "int")
        elif jar == 3:
            Class = str(level+"hum")
        elif jar == 4:
            Class = str(level+"res")
        elif jar == 5:
            Class = str(level+"lov")
        elif jar == 6:
            Class = str(level+"fai")
        else:
            Class = str(level+"hop")

        return Class


    #get index number (gindx)
    def gindx():
        while True:
            try:
                number = int(input("enter your index number: "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")
        indexno = ("%02d" % number)
        indexno = str(indexno)

        while (number<1) or (len(indexno)!=2):
            print("index number has to be 2 digits long")
            while True:
                try:
                    number = int(input("enter your index number: "))
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")
            indexno = ("%02d" % number)
            indexno = str(indexno)
            
        return indexno

    global level

    #get new level (gtnwlvl)
    def gtnwlvl():
        while True:
            try:
                level2 = int(input("What is your new level: Secondary "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")
            
        while (level2<1) or (level2>5):
            print("your level is not valid, please try again")
            while True:
                try:
                    level2 = int(input("What is your new level: Secondary "))
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")

        return level2

    global Class
    #get new class (gtnwclss):
    def gtnwclss():
        level = str(gtnwlvl())
        print("1.Charity\n2.Integrity\n3.Humility\n4.Respect\n5.Love\n6.Faith\n7.Hope")
        while True:
            try:
                jar = int(input("Please enter the corresponding number of your desired class: "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")

        while (jar<1) or (jar>7):
            print("that input is not valid, please try again")
            while True:
                try:
                    jar = int(input("Please enter the corresponding number of your desired class: "))
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")
               
        level = str(level)
        if jar == 1:
            Class = str(level+"cha")
        elif jar == 2:
            Class = str(level+ "int")
        elif jar == 3:
            Class = str(level+"hum")
        elif jar == 4:
            Class = str(level+"res")
        elif jar == 5:
            Class = str(level+"lov")
        elif jar == 6:
            Class = str(level+"fai")
        else:
            Class = str(level+"hop")

        return Class


    #get new index number (gindx)
    def gtnwindx():
        while True:
            try:
                number2 = int(input("enter your new index number: "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")
        indexno2 = ("%02d" % number2)
        indexno2 = str(indexno2)

        while (number2<1) or (len(indexno2)!=2):
            print("index number has to be 2 digits long")
            while True:
                try:
                    number2 = int(input("enter your new index number: "))
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")
            indexno2 = ("%02d" % number2)
            indexno2 = str(indexno2)
            
        return indexno2

    def new_tag():
        wanted_class = gtnwclss()
        wanted_indexno = gtnwindx()
        wanted_tag = str(wanted_class + wanted_indexno+"\n")
        koon = open('profile.txt').read().splitlines()
        if citiif(wanted_tag) == True:
            print("index number", wanted_indexno, "from class", wanted_class, "is currently taken.")
            olajide = input("enter 1 to try another class and index number, 2 to swap classes with the current occupant or any other button to exit: ")
            if olajide == "1":
                ritchie = "1"
                while ritchie == "1":
                    wanted_class = gtnwclss()
                    wanted_indexno = gtnwindx()
                    wanted_tag = (wanted_class + wanted_indexno+"\n")
                    if citiif(wanted_tag) == True:
                        ritchie = input("That class and/or index number is still taken. Enter 1 to try again or enter any other button to exit: ")
                        
            elif olajide == "2":
                 print("are you sure you have the current user's permission to swap tags?")
                 #ritchie you might want to add a security function here
                 coxlong = input("enter 1 to exit or any other button to continue: ")
                 coxlong = input("ARE YOU SURE U HAVE THEIR PERMSISSION? enter 1 to exit or any other button to continue: ")
                 if coxlong == "1":
                     print("understandable have a nice day")
                 else:
                     shaq = fpotif('profile.txt', wanted_tag)
                     user_tag = fpotif('profile.txt', search_tag)
                     fatneek = search_tag.rstrip()
                     akneehow = wanted_tag.rstrip()
                     koon[user_tag-1] = akneehow
                     koon[user_tag] = wanted_class
                     koon[user_tag+1] = wanted_indexno
                     koon[shaq-1] = fatneek
                     koon[shaq] = Class
                     koon[shaq+1] = indexno
                     open('profile.txt','w').write('\n'.join(koon))
                     print("your class and index numbers have been swapped. goodbye")

            else:
                print("goodbye")
                                      
        if citiif(wanted_tag) == False:
            user_tag = fpotif('profile.txt', search_tag)
            akneehow = wanted_tag.rstrip()
            koon[user_tag-1] = akneehow
            koon[user_tag] = wanted_class
            koon[user_tag+1] = wanted_indexno
            open('profile.txt','w').write('\n'.join(koon))
            print("your class and index numbers have been updated. goodbye")


    #user's date of birth(dtfbrth)
    def dtfbrth():
        print("Date of Birth")
        time.sleep(1)
        while True:
            try:
                year = int(input("Year(YYYY): "))
                break
            except ValueError:
                print("Enter a number please")
        while year<2002 or year>2010:
            print("that is not a valid year try again")
            while True:
                try:
                    year = int(input("Year(YYYY): "))
                    break
                except ValueError:
                    print("Enter a number please")

        while True:
            try:
                month = int(input("Month(MM): "))
                break
            except ValueError:
                print("try again, please enter the number of the month")
        while (month<1) or (month>12):
            print("that is not a valid month")
            while True:
                try:
                    month = int(input("Month(MM): "))
                    break
                except ValueError:
                    print("please enter the number of the month")

        date = 0
        if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
            while (date<1) or (date>31):
                while True:
                    try:
                        date =  int(input("Day(DD): "))
                        break
                    except ValueError:
                        print("Please enter a number")
                if (date<1) or (date>30):
                    print("that's not a valid day in relation to your month")
                else:
                    break
                            
        elif month == 4 or 6 or 9 or 11:
            while (date<1) or (date>30):
                while True:
                    try:
                        date =  int(input("Day(DD): "))
                        break
                    except ValueError:
                        print("Please enter a number")
                if (date<1) or (date>30):
                    print("that's not a valid day in relation to your month")
                else:
                    break
                    
        else:
            if year%4 == 0:
                while (date<1) or (date>29):
                    while True:
                        try:
                            date =  int(input("Day(DD): "))
                            break
                        except ValueError:
                            print("Please enter a number")
                    if (date<1) or (date>29):
                        print("that's not a valid day in relation to your month")
                    else:
                        break
                    
                
            else:
                while (date<1) or (date>28):
                    while True:
                        try:
                            date =  int(input("Day(DD): "))
                            break
                        except ValueError:
                            print("Please enter a number")
                    if (date<1) or (date>28):
                        print("that's not a valid day in relation to your month")
                    else:
                        break
                                            
        month = str("%02d" % month)
        date = str(date)
        year = str(year)
        donk = str(date+"/"+month+"/"+year)
        return donk


    Class = gclss()
    indexno = gindx()
    search_tag= str(Class+indexno+"\n")
    user_tag = fpotif('profile.txt', search_tag)
    koon = open('profile.txt').read().splitlines()

    while citiif(search_tag) == False:
        print("we can't seem to identify you, would you like to try again?")
        iridocyclitis = input("enter any button to try again or 1 to exit: ")
        if iridocyclitis == "1":
            break  #exit to main menu
        else:
            Class = gclss()
            indexno = gindx()
            search_tag= str(Class+indexno+"\n")

    chlamydia = "1"
    if citiif(search_tag) == True:
        while chlamydia == "1":
            print(".")
            print("1. Class and index number\n2. Name\n3. Date of birth\n4. Gender\n5. Nationality\n6. Address\n7. Medical conditions"
                  "\n8. Student personal mobile phone number\n9. Parent/Guardian name\n10. Parent/Guardian phone number\n11. Exit")
            while True:
                try:
                    hiv = int(input("Enter the corresponding number of the peice of your data you would like to ammend: "))
                    break
                except ValueError:
                    print("that is not a valid number")
            while (hiv > 11) or (hiv < 1):
                print("that isn't a valid number please try again")
                while True:
                    try:
                        hiv = int(input("Enter the number of the peice of your data you would like to amend: "))
                        break
                    except ValueError:
                        print("that is not a valid number")

            print(".")
            time.sleep(1)
            if hiv == 1:
                new_tag()

            elif hiv == 2:
                fullname= input("full name(Birth certificate): ")
                while fullname == "":
                    print("this is a compulsory question")
                    fullname= input("full name(Birth certificate): ")
                with open('profile.txt') as f:
                    normal = f.readlines()
                check = normal[3::12]
                checkmate = str(fullname+"\n") in check
                while checkmate == True:
                    print("that is not a valid name, try again")
                    fullname= input("full name(Birth certificate): ")
                    while fullname == "":
                        print("this is a compulsory question")
                        fullname= input("full name(Birth certificate): ")
                    check = normal[3::12]
                    checkmate = str(fullname+"\n") in check
                koon[user_tag+2] = fullname
                open('profile.txt','w').write('\n'.join(koon))
                print("your data has been updated")

              
            elif hiv == 3:
                dob = dtfbrth()
                koon[user_tag+3] = dob
                open('profile.txt','w').write('\n'.join(koon))
                print("your data has been updated") 
                
            elif hiv == 4:
                gender = input("gender: ")
                while gender == "":
                    print("this is a compulsory question")
                    gender = input("gender: ")
                with open('profile.txt') as f:
                    normal = f.readlines()
                check = normal[3::12]
                checkmate = str(gender +"\n") in check
                while checkmate == True:
                    print("that is not a valid gender (YES SHUT UP NOT VALID), try again")
                    gender = input("gender: ")
                    while gender == "":
                        print("this is a compulsory question")
                        gender = input("gender: ")
                    check = normal[3::12]
                    checkmate = str(gender +"\n") in check
                koon[user_tag+4] = gender
                open('profile.txt','w').write('\n'.join(koon))
                print("your data has been updated")
            
            elif hiv == 5:
                nation = input("nationality: ")
                while nation == "":
                    print("this is a compulsory question")
                    nation = input("nationality: ")
                with open('profile.txt') as f:
                    normal = f.readlines()
                check = normal[3::12]
                checkmate = str(nation +"\n") in check
                while checkmate == True:
                    print("that is not a valid nationality, try again")
                    nation = input("nationality: ")
                    while nation == "":
                        print("this is a compulsory question")
                        nation = input("nationality: ")
                    check = normal[3::12]
                    checkmate = str(nation +"\n") in check    
                koon[user_tag+5] = nation
                open('profile.txt','w').write('\n'.join(koon))
                print("your data has been updated")

            elif hiv == 6:
                address = input("address: ")
                while address == "":
                    print("this is a compulsory question")
                    address = input("address: ")
                with open('profile.txt') as f:
                    normal = f.readlines()
                check = normal[3::12]
                checkmate = str(address +"\n") in check
                while checkmate == True:
                    print("that is not a valid ADDRESS, try again")
                    address = input("address: ")
                    while address == "":
                        print("this is a compulsory question")
                        address = input("address: ")
                    check = normal[3::12]
                    checkmate = str(address +"\n") in check
                koon[user_tag+6] = address
                open('profile.txt','w').write('\n'.join(koon))
                print("your data has been updated")

            elif hiv == 7:
                medcon = input("any medical conditions: ")
                while medcon =="":
                    print("this is a compulsory question")
                    medcon = input("any medical conditions: ")
                with open('profile.txt') as f:
                    normal = f.readlines()
                check = normal[3::12]
                checkmate = str(medcon +"\n") in check
                while checkmate == True:
                    print("that is not a valid input, try again")
                    medcon = input("any medical conditions: ")
                    while medcon =="":
                        print("this is a compulsory question")
                        medcon = input("any medical conditions: ")
                    check = normal[3::12]
                    checkmate = str(medcon +"\n") in check   
                koon[user_tag+7] = medcon
                open('profile.txt','w').write('\n'.join(koon))
                print("your data has been updated")

            elif hiv == 8:
                while True:
                    try:
                        stdntno = int(input("student phone number: "))
                        break
                    except ValueError:
                        print ("THAT IS NOT A NUMBER DO AGAIN")
                studenthp = str(stdntno)
                while (len(studenthp) < 8) or (stdntno<1):
                    print ("that is not a valid phone number")
                    while True:
                        try:
                            stdntno = int(input("student phone number: "))
                            break
                        except ValueError:
                            print ("THAT IS NOT A NUMBER DO AGAIN")
                    studenthp = str(stdntno)
                koon[user_tag+8] = studenthp
                open('profile.txt','w').write('\n'.join(koon))
                print("your data has been updated")

            elif hiv == 9:
                parentname = input("Parent/Guardian's name: ")
                while parentname == "":
                     print("this is a compulsory question")
                     parentname = input("Parent/Guardian's name: ")
                with open('profile.txt') as f:
                    normal = f.readlines()
                check = normal[3::12]
                checkmate = str(parentname +"\n") in check
                while checkmate == True:
                    print("that is not a valid input, try again")
                    parentname = input("Parent/Guardian's name: ")
                    while parentname == "":
                         print("this is a compulsory question")
                         parentname = input("Parent/Guardian's name: ")
                    check = normal[3::12]
                    checkmate = str(parentname +"\n") in check
                koon[user_tag+9] = parentname
                open('profile.txt','w').write('\n'.join(koon))
                print("your data has been updated")

            elif hiv == 10:
                while True:
                    try:
                        prnthpno = int(input("parent/guardian's phone number: "))
                        break
                    except ValueError:
                       print ("THAT IS NOT A NUMBER DO AGAIN")
                parenthp = str(prnthpno)
                while (len(parenthp) < 8) or (prnthpno<1):
                    print ("that is not a valid phone number")            
                    while True:
                        try:
                            prnthpno = int(input("parent/guardian's phone number: "))
                            break
                        except ValueError:
                           print ("THAT IS NOT A NUMBER DO AGAIN")
                    parenthp = str(parentno) 
                koon[user_tag+10] = parenthp
                open('profile.txt','w').write('\n'.join(koon))
                print("your data has been updated")

            elif hiv == 11:
                chlamydia = 0

            while chlamydia == "1":
                time.sleep(1)
                chlamydia =  input("do you want to amend anything else? enter 1 to continue amending or any other button to exit: ")
                time.sleep(1)
                if chlamydia == "1":
                    break
                

    encryption()
    database()


def delete():
    print("\n\n\n▬▬▬▬▬DELETE▬DATA▬▬▬▬▬")
    decryption()
    global level
    #search:
    #check if tag is in file (citiif)
    def citiif(string_to_search):
        delahoya = open('profile.txt').readlines() 
        if string_to_search in delahoya[3::12]: #search for tag every 12th line in the file
            return True
        return False

    #find position of tag in file (fpotif)
    def fpotif(file_name, string_to_search):
        dorrito = open(file_name, 'r').readlines()
        chewchewchew = dorrito.index(string_to_search)
        return chewchewchew
                

    #get level (glvl)
    def glvl():
        while True:
            try:
                level = int(input("What is your level: Secondary "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")
            
        while (level<1) or (level>5):
            print("your level is not valid, please try again")
            while True:
                try:
                    level = int(input("What is your level: Secondary "))
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")

        return level

    #get class (gclss):
    def gclss():
        level = str(glvl())
        print("1.Charity\n2.Integrity\n3.Humility\n4.Respect\n5.Love\n6.Faith\n7.Hope")
        while True:
            try:
                jar = int(input("Please enter the number of your corresponding class: "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")

        while (jar<1) or (jar>7):
            print("that input is not valid, please try again")
            while True:
                try:
                    jar = int(input("Please enter the number of your corresponding class: ")) 
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")
           
        level = str(level)
        if jar == 1:
            Class = str(level+"cha")
        elif jar == 2:
            Class = str(level+ "int")
        elif jar == 3:
            Class = str(level+"hum")
        elif jar == 4:
            Class = str(level+"res")
        elif jar == 5:
            Class = str(level+"lov")
        elif jar == 6:
            Class = str(level+"fai")
        else:
            Class = str(level+"hop")

        return Class


    #get index number (gindx)
    def gindx():
        while True:
            try:
                number = int(input("enter your index number: "))
                break
            except ValueError:
               print ("THAT IS NOT A NUMBER DO AGAIN")
        indexno = ("%02d" % number)
        indexno = str(indexno)

        while (number<1) or (len(indexno)!=2):
            print("index number has to be 2 digits long")
            while True:
                try:
                    number = int(input("enter your index number: "))
                    break
                except ValueError:
                   print ("THAT IS NOT A NUMBER DO AGAIN")
            indexno = ("%02d" % number)
            indexno = str(indexno)
            
        return indexno

    print("please enter the following details so we can identify you")
    Class = gclss()
    indexno = gindx()
    search_tag= str(Class+indexno+"\n")
    help_me = 0
    while citiif(search_tag) == False:
        print("Sorry but we could'nt identify you")
        ginger = input("enter any button to try again or 1 to exit ")
        if ginger == "1":
            print("goodbye")
            help_me = 1
            #exit to menu
        else:
            time.sleep(1)        
            Class = gclss()
            indexno = gindx()
            search_tag= str(Class+indexno+"\n")
                

    if help_me == 0:           
        user_tag = fpotif('profile.txt', search_tag)
        print("Are you sure you want to delete?")
        blipblop= input("enter any button to continue, or enter 1 to exit ")

        if blipblop == "1":
            print("your data has not been deleted, goodbye") #exit to main menu

        else:
            kay = -1
            koon = open('profile.txt', 'r').read().splitlines()
            for i in range(12):
                kay += 1
                koon[user_tag+kay] = "deleted line"
                
            open('profile.txt','w').write("\n".join(koon))
            print("your data has been deleted")

    encryption()
    database()



#execution
if os.path.exists("profile.txt"):
    fh = open("profile.txt", "r")
else:
    fh = open("profile.txt", "w+")
stuff = ["bruh"]
stuff = (fh.read()).splitlines()
fh.close()
if stuff == []:
    init()
    fh = open("profile.txt", "r")
    stuff = (fh.read()).splitlines()
thatline = ""
thatline = stuff[0]
if thatline[-1] == "a":
    print("NOTE: FILE HAS BEEN AUTOMATICALLY ENCRYPTED AS IT WAS LEFT DECRYPTED")
    encryption()##ENSURE IT STAYS ENCRYPTED

#the big bang
main(1)
