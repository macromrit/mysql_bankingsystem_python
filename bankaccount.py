#உ
import mysql.connector as db
from mysql.connector.cursor import CursorBase
from mysql.connector.errors import DatabaseError
import datetime
import csv
import random


try:
    mydb = db.connect(
        host="127.0.0.1",
        username="root",  

        password="amma@1953",
        database = "bankaccount"
    )
    error = False
    print("connected successfully")

except DatabaseError:
    print("connection unsuccessful")
    error = True

if error:
    print("Ooops! something got fiddled while trying to meet ends right")
#----------------------------------------------------------------------------------------------------------------------------#


else:



    #functions to be used
    #create user
    def createuser():
        """
        contrives a user to the mysql server or databse via python inputs
        name, passcode, id, balance, date_created 
        """
        
        #name-----------------------------------------------------
        while True:

            #name----------------------------------------------------------------------------------->
            while True:
                try:
                    name = str(input("enter you name or 's' to stop: "))
                    #####
                    break
                except(ValueError, KeyboardInterrupt, EOFError):
                    print("Oops the name you entered wasn't valid... Pls try again!!")


            if name=="s":
                print("thankyou")
                break
            else:
                cursor = mydb.cursor()
                cursor.execute('SELECT name FROM bankusers_main')
                check_list = cursor.fetchall()
                cursor.close()

                if ((name,) in check_list)==True:    
                    print("someone had registered that name...try again")
                elif (len(name)<5) and (len(name)>80):
                    print("username too short")           
                elif (len(name)>80):
                    print("username too long")           
                elif name[0]==" ":
                    print("hey don't start with blank spaces.. try again")
                else:
                    valid_name = name



                    #passcode-------------------------------------------------
                    while True:
                        while True:
                            try:
                                passcode1 = str(input("enter you password(must have 8 characters atleast and no spaces between those): "))
                                #####
                                break
                            except(ValueError, KeyboardInterrupt, EOFError):
                                print("Oosps the password you entered wasn't valid... Pls try again!!")
                        
                        while True:    
                            try:
                                passcode2 = str(input("enter you password again: "))
                                #####
                                break
                            except(ValueError, KeyboardInterrupt, EOFError):
                                print("Oops the passwrod you entered wasn't valid... Pls try again!!")
                            
                        
                        if passcode1==passcode2 and 80>len(passcode1)>8 and " " not in passcode1:
                            break
                        else:
                            print("hey it seems something went wrong! might be that your passwords didnt match or was too short or long... or spaces might be the culprit")
                    
                    valid_passcode = passcode1



                    #id---------------------------------------------------------
                    while True:
                        alphas = ("q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m")

                        alldigits = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)

                        exc_symbols = ['@', '#']

                        ans = ""

                        for i in range(1):
                            c = random.choice(exc_symbols)
                            ans+=c

                        for i in range(5):
                            x = random.choice(alphas)
                            ans +=x

                        for z in range(4):
                            y = random.choice(alldigits)
                            ans+=str(y)

                        id_manufactured = ans
                        #-------------------------------------------------------
                        cursor = mydb.cursor()
                        cursor.execute('SELECT used_id FROM bankusers_main')
                        val_list = cursor.fetchall()
                        cursor.close()
                        #-------------------------------------------------------

                        if (id_manufactured,) in val_list:
                            continue
                        else:
                            print("id registered successfully, your id was: {0}".format(id_manufactured))
                            break
                    valid_id = id_manufactured




                #intial acc_ balance----------------------------------------------------------------------------------->
                initial_acc_balance = 0

                #date registered into
                valid_time = datetime.datetime.now()

                #--------------------------------------------------------->

                #insertable values = valid_name, valid_passcode, valid_id, initial_acc_balance, valid_time
                mycursor = mydb.cursor()
                mycursor.execute(F"INSERT INTO bankusers_main VALUES('{valid_name}', '{valid_passcode}', '{valid_id}', {initial_acc_balance}, '{valid_time}')")

                mydb.commit()
                mycursor.close()

                print(F"""
        #############################################
        #                                            
        #   Account info:                              
        #   Name = {valid_name}                         
        #   Password = {len(valid_passcode)*'*'}        
        #   User Id = {valid_id}                                     
        #   Date & Time created: {valid_time}           
        #                                            
        #############################################
                """)
                return "Account created successfully"
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>








