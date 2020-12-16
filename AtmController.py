# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 02:26:11 2020

@author: misra

Code supported for testing
Note: The controller does not have access to Bank PIN
"""

class Bank:
    def __init__(self):
        self.CustomerAccounts = {}
        self.__AccountVerification = {}
        
    def addNewCustomerAccount(self, CustomerID = 99999999, AccNo = 99999999, Pin = 0000, AccountType = "Checking", Value = 0):
        
        AcceptableAccountType = ["Checking", "Saving"]
        
        if len(str(CustomerID)) != 8 or len(str(AccNo)) != 8 or len(str(Pin)) != 4 or AccountType.capitalize() not in AcceptableAccountType:
            raise ValueError('Please enter valid account information')
        else:
            AccountInfo = {AccountType.capitalize(): {"Balance": Value, "AccNo": AccNo}}
            self.CustomerAccounts[CustomerID] = {"AccountInfo": AccountInfo}
            self.__AccountVerification[CustomerID] = {"Pin":Pin}
            
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
            self.CustomerAccounts[CusID]["AccountInfo"][AccountType.capitalize()]["Balance"] += Value
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
        if CusID in self.__AccountVerification and self.__AccountVerification[CusID]["Pin"] == PinInput:
            return True
        else:
            return False
        
    

class Controller:
    def __init__(self):
        self.ValidPin = False
        
    def cardSwipe(self, CusID, Bank):
        
        print("Enter PIN: ", end = ' ')
        Pin = int(input())
        print('\n')
        
        self.Bank = Bank
        
        IsValidPin = Bank.verifyPin(CusID, Pin)
        if not IsValidPin:
            print("Invalid PIN")
        else:
            print("Select Account:\n1.Checking\n2.Saving")
            UserInput = int(input())
            while UserInput not in [1,2]:
                print("\nPlease select a valid account:")
                UserInput = int(input())
                
            self.selectAccount(UserInput, CusID)
            self.ValidPin = True
            
        return self.ValidPin
        
    def selectAccount(self, AccountSelection, CusID):
        
        if AccountSelection == 1:
            AccountType = "Checking"
        elif AccountSelection == 2:
            AccountType = "Saving"
            
        if AccountType in self.Bank.CustomerAccounts[CusID]["AccountInfo"]:
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
            self.Bank.displayAccount(CusID, AccountType)
            return True
        elif Option == 2:
            print("Enter amount to be deposited: ")
            Val = int(input())
            
            self.Bank.updateAccount(CusID, AccountType, Val)
            print("\nUpdated {} Account:\n".format(AccountType))
            self.Bank.displayAccount(CusID, AccountType)
            return True
        else:
            print("Enter amount to be withdrawn: ")
            Val = int(input())
            
            BankBalance = self.Bank.CustomerAccounts[CusID]["AccountInfo"][AccountType]["Balance"]
            
            if Val > BankBalance:
                print("Failed to withdraw amount")
                return False
            else:
            
                self.Bank.updateAccount(CusID, AccountType, -1*Val)
                print("\nUpdated {} Account:\n".format(AccountType))
                self.Bank.displayAccount(CusID, AccountType)
                return True
            


if __name__ == "__main__":

    B = Bank()
    B.addNewCustomerAccount(10000001, 12345678, 1234, "Checking", 1000)
    B.addExistingCustomerAccount(10000001, 87654321, "Saving", 1500)
    B.displayAccount(10000001)
    
    # Validating that 2 same accounts cannot exist under the same customer
    # B.addExistingCustomerAccount(10000001, 87654321, "Checking", 1500)
    
    C = Controller()
    C.cardSwipe(10000001, B)
    
    # Display all information pertaining to a customer
    # print('\n')
    # B.displayAccount(10000001)
    
    
    
    
