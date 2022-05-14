#include <bits/stdc++.h>
using namespace std;

class banking_system
{

public:
    string username;
    string account_type;
    long long int account_number;
    long long int amount;

    void user_info()
    {
        cout << "\nName :"<<username;
        cout << "\nCurrent Balance :" << amount;
        cout << "\nAccount Type :" << account_type;
        cout << "\nAccount Number :" << account_number;
        
    }
    void assign()
    {
        cout << "\nEnter Customer's Name:";
        getline(cin,username);
        cout << "\nEnter Account number:";
        cin >> account_number;
        cout << "\nEnter type of account:";
        cin >> account_type;
        cout << "\nEnter amount to deposit:";
        cin >> amount;
    }

    void deposit()
    {
        long long int bal;
        cout << "\nEnter the amount to be deposited:";
        cin >> bal;
        amount += bal;
        cout << "\nThe New Balance is:" << amount;
    }


    void withdraw()
    {
        long long int bal;
        cout << "\nYour balance :" << amount << "\nEnter amount to withdraw:";
        cin >> bal;
        if (bal <= amount)
        {
            amount -= bal;
            cout << "\nRemaining Balance:" << amount;
        }
        else
        {
            cout<<"\nYou don't have enough balace!";
        }
    }

};

int main()
{
    int i;
    banking_system user;
    user.assign();
    cout << "\n1) User Information\n2) Deposit\n3) Withdraw\nEnter your choice:";
    cin >> i;
    if (i == 1)
    {
        user.user_info();
    }
    else if (i == 2)
    {
        user.deposit();
    }
    else if (i == 3)
    {
        user.withdraw();
    }

}
