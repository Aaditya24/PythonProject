create database bankSystem;
use bankSystem;
create table customers(
						Customer_Id varchar(10) primary key,
                        Password varchar(12),
                        name varchar(15), /*Name field is added*/
                        Address varchar(10),
                        Pan varchar(10),
                        Mobile varchar(10),
                        DOB date
						);
drop table customers;
alter table customers add column name varchar(15) after Password;
select * from customers;

create table accounts(
					Account_no varchar(10) primary key,
					Customer_Id varchar(12),
					Balance long,
					Account_Type varchar(10),
					check (Account_Type = "saving" or Account_Type = "current" or Account_Type = "fdaccount"),
					Account_creation_Date date,
					foreign key (Customer_Id) references customers(Customer_Id) ON DELETE CASCADE
                        );
drop table accounts;
desc account1s;
select * from accounts;


create table transactions(
							Transaction_Id varchar(10) primary key,
                            Date_Of_Transaction date,
                            From_Account varchar(10),
                            To_Account varchar(10),
                            Type_Of_Transaction varchar(10),
                            check (Type_Of_Transaction = "deposit" or Type_Of_Transaction = "withdraw" or Type_Of_Transaction = "transfer"),
                            Amount long,
                            foreign key (From_Account) references accounts(Account_no) ON DELETE CASCADE,
                            foreign key (To_Account) references accounts(Account_no) ON DELETE CASCADE
                            );
drop table transactions;
desc transactions;
select * from transactions;

create table fixedAccount (
						   Fd_Account_No varchar(10) primary key,
                           Customer_Id varchar(10),
                           Amount long,
                           Term int,
                           Return_Amount long,
                           foreign key (Customer_Id) references customers(Customer_Id) ON DELETE CASCADE
							);
select * from fixedAccount;
drop table fixedAccount;
desc fixedaccount;


create table loans (
					Loan_Account_No varchar(10) primary key,
                    Customer_Id varchar(10),
                    Amount long,
                    Repayment_Term int,
                    Return_Amount long,
                    Repayment_TermWise_Amount long,
                    foreign key (Customer_Id) references customers(Customer_Id) ON DELETE CASCADE
                    );
select * from loans;
drop table loans;

create table admins (
						Admin_Id varchar(10) primary key,
                        password varchar(12),
                        Admin_Name varchar(15),
                        Address varchar(15),
                        Email varchar(15),
                        Mobile long
                        );
select * from admins;
drop table admins;


create table ClosedAccounts (
							Account_no varchar(10),
                            Account_Type varchar(10),
                            Date_Of_Closure date
                            );
select * from closedAccounts;
drop table ClosedAccounts;