#-------------------------------------------------------
#qc test-> passed
    def withdraw_deposit():

        while True:
            
            while True:
                try:
                    name = str(input("Enter your username or enter 's' to stop: "))
                    break
                except(ValueError, EOFError, KeyboardInterrupt):
                    print("hey try again")
            
            
            if name=="s":
                print("thanks for choosing us")
            else:
                while True:
                    try:
                        passcode = str(input("Enter your password: "))
                        break
                    except(ValueError, EOFError, KeyboardInterrupt):
                        print("hey try again")
                cursor = mydb.cursor()
                cursor.execute(F"SELECT name, passcode, balance FROM bankusers_main WHERE name = '{name}'")
                x = cursor.fetchall()
                val = []

                for i in x:
                    val.append(i)
                cursor.close()

                if val == []:
                    print("Ooops, i'm so sorry try again....got messed up with login")
                
                #------------------------------------------------------------->
                else:
                    if val[0][1]==passcode: 

                        while True:
                            try:
                                decider = (str(input("Enter whether you wanna withdraw or deposit funds(W/d): ")).casefold())
                                break
                            except(ValueError, EOFError, KeyboardInterrupt):
                                print("hey try again")
                                
                        if decider == "w":
                            while True:
                                try:
                                    withdrwal_tag = float(input("how much do you wanna withdraw: "))
                                    break
                                except(ValueError, EOFError, KeyboardInterrupt):
                                    print("Ooops! input valid amount")
                            
                            if withdrwal_tag<0 or withdrwal_tag>val[0][2]-1:
                                print("pls try again enter a valid amount or it might be the acc. balance ain't sufficeient enough...")

                            else:
                                bank_value = val[0][2]-withdrwal_tag
                                cursor = mydb.cursor()
                                cursor.execute(F"UPDATE bankusers_main set balance = {bank_value} WHERE name='{name}'")
                                c = datetime.datetime.now()
                                cursor.execute(F"INSERT INTO bankusers_history VALUES('{name}', 'withdrawed', '{c}', {withdrwal_tag})")
                                mydb.commit()
                                cursor.close()
                                
                                print("withdrawed successfully")
                                print("current acc. balance:", bank_value)
                                reciept = F"""
    ####################################################
    #
    #   name = {name}
    #
    #   amount withdrawed = {withdrwal_tag}
    #
    #   total balance = {bank_value}
    #
    #####################################################
                                """                         
                                print(reciept)
                                break

                        elif decider == 'd':
                            while True:
                                try:
                                    deposital_tag = float(input("how much do you wanna deposit: "))
                                    break
                                except(ValueError, EOFError, KeyboardInterrupt):
                                    print("Ooops! input valid amount")
                            
                            if deposital_tag<1:
                                print("Ooops! too low to deposit")
                            else:
                                bank_val = val[0][2]+deposital_tag
                                cursor = mydb.cursor()
                                cursor.execute(F"UPDATE bankusers_main SET balance={bank_val} WHERE name='{name}'")
                                #name with_depo ticky amount
                                z = datetime.datetime.now()
                                cursor.execute(F"INSERT INTO bankusers_history VALUES('{name}', 'deposited', '{z}', {deposital_tag})")
                                mydb.commit()
                                cursor.close()
                                print("deposited successfully")
                                print("current acc. balance:", bank_val)
                                reciept = F"""
    ####################################################
    #
    #   name = {name}
    #
    #   amount deposited = {deposital_tag}
    #
    #   total balance = {bank_val}
    #
    #####################################################
                                """
                                print(reciept)
                                break

                        else:
                            print("Oooops! transactions failed")
                        
                    else:
                        print("username didn't match password... try again")


