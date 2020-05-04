import mysql.connector
import random
import re
import math
from datetime import date
from datetime import datetime
from pip._vendor.distlib.compat import raw_input
from builtins import input
def promptForDetails():
    name = input("Enter name: \n")
    if len(name) == 0:
        print("Enter a name Atleast..")
        return
    while True:
        dob = input("Enter DOB(YYYY-MM-DD): \n") #1996-12-31
        flag = 0
        x = dob.split("-")
        if not (int(x[1])>0 and int(x[1])<13):
            flag = -1
        elif not (int(x[2])>0 and int(x[2])<32):
            flag = -1
        elif not (int(x[0])>1800 and int(x[0])<2002):
            flag = -1
        if flag == -1:
            print("Enter valid DOB")
        else:
            break
    while True:
        password = input("Enter password: \n")
        flag = 0
        if (len(password)<8): 
            flag = -1
        elif not re.search("[a-z]", password): 
            flag = -1
        elif not re.search("[A-Z]", password): 
            flag = -1
        elif not re.search("[0-9]", password): 
            flag = -1
        elif not re.search("[_@$]", password): 
            flag = -1
        elif re.search("\s", password): 
            flag = -1
        if flag == -1:
            print(" Retry valid pass")
        else:
            break
    address = input("Enter address: \n")
    pan = input("Enter PAN Number \n")
    while True:
        mobile = input("Enter your Mobile number: \n")
        if len(mobile) != 10:
            print("Enter a valid mobile number: \n")
        else:
            break
    #acctype = input("Enter the account type: \n")
    #balance = int(input("Enter amount to be addded to your account: \n"))
    #if acctype == "current" and balance < 5000:
    #    print("Account could not be created as amount you have added is less than 5000")
    #    return
    #else:
    #    print(balance," added to your",acctype," account")
    custID = "CUST"+str(random.randint(100000,999999))
    #accountno = custID
    stmt = ("""insert into customers (Customer_Id,Password,name,Address,Pan,Mobile,DOB) values
                    (%s,%s,%s,%s,%s,%s,%s)""")
    data = (custID,password,name,address,pan,mobile,dob)
    cur.execute(stmt,data)
    con.commit()
    print("User account successfully created")
    
def signIn():
    cur.execute("select Customer_Id,password from customers")
    for row in cur.fetchall():
            dataset[row[0]] = row[1]
    i=3
    while True:
        custId = input("Enter customer id: \n")
        if custId in dataset.keys():
            while i>0:
                password = input("Input Password : \n")
                if dataset.get(custId) == password:
                    print("successful Login")         
                    break
                else:
                    i = i-1
                    print("you have entered wrong credentials, tries left = ",i)
                if i == 0:
                    print("Account is locked, it was nice working with you! BYE")
                    return
        else:
            print("Enter a valid customer id")
        break
    subSignIn(custId)


def createSA(customer_Id):
    Account_no = "SAV" + str(random.randint(1000000,9999999))
    account_type = "saving"
    balance = int(raw_input("Enter the amount to be deposited or press enter to skip: \n") or "0")
    account_creation_date = date.today()
    stmt = """insert into accounts (Account_no,Customer_Id,Balance,Account_Type,Account_creation_Date)
                values (%s,%s,%s,%s,%s)"""
    data = (Account_no,customer_Id,balance,account_type,account_creation_date)
    cur.execute(stmt,data)
    con.commit()
    return
    
def createCA(customer_Id):
    Account_no = "CUR" + str(random.randint(1000000,9999999))
    account_type = "current"
    balance = 0
    balance = int(input("Enter amount to be added to your account: \n"))
    if account_type == "current" and balance < 5000:
        print("Account could not be created as amount you have added is less than 5000")
        return
    else:
        print(balance," added to your",account_type," account")
    account_creation_date = date.today()
    stmt = """insert into accounts (Account_no,Customer_Id,Balance,Account_Type,Account_creation_Date)
                values (%s,%s,%s,%s,%s)"""
    data = (Account_no,customer_Id,balance,account_type,account_creation_date)
    cur.execute(stmt,data)
    con.commit()
    return


