# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 02:26:11 2020

@author: misra
"""

import sys

"""
Note: I have kept all data as public for simplicity of implementation,
but to protect the bank details, private property is essential

Code supported for testing
"""

class Bank:
    def __init__(self):
        self.CustomerAccounts = {}
        
    def addNewCustomerAccount(self, CustomerID = 99999999, AccNo = 99999999, Pin = 0000, AccountType = "Checking", Value = 0):
        
        AcceptableAccountType = ["Checking", "Saving"]
        
        if len(str(CustomerID)) != 8 or len(str(AccNo)) != 8 or len(str(Pin)) != 4 or AccountType.capitalize() not in AcceptableAccountType:
            raise ValueError('Please enter valid account information')
        else:
            AccountInfo = {AccountType.capitalize(): {"Balance": Value, "AccNo": AccNo}}
            self.CustomerAccounts[CustomerID] = {"Pin":Pin, "AccountInfo": AccountInfo}
            
    def addExistingCustomerAccount(self, CustomerID = 99999999, AccNo = 99999999, AccountType = "Checking", Value = 0):
        
        AcceptableAccountType = ["Checking", "Saving"]
        
        if len(str(CustomerID)) == 8 and len(str(AccNo)) == 8 and AccountType.capitalize() in AcceptableAccountType:
            if AccountType.capitalize() in self.CustomerAccounts[CustomerID]["AccountInfo"]:
                raise ValueError('{} Account exist for this customer'.format(AccountType.capitalize()))
            else:
                # print(AccountType)
                self.CustomerAccounts[CustomerID]["AccountInfo"].update({AccountType.capitalize(): {"Balance": Value, "AccNo": AccNo}})
     
    def updateAccount(self, CusID, AccountType, Value):
        if AccountType.capitalize() in self.CustomerAccounts[CusID]["AccountInfo"]:
            self.CustomerAccounts[CusID]["AccountInfo"][AccountType.capitalize()]["Balance"] = Value
            return True
        else:
            return False
        
    def displayAccount(self, CusID, AccountType = None):
        if CusID in self.CustomerAccounts:
            if AccountType is None:
                print("Displaying Account Information:")
                [print(x, y) for x, y in self.CustomerAccounts[CusID]["AccountInfo"].items()]
                print('\n')
            else:
                if AccountType.capitalize() in self.CustomerAccounts[CusID]["AccountInfo"]:
                    print(self.CustomerAccounts[CusID]["AccountInfo"][AccountType.capitalize()])
                else:
                    print("No existing accounts to show")
            
        else:
            print("Invalid Customer ID")
    
    def verifyPin(self, CusID, PinInput):
        if CusID in self.CustomerAccounts and self.CustomerAccounts[CusID]["Pin"] == PinInput:
            return self.CustomerAccounts[CusID]["AccountInfo"]
        else:
            return None
        
    

class Controller:
    def __init__(self):
        self.ValidPin = False
        
    def cardVerify(self, CusID, Bank):
        
        print("Enter PIN: ", end = ' ')
        Pin = int(input())
        print('\n')
        
        self.Bank = Bank
        self.AccountInfo = Bank.verifyPin(CusID, Pin)
        if self.AccountInfo is None:
            print("Invalid Pin")
        else:
            print("Select Account (Checking/Saving): ")
            UserInput = input()
            self.selectAccount(UserInput, CusID)
            self.ValidPin = True
            
        return self.ValidPin
        
    def selectAccount(self, AccountType, CusID):
        
        AccountType = AccountType.capitalize()
        
        if AccountType in self.AccountInfo:
            print("\n1. Display\n2. Deposit\n3. Withdraw\nEnter Option: ")
            N = int(input())
            print('\n')
            while N not in [1,2,3]:
                print("Please select 1 of the 3 actions [1, 2 or 3]:")
                N = int(input())
                print('\n')
                
            self.performTask(N, AccountType, CusID)
            return True
        else:
            print("Account does not exist")
            return False
        
    def performTask(self, Option, AccountType, CusID):
        if Option == 1:
            print(self.AccountInfo[AccountType])
            return True
        elif Option == 2:
            print("Enter amount to be deposited: ")
            Val = int(input())
            
            NewVal = self.AccountInfo[AccountType]["Balance"] + Val
            
            self.Bank.updateAccount(CusID, AccountType, NewVal)
            print("Updated Account: \n")
            self.Bank.displayAccount(CusID, AccountType)
            return True
        else:
            print("Enter amount to be withdrawn: ")
            Val = int(input())
            
            if Val > self.AccountInfo[AccountType]["Balance"]:
                print("Failed to withdraw amount")
                return False
            else:
                NewVal = self.AccountInfo[AccountType]["Balance"] - Val
            
                self.Bank.updateAccount(CusID, AccountType, NewVal)
                print("Updated Account: \n")
                self.Bank.displayAccount(CusID, AccountType)
                return True
            


if __name__ == "__main__":

    B = Bank()
    B.addNewCustomerAccount(10000001, 12345678, 1234, "Checking", 1000)
    B.addExistingCustomerAccount(10000001, 87654321, "Saving", 1500)
    B.displayAccount(10000001)
    
    # B.addExistingCustomerAccount(10000001, 87654321, "Checking", 1500)
    
    C = Controller()
    C.cardVerify(10000001, B)
    
    # B.displayAccount(10000001)
    
    
    
    