#--------------------------------------------------------------------------------------------------------------------------------------->
#qc test-> passed
    def transfer_funds():
        while True:
            
            while True:
                try:
                    name = str(input("Enter your username or enter 's' to stop: "))
                    break
                except(ValueError, EOFError, KeyboardInterrupt):
                    print("hey try again")
            

            if name=="s":
                print("thanks for choosing us")
                break
            else:
                while True:
                    try:
                        passcode = str(input("Enter your password: "))
                        break
                    except(ValueError, EOFError, KeyboardInterrupt):
                        print("hey try again")

                cursor = mydb.cursor()
                cursor.execute(F"SELECT name, passcode, balance FROM bankusers_main WHERE name = '{name}'")
                x = cursor.fetchall()
                val = []

                for i in x:
                    val.append(i)
                cursor.close()

                if val == []:
                    print("Ooops, i'm so sorry try again....no such user found ")
                
                #------------------------------------------------------------->
                else:
                    if val[0][1]==passcode: 

                        while True:
                            try:
                                reciver = str(input("Enter the name of the user you wanna send funds to: "))
                                break
                            except(ValueError, EOFError, KeyboardInterrupt):
                                print("Sorry.. something went wrong try again".title())
                        
                        while True:
                            try:
                                reciver_id = str(input("Enter recievers bank id: "))
                                break
                            except(ValueError, EOFError, KeyboardInterrupt):
                                print("Sorry.. something went wrong try again".title())
                    
                        cursor = mydb.cursor()
                        cursor.execute(F"SELECT name, used_id, balance FROM bankusers_main WHERE name = '{reciver}'")
                        v = cursor.fetchall()
                        list1 = []
                        for i in v:
                            list1.append(i)
                        if list1 == []:
                            print("no such user found to send money... Try again")
                        elif reciver == list1[0][0]:
                            if reciver_id == list1[0][1]:
                                values = float(input(F"enter the amount to be transferred to {reciver}: "))
                                if (values<val[0][2]-1) and values>0:
                                    
                                    bank_value = val[0][2]-values
                                    bank_value2 = list1[0][2]+values
                                    cursor = mydb.cursor()
                                    cursor.execute(F"UPDATE bankusers_main set balance = {bank_value} WHERE name='{name}'")
                                    c = datetime.datetime.now()
                                    cursor.execute(F"INSERT INTO bankusers_history VALUES('{name}', 'withdrawed', '{c}', {values})")
                                    cursor.execute(F"INSERT INTO bankusers_transferr VALUES('{name}', '{reciver}', '{reciver_id}', {values}, '{c}')")
                                    cursor.execute(F"UPDATE bankusers_main set balance = {bank_value2} WHERE name='{reciver}'")
                                    mydb.commit()
                                    cursor.close()
                                    print("transfer successful")
                                    reciept = F"""
    #############################################
    #
    #   transferred from: {name}   
    #
    #   transferred to: {reciver}
    # 
    #   total funds transferred: {values}
    #
    #############################################                                
                                    """
                                    print(reciept)
                                    break

                                else:
                                    print("insufficient funds to transfer")
                            else:
                                print("id didnt match.. try again")                        

                        else:
                            print("No such user figured :(")
                        
                    
                        
                    else:
                        print("username didn't match password... try again".title())




    def view_info():
        while True:
            
            while True:
                try:
                    name = str(input("Enter your username or enter 's' to stop: "))
                    break
                except(ValueError, EOFError, KeyboardInterrupt):
                    print("hey try again")
            

            if name=="s":
                print("thanks for choosing us")
                break
            else:
                while True:
                    try:
                        passcode = str(input("Enter your password: "))
                        break
                    except(ValueError, EOFError, KeyboardInterrupt):
                        print("hey try again")

                cursor = mydb.cursor()
                cursor.execute(F"SELECT name, passcode, balance, used_id, date_created FROM bankusers_main WHERE name = '{name}'")
                x = cursor.fetchall()
                val = []

                for i in x:
                    val.append(i)
                
                val1 = []
                cursor.execute(F"SELECT * FROM bankusers_transferr WHERE sender_name='{name}'")
                ads = cursor.fetchall()
                for i in ads:
                    val1.append(i)

                val2 = []
                cursor.execute(F"SELECT * FROM bankusers_history WHERE name='{name}'")
                bbs = cursor.fetchall()
                for z in bbs:
                    val2.append(z)
                cursor.close()

                if val == []:
                    print("Ooops, i'm so sorry try again....no such user found ")
                
                #------------------------------------------------------------->
                else:
                    if val[0][1]==passcode: 
                        print(F"""
                 USER INFO                        
############################################
#
#   name: {name}
#   user_id: {val[0][3]}
#   account was created on: {val[0][4]}
#   balance: {val[0][2]}
# 
############################################                        
                        """)

                        count = 1
                        print('-'*40)
                        print("Fund Tranfer History")
                        if val1!=[]:
                            for i, j, k, l, m in val1:
                                
                                print(F"""
    ############################################
    #
    #   transfer no.: {count}
    #   senders name: {i}
    #   recievers name: {j}
    #   reciever's id: {k}
    #   amount transferred: {l}
    #   date transferred: {m}   
    #
    ############################################
                                """)
                                count+=1
                        else:
                            print("No transactions made yet")



                        county1 = 1
                        county2 = 1

                        print('-'*40)
                        print("withdrawal-deposital history")
                        if val2!=[]:
                            for i, j, k, l in val2:
                                if j == "withdrawed":
                                    print(F"""
    #############################################
    #
    #      withdrwal no.: {county1}
    #      date: {k}
    #      amount: {l}
    #
    ##############################################                            
                                    """)
                                    county1+=1

                                else:#deposited
                                    print(F"""
    #############################################
    #
    #      deposital no.: {county2}
    #      date: {k}
    #      amount: {l}
    #
    ##############################################                            
                                    """)
                                    county2+=1                                
                        else:
                            print("No depositions or withrawals made yet.... Hopefully do it soon")
                    
                    else:
                        print("password did'nt match")
    def deleteacc():
        while True:
            
            while True:
                try:
                    name = str(input("Enter your username or enter 's' to stop: "))
                    break
                except(ValueError, EOFError, KeyboardInterrupt):
                    print("hey try again")
            
            
            if name=="s":
                print("thanks for choosing us")
                break
            else:
                while True:
                    try:
                        passcode = str(input("Enter your password: "))
                        break
                    except(ValueError, EOFError, KeyboardInterrupt):
                        print("hey try again")
                cursor = mydb.cursor()
                cursor.execute(F"SELECT name, passcode, balance FROM bankusers_main WHERE name = '{name}'")
                x = cursor.fetchall()
                val = []

                for i in x:
                    val.append(i)
                cursor.close()

                if val == []:
                    print("Ooops, No such user found")
                
                #------------------------------------------------------------->
                else:
                    #main cintent
                    sure = str(input("are you sure to delete(input yes or no): "))
                    if sure=="yes":
                        cursor = mydb.cursor()
                        cursor.execute(F"DELETE FROM bankusers_main WHERE name='{name}'")
                        cursor.execute(F"DELETE FROM bankusers_transferr WHERE sender_name='{name}'")
                        cursor.execute(F"DELETE FROM bankusers_history WHERE name='{name}'")
                        mydb.commit()
                        cursor.close()
                        print("account deleted successfully.. will miss you for sure.")
                        break
                    elif sure=="no":
                        print("ohhh... good decision.")
                        break
                    else:
                        print("Sorry.. Try again")



    while True:
        while True:
            try:
                menu = str(input("what do ya wanna do(transfer(T)/ withdrawal or deposit(W&D)/ create account(C)/ History(H)/ stop(S)/ delete account(D): ")).casefold()
                #---------------------------------------------------------------->
                break
            except(ValueError, EOFError, KeyboardInterrupt):
                print("Hey try again... was too complex")

        if menu=="t":
            transfer_funds()
        elif menu=="h":
            view_info()
        elif menu=="d":
            deleteacc()
        elif menu=="w&d":
            withdraw_deposit()
        elif menu=="c":
            createuser()
        elif menu=="s":
            print("thanks for choosing us")
            break
        else:
            print("Ooops... give a valid input. Try again")
    
    