def createFD(customer_Id):
    print("""Amount to be deposited should be a multiple of 1000 and minimum term for FD will be 12 months""")
    while True:
        amount = int(input("Enter amount for FD: \n"))
        if not amount < 1000:
            if amount % 1000 == 0:
                break
            else:
                print("input amount is not a multiple of 1000,retry \n")
        else:
            continue
    while True:
        term = int(input("Enter the term for FD: \n"))
        if term < 12:
            print("Term should be equal to or more than 12 months: \n")
        else:
            break
    fd_accountno = "FD" + str(random.randint(10000000,99999999))
    return_amount = (((amount*5*term)/100) + amount)
    stmt = """insert into fixedAccount (Fd_Account_No,Customer_Id,Amount,Term,Return_Amount)
                values (%s,%s,%s,%s,%s)"""
    data = (fd_accountno,customer_Id,amount,term,return_amount)
    cur.execute(stmt,data)
    con.commit()
    print("FD created successfully.... with FD Account no :",fd_accountno)
    return
    
def subSignIn(customer_Id):
    while True:
        today = date.today()
        print("_________SUB MENU________")
        print("1: Address Change")
        print("2: Open New Account")
        print("3: Money Deposit")
        print("4: Money Withdraw")
        print("5: Transfer Money")
        print("6: Print Statement")
        print("7: Account Closure")
        print("8: Avail Loan")
        print("0: Customer Logout")
        choice = input("Enter your choice: \n")
        #Address change Logic below:
        if choice == "1":
            address = input("Enter your new address: \n")
            stmt = """Update customers set Address = %s where
                        Customer_Id = %s"""
            data = (address,customer_Id)
            cur.execute(stmt,data)
            con.commit()
            print("address changed successfully for customerID:",customer_Id,"address:",address)
        #Open New Account logic below:
        if choice == "2":
            print("_________Opening Of New Account________")
            print("1: Open Savings Account")
            print("2: Open Current Account")
            print("3: Open Fixed Deposit")
            print("""A customer can have either of the following type of accounts:
**Savings Account – Generally used for temporary savings.
    Offers interest at the rate of 7.5% per annum on your savings.
    Maximum 10 withdrawals are allowed per month.
    No minimum balance is needed to open or maintain this account.
**Current Account – Generally used by corporate peeps and business men.
    No interest is offered on this account.
    No limit of on no. of withdrawals.
    A customer needs to have minimum 5K to open or maintain this account.
**Fixed Deposit – Amount should not be negative and should be in multiples
    of 1000, term should not be negative""")
            choice = input("Enter your choice: \n")
            if choice == "1":
                createSA(customer_Id)
            elif choice == "2":
                createCA(customer_Id)
            elif choice == "3":
                createFD(customer_Id)
            else:
                print("Invalid Choice, Select correct choice \n")
                return
            return
        # Money Deposit Logic below:
        if choice == "3":
            amount = int(input("Enter amount to be Deposited: \n"))
            if amount <= 0:
                print("Enter valid amount")
                return
            # For valid account no:
            while True:
                account_no = input("Enter the account no in which you want to deposit: \n")
                stmt1 = """select Customer_Id,Balance from accounts where Account_no = %(accno)s"""
                cur.execute(stmt1,{'accno':account_no})
                result_set = cur.fetchall()
                custid = ""
                for row in result_set:
                    custid = row[0]
                    balance = int(row[1])
                if custid == customer_Id:
                    print("Account number verified: \n")
                    break
                else:
                    continue
            # For creating transaction id
            stmt2 = "select * from transactions"
            cur.execute(stmt2)
            cur.fetchall()
            rowcnt = cur.rowcount
            transaction_Id = rowcnt + 1;
            transaction_Type = "deposit"
            #DateTime import is used and today's date is created here
            Date_Of_Transaction = str(date.today())
            to_account   = account_no
            from_account = account_no
            #inserting into transactions table:
            stmt3 = """insert into transactions (Transaction_Id,Date_Of_Transaction,From_Account,To_Account,Type_Of_Transaction,Amount)
                        values (%s,%s,%s,%s,%s,%s)"""
            data = (transaction_Id,Date_Of_Transaction,from_account,to_account,transaction_Type,amount)
            cur.execute(stmt3,data)
            balance = balance + amount
            #updating balance in accounts table:
            stmt4 = """update accounts set Balance = %(bln)s where Account_no = %(acno)s"""
            cur.execute(stmt4,{'bln':balance,'acno':account_no})
            print("Updated the balance for the account:",balance)
            con.commit()
            
        # Money withdraw logic below:
        if choice == "4":
            amount = int(input("Enter amount to be withdrawn: \n"))
            if amount <= 0:
                print("Enter valid amount")
                return
            # For valid account no:
            while True:
                account_no = input("Enter the account number: \n")
                stmt1 = """select balance,Customer_Id from accounts where account_no = %(accno)s"""
                cur.execute(stmt1,{'accno':account_no})
                result_set = cur.fetchall()
                custid = ""
                for row in result_set:
                    balance = int(row[0])
                    custid = row[1]
                if custid == customer_Id:
                    print("Account number verified: \n")
                    break
                else:
                    continue
            stmt2 = """select Account_Type from accounts where Account_no  = %(accno)s"""
            cur.execute(stmt2,{'accno':account_no})
            result_set = cur.fetchall()
            for row in result_set:
                acctype = row[0]
            #validating number of transaction rule for saving account:
            if acctype == "saving":
                stmt3 = """select count(Date_Of_Transaction) from transactions where From_Account
                        = %(accno)s AND Type_Of_Transaction = 'withdraw' AND
                        month(Date_Of_Transaction) = month(now())"""
                cur.execute(stmt3,{'accno':account_no})
                rows = cur.fetchall()
                count = 0
                for row in rows:
                    count = int(row[0])
                if count > 9:
                    print("Your total number of transactions for the month is over: COME BACK NEXT MONTH!!")
                    return
            else:
                # creating transaction id:
                stmt4 = "select * from transactions"
                cur.execute(stmt4)
                cur.fetchall()
                rc = cur.rowcount
                transaction_Id = rc + 1;
                transaction_Type = "withdraw"
                #DateTime import is used and today's date is created here
                Date_Of_Transaction = str(date.today())
                #valid amount to be withdrawn check:
                if amount > balance:
                    print("insufficient balance...u have: ",balance," balance")
                    return
                # withdraw check for current account according to the rule:
                elif acctype == "current":
                    balance = balance - amount
                    if balance < 5000:
                        print("Voilating the current account rules")
                        return
                else:
                    
                    balance = balance - amount
                    print("Amount left in your account:",balance)
                # updating the accounts table:
                stmt5 = """update accounts set Balance = %s where Account_no = %s"""
                cur.execute(stmt5,(balance,account_no))
                from_account = account_no
                to_account = account_no
                # inserting a new transaction in transactions table
                stmt6 = """insert into transactions (Transaction_Id,Date_Of_Transaction,From_Account,To_Account,Type_Of_Transaction,Amount)
                        values (%s,%s,%s,%s,%s,%s)"""
                data = (transaction_Id,Date_Of_Transaction,from_account,to_account,transaction_Type,amount)
                cur.execute(stmt6,data)
                print("Amount successfully Withdrawn.........balance:",balance)
                con.commit()
        
        # Money transfer logic below:
        if choice == "5":
            account_to = input("Enter the account no of reciever: \n")
            # stmt1 is used to validate the reciever account
            stmt1 = """select * from accounts where Account_no = %(actno)s"""
            cur.execute(stmt1,{'actno':account_to})
            cur.fetchall()
            if not cur.rowcount == 1:
                print("Reciever account doesn't exists,enter again")
                return
            else:
                amount = int(input("Enter the amount to be transfered: \n"))
                if amount <= 0:
                    print("Enter valid amount")
                    return
                # stmt2 is used to get balance and account type of the sender
                account_from = input("Enter your account no.: \n")
                stmt2 = """select Balance,Account_Type from accounts where Account_no = %(accno)s"""
                cur.execute(stmt2,{ 'accno': account_from })
                current = cur.fetchall()
                balance = 0
                # validating the amount and the current account properties
                for curr in current:
                    balance = int(curr[0])
                    account_type = curr[1]
                    if amount > balance:
                        print("insufficient balance...u have: ",balance," balance")
                        return
                    elif account_type == "current":
                        balance = balance - amount
                        if balance < 5000:
                            print("Voilating the current account rules")
                            return
                    else:
                        balance = balance - amount
                # stmt3 is used to update the balance in the accounts table for sender
                stmt3 = """update accounts set Balance = %(blnc)s where
                            Account_no = %(accno)s"""
                cur.execute(stmt3,{'blnc':balance,'accno':account_from})
                # stmt4 & 5 is used to update the balance in the accounts table for reciever
                stmt4 = """select Balance from accounts where Account_no = %(accno)s"""
                cur.execute(stmt4,{'accno':account_to})
                res = cur.fetchall()
                for r in res:
                    rbalance = int(r[0])
                    rbalance = rbalance + amount
                stmt5 = """update accounts set Balance = %(blnc)s where
                            Account_no = %(accno)s"""
                cur.execute(stmt5,{'blnc':rbalance,'accno':account_to})
                # stmt 6 is used to get the rows in transaction table and to generate transfer ID
                stmt6 = "select * from transactions"
                cur.execute(stmt6)
                cur.fetchall()
                rc = cur.rowcount
                transferId = rc + 1;
                dateOfTransfer = str(date.today())
                if account_type == "saving":
                    # stmt 7  is used to validate the 10 transaction rules on the savings account
                    stmt7 = """select count(Date_Of_Transaction) from transactions where From_Account
                            = %(accno)s AND Type_Of_Transaction = 'withdraw' 
                            AND month(Date_Of_Transaction) = month(now())"""
                    cur.execute(stmt7,{'accno':from_account})
                    rows = cur.fetchall()
                    count = 0
                    for row in rows:
                        count = int(row[0])
                    if count > 9:
                        print("Your total number of transactions for the month is over: COME BACK NEXT MONTH!!")
                        return
                else:
                    # stmt 8 is used to get the row in transactions table and to generate the transaction id
                    stmt8 = "select * from transactions"
                    cur.execute(stmt8)
                    cur.fetchall()
                    rc = cur.rowcount
                    transaction_Id = rc + 1;
                    transaction_Type = "transfer"
                    # stmt 9 is used to add a row in the transactions table about the transfer
                    stmt9 = """insert into transactions
                            (transaction_Id,Date_Of_Transaction,From_Account,To_Account,Type_Of_Transaction,Amount)
                            values (%s,%s,%s,%s,%s,%s)"""
                    data = (transaction_Id,dateOfTransfer,account_from,account_to,transaction_Type,amount)
                    cur.execute(stmt9,data)
                    con.commit()
                    print("Amount Transfered successfully to :",account_to)

        #Logic for printing statement below:
        if choice == "6":
            account_no = input("Enter your account no: \n")
            date_from = input("Enter the starting date for statement(YYYY-MM-DD):\n")
            date_to = input("Enter the ending date for statement(YYYY-MM-DD): \n")
            stmt = """select Customer_Id from accounts where Account_no = %(acno)s"""
            cur.execute(stmt,{'acno':account_no})
            result = cur.fetchall()
            if cur.rowcount == 1:
                for r in result:
                    custid = r[0]
                if custid == customer_Id:
                    print("Account number is verified")
                    dt_from = date_from.split("-")
                    dt_to = date_to.split("-")
                    dt1 = ""
                    dt2 = ""
                    for i in dt_from:
                        dt1 = dt1 + i
                    for j in dt_to:
                        dt2 = dt2 + j
                    dt1 = int(dt1)
                    dt2 = int(dt2)
                    if dt2 > dt1:
                        print("Date verified")
                        stmt1 = """select Date_Of_Transaction,Type_Of_Transaction,Amount from transactions
                                    where Date_Of_Transaction >= %(dt_from)s AND Date_Of_Transaction <= %(dt_to)s"""
                        cur.execute(stmt1,{'dt_from':date_from,'dt_to':date_to})
                        resultSet = cur.fetchall()
                        print("[-  DATE     -  TYPE_OF_TRANSACTION  -  AMOUNT  -]")
                        for row in resultSet:
                            Date_Of_Transaction = row[0]
                            Type_of_transaction = row[1]
                            amount = row[2]
                            print(" ",Date_Of_Transaction,"\t",Type_of_transaction,"\t\t",amount)
                    else:
                        print("The starting date is greater than the ending date for statement..")
                else:
                    print("the account number doesn't belong to you")
            else:
                print("No account Found")
            
        
        #Logic for Account Closure below:
        if choice == "7":
            print("ARE YOU SURE YOU WANT TO DELETE YOUR ACCOUNT FROM THIS BANK \n")
            print("IF YES THEN ENTER YOUR ACCOUNT NO. \n")
            account_no = input()
            stmt1 = """select Account_Type from accounts where account_no = %(acnt)s"""
            cur.execute(stmt1,{'acnt':account_no})
            result = cur.fetchall()
            for r in result:
                account_type = r[0]
            stmt3 = """insert into ClosedAccounts (Account_no,Account_Type,Date_Of_Closure)
                        values (%s,%s,%s)"""
            today = str(date.today())
            data = (account_no,account_type,today)
            cur.execute(stmt3,data)
            stmt2 = """delete from accounts where account_no = %(acn)s"""
            cur.execute(stmt2,{'acn':account_no})
            print("Account closed successfully: ",account_no)
            con.commit()
            
        
        #Logic for loan account below:
        if choice == "8":
            print("""Amount of loan should be a multiple of 1000""")
            while True:
                amount = int(input("Enter amount for Loan : \n"))
                if not amount < 1000:
                    if amount % 1000 == 0:
                        break
                    else:
                        print("input amount is not a multiple of 1000,retry \n")
                else:
                    continue
            while True:
                term = int(input("Enter the Repayment term(in months): \n"))
                if term < 1:
                    print("Enter a valid Repayment term: \n")
                else:
                    break
            loan_no = "LOAN" + str(random.randint(100000,999999))
            return_amount = (((amount*7*term)/100) + amount)
            repayment_termwise_amount = math.ceil(return_amount / term)
            
            stmt = """insert into loans (Loan_Account_No,Customer_Id,Amount,Repayment_Term,Return_Amount,
                        Repayment_TermWise_Amount) values (%s,%s,%s,%s,%s,%s)"""
            data = (loan_no,customer_Id,amount,term,return_amount,repayment_termwise_amount)
            cur.execute(stmt,data)
            con.commit()
            print("Loan Availed successfully.... with Loan number :",loan_no)
            
        # Logic Report of Customers who are yet to avail a loan below:
        if choice == "9":
            cur.execute("""""");
        
        # Logic for Logout below:
        if choice == "0":
            print("Customer Logout successfull")
            return
        
def adminSignIn():
    cur.execute("select Admin_Id,password from admins")
    for row in cur.fetchall():
        dataset[row[0]] = row[1]
    while  True:
        adminId = input("Enter Admin id: \n")
        if adminId in dataset.keys():
            while True:
                passwd = input("Input Password : \n")
                if dataset.get(adminId) == passwd:
                    print("successful Login")            
                    break
                else:
                    print("you have entered wrong Password")
                    continue
            break
        else:
            print("Enter a valid admin Id")
    while True:
        print("-------ADMIN SUB-MENU-------\n")
        print("1.  print closed account history \n")
        print("2.  FD Report of a Customer \n")
        print("3.  FD Report of Customers vis-a-vis another Customer \n")
        print("4.  FD Report of Customers w.r.t a particular FD Amount \n")
        print("5.  Loan Report of a Customer \n")
        print("6.  Loan Report of Customers vis-a-vis another Customer \n")
        print("7.  Loan Report of Customers w.r.t a particular Loan Amount \n")
        print("8.  Loan�FD Report of Customers \n")
        print("9.  Report of Customers who are yet to avail a loan \n")
        print("10. Report of Customers who are yet to open a FD account \n")
        print("11. Report of Customers who neither have a loan nor a FD account with the bank \n")
        print("0.  Admin logout \n")
        choice = input("Enter your choice: \n")
        
        # logic for the display of all closed accounts below:
        if choice == "1":
            stmt = """select * from ClosedAccounts"""
            cur.execute(stmt)
            resultSet = cur.fetchall()
            i = 0
            for result in resultSet:
                accno = result[0]
                accType = result[1]
                doc = result[2]
                i = i + 1
                print(i,".) ","Account No.: ",accno,"\t","Account type: ",accType,"\t","Date of closure: ",doc,"\t")
                
        # logic for FD report for a customer below :
        if choice == "2":
            while True:
                custId = input("Enter a customer Id: \n")
                stmt = "Select * from customers where Customer_Id = %(custid)s"
                cur.execute(stmt,{'custid':custId})
                cur.fetchall()
                if cur.rowcount == 1:
                    stmt1 = """select Fd_Account_No,Amount,Term from fixedAccount where Customer_Id = %(custid)s"""
                    cur.execute(stmt1,{'custid':custId})
                    resultSet = cur.fetchall()
                    i = 0
                    for result in resultSet:
                        fd_account_no = result[0]
                        amount = result[1]
                        term = result[2]
                        i = i + 1
                        print(i,".) ","FD Account No.: ",fd_account_no,"Amount: ",amount,"Term : ",term)
                    break
                else:
                    print("Enter a valid Customer Id")
        # logic for Display the details of all customers who have a FD with amount greater than
        # or equal to the sum of all FD amounts of the selected customer below:
        if choice == "3":
            while True:
                custId = input("Enter a customer Id: \n")
                stmt = "Select * from fixedAccount where Customer_Id = %(custid)s"
                cur.execute(stmt,{'custid':custId})
                cur.fetchall()
                if cur.rowcount > 0:
                    stmt1 = """select Customer_Id,Fd_Account_No,Amount,Term from fixedaccount where Amount > (
                                select sum(amount) from fixedaccount where Customer_Id = %(custid)s)"""
                    cur.execute(stmt1,{'custid':custId})
                    resultSet = cur.fetchall()
                    i = 0
                    for result in resultSet:
                        custId = result[0]
                        fd_account_no = result[1]
                        amount = result[2]
                        term = result[3]
                        i = i + 1
                        print(i,".) ","Customer Id: ",custId,"FD Account No.: ",fd_account_no,"Amount: ",amount,"Term : ",term)
                    break
                else:
                    print("Enter a Customer Id that have FD account")
        #Logic for listing the details of all customers (customer-id, first name,
        # last name, FD amount) who have an FD of amount greater than the selected amount below:
        if choice == "4":
            while True:
                amount = int(input("Enter amount: \n"))
                if not amount < 1000:
                    if amount % 1000 == 0:
                        break
                    else:
                        print("input amount is not a multiple of 1000,retry \n")
                else:
                    continue
            stmt = """select c.Customer_Id,c.name,f.amount from fixedaccount as f 
                    inner join customers as c on c.Customer_Id = f.Customer_Id where f.amount > %(amt)s"""
            cur.execute(stmt,{'amt':amount})
            resultSet = cur.fetchall()
            i = 0
            for result in resultSet:
                custId = result[0]
                name = result[1]
                amount = result[2]
                i = i + 1
                print(i,".) ","Customer Id:",custId,"<Name of customer: ",name,",Amount: ",amount)
        
        #Logic for the loan report of a customer below:
        if choice == "5":
            while True:
                custId = input("Enter a customer Id: \n")
                stmt = "Select * from loans where Customer_Id = %(custid)s"
                cur.execute(stmt,{'custid':custId})
                cur.fetchall()
                if cur.rowcount == 1:
                    stmt1 = """select Loan_Account_No,Amount,Repayment_Term from loans where Customer_Id = %(custid)s"""
                    cur.execute(stmt1,{'custid':custId})
                    resultSet = cur.fetchall()
                    i = 0
                    for result in resultSet:
                        Loan_Account_No = result[0]
                        amount = result[1]
                        Repayment_Term = result[2]
                        i = i + 1
                        print(i,".) ","Loan Account No.: ",Loan_Account_No,"Amount: ",amount,"Repayment Term : ",Repayment_Term)
                    break
                else:
                    print("The loan is not availed by the given customer having id:",custId)
                    break
        
        #Logic for the Display of details of all customers
        # who have availed a loan with loan amount greater
        # than or equal to the total loan amount of the selected customer below:
        if choice == "6":
            while True:
                custId = input("Enter a customer Id: \n")
                stmt = "Select * from loans where Customer_Id = %(custid)s"
                cur.execute(stmt,{'custid':custId})
                cur.fetchall()
                if cur.rowcount > 0:
                    stmt1 = """select Customer_Id,Loan_Account_No,Amount,Repayment_Term from loans where Amount > (
                                select sum(amount) from loans where Customer_Id = %(custid)s)"""
                    cur.execute(stmt1,{'custid':custId})
                    resultSet = cur.fetchall()
                    i = 0
                    for result in resultSet:
                        custId = result[0]
                        Loan_Account_No = result[1]
                        amount = result[2]
                        Repayment_Term = result[3]
                        i = i + 1
                        print(i,".) ","Customer Id: ",custId,"Loan Account No.: ",Loan_Account_No,"Amount: ",amount,"Repayment_Term : ",Repayment_Term)
                    break
                else:
                    print("Enter a Customer Id that have availed atleast one loan")
            
        #Logic for Loan Report of Customers w.r.t a particular Loan Amount below:
        if choice == "7":
            while True:
                amount = int(input("Enter amount: \n"))
                if not amount < 1000:
                    if amount % 1000 == 0:
                        break
                    else:
                        print("input amount is not a multiple of 1000,retry \n")
                else:
                    continue
            stmt = """select c.Customer_Id,c.name,l.Amount from loans as l 
                    inner join customers as c on c.Customer_Id = l.Customer_Id where l.amount > %(amt)s"""
            cur.execute(stmt,{'amt':amount})
            resultSet = cur.fetchall()
            i = 0
            for result in resultSet:
                custId = result[0]
                name = result[1]
                loan_amount = result[2]
                i = i + 1
                print(i,".) ","Customer Id:",custId,",Name of customer: ",name,",Loan Amount: ",loan_amount)
        #Logic Display the list of Customers whose sum of loan amounts is greater than the sum 
        #of FD amounts below:
        if choice == "8":
            cur.execute("""with temp (custid,name,sumOfLoan,sumOfFd) AS
                            (select c.Customer_Id,c.name,sum(l.amount) as
                             sum_of_loan_amount,sum(f.amount) as sum_of_fd_amount from customers as c
                            inner join loans as l on c.Customer_Id = l.Customer_Id
                            inner join fixedaccount as f 
                            on l.Customer_Id = f.Customer_Id group by f.Customer_Id)
                            SELECT custid,name,sumOfLoan,sumOfFd from temp where sumOfLoan > sumOfFd""")
            resultSet = cur.fetchall()
            i = 0
            for row in resultSet:
                custid = row[0]
                name = row[1]
                sumOfLoan = row[2]
                sumOfFd = row[3]
                i = i + 1
                print(i,".) ","Customer Id:",custid,",customer name:",name,",Sum of loan:",sumOfLoan,",Sum of FixedAccount:",sumOfFd)
            
        #Logic for Report of Customers who are yet to avail a loan below:
        if choice == "9":
            cur.execute("""select Customer_Id,name from customers where
                         Customer_Id not in (select distinct Customer_Id from loans)""")
            resultSet = cur.fetchall()
            i = 0
            for row in resultSet:
                custid = row[0]
                name = row[1]
                i = i + 1
                print(i,".) ","Customer Id:",custid,",customer name:",name)
            
        #Logic for Report of Customers who are yet to open a FD account below:
        if choice == "10":
            cur.execute("""select Customer_Id,name from customers where
                         Customer_Id not in (select distinct Customer_Id from fixedAccount)""")
            resultSet = cur.fetchall()
            i = 0
            for row in resultSet:
                custid = row[0]
                name = row[1]
                i = i + 1
                print(i,".) ","Customer Id:",custid,",customer name:",name)
            
        # Logic Report of Customers who neither have a loan nor a FD account with the bank below:
        if choice == "11":
            cur.execute("""select Customer_Id,name from customers where Customer_Id not in 
                        (select distinct Customer_Id from fixedAccount union select distinct Customer_Id from loans)""")
            resultSet = cur.fetchall()
            i = 0
            for row in resultSet:
                custid = row[0]
                name = row[1]
                i = i + 1
                print(i,".) ","Customer Id:",custid,",customer name:",name)
        
        
        # logic for Admin logout below:
        if choice == "0":
            print("admint logout successfull")
            return
        
con = mysql.connector.connect(
    host   = "localhost",
    user   = "root",
    passwd = "root"
    )
dataset = {}
cur = con.cursor()
cur.execute("use bankSystem")
while True:
    print("______MAIN MENU______")
    print("1. Sign Up(New Customer)")
    print("2. Sign In(Existing Customer)")
    print("3. Admin Sign In")
    print("0. Quit")
    choice = input("Select the option from above: \n")
    if choice == "1":
        promptForDetails()
    elif choice == "2":
        print("inside signIn")
        signIn()
    elif choice == "3":
        print("inside admin signIn")
        adminSignIn()
    elif choice == "0":
        print("inside Quit")
        #sys.exit()
        break
    else:
        print("______Invalid Option______")
print("Application Quitted")


    
