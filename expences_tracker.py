from tkinter import *
from tkinter import messagebox
from tkcalendar import *
import datetime
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
root=Tk()
root.geometry("620x600")
root.title("Monthely Expenses calculator")
root.config(bg="#EDC9Af")
#connection with database
conn=sqlite3.connect('monthly_expenses.db')
#create curse
c = conn.cursor()

#insert into table
'''c.execute("""
create table monthlyexp(
catogery text,
date date,
amount integer
)""")'''





#lables
#first label
heading=Label(root,text="Enter the major expenses of everymonth!",font='forte 15 underline',bg="#B87333")
heading.grid(row=0,column=1,padx=10,pady=10)
#catogery dowpdown
option=[
    "Food",
    "Rent",
    "Health",
    "Retirement",
    "Gym ",
    "Funstuff",
    "Others"
]

clicked=StringVar()
clicked.set(option[0])
catogery=OptionMenu(root,clicked,*option)
catogery.config(width=30,font=('times',10))

my_lable=Label(root,text="Catogery",font='times 12 bold',bg="#EDC9Af")
my_lable.grid(row=1,column=0,padx=10,pady=10)
catogery.grid(row=1,column=1,padx=10,pady=10)

#second lable -calander 
#pip intall tkcalendar
calendar=Label(root,text="Calender",font='times 12 bold',bg="#EDC9Af")
calendar.grid(row=2,column=0,padx=10,pady=10)
cal= Calendar(root,selectmode="day",year=2020,month=10,day=30)
cal.grid(row=2,column=1,padx=10,pady=10)

#for amount
Label(root,text="Enter the amount",font="times 12 bold",bg='#EDC9Af').grid(row=3,column=0,padx=10,pady=10)
entry_of_amount=Entry(root)
entry_of_amount.config(width=30)
entry_of_amount.grid(row=3,column=1,padx=10,pady=10)
#create a delete entry
delete_box=Entry(root)
delete_box.grid(row=6,column=1)
delete_lable=Label(root,text="ID of row to delete",font="times 12 bold",bg='#EDC9Af').grid(row=6,column=0,pady=(20,0))







#function
#for submmition
def submit():
    #cleaning the previous values
    
    #connection with database
    conn=sqlite3.connect('monthly_expenses.db')
    #create curse
    c = conn.cursor()
    #checking if the current month is same as new month provided 
    #if not then change the ate of all the rows to the new date
    c.execute('select date from monthlyexp')

    old_date=c.fetchone()
    old_date=old_date[0].split("/")
    
    current_date=cal.get_date().split("/")
    if(old_date[0]!=current_date[0]):
        responce=messagebox.askokcancel(title="Monthly expenses calculator",message="Delete old value and add new month?")
        if(responce==1):
            for i in range(1,8):
                c.execute("update monthlyexp set date=? where oid=?",(cal.get_date(),i))
    
        
    c.execute("UPDATE monthlyexp SET date = ?,amount = ? WHERE catogery=?",(cal.get_date(),entry_of_amount.get(),clicked.get()))
        


    
    #commit changes
    conn.commit()
    #close connection
    conn.close()
    entry_of_amount.delete(0,END)
    
#deleteing the recoeds
def delete_record():
    conn=sqlite3.connect('monthly_expenses.db')

    c = conn.cursor()
    #update the recoed instead o delete because of the pie chart
    c.execute("update monthlyexp set amount=? where catogery=?",(0,clicked.get()))
    
    


    conn.commit()
    
    conn.close()
    delete_box.delete(0,END)
#showing the record
def showing_records():
    #creating new windows to show records
    top=Toplevel()
    top.config(bg="#EDC9Af")
    top.geometry("400x400")
    #connection with database
    conn=sqlite3.connect('monthly_expenses.db')
    #create curse
    c = conn.cursor()
    
    c.execute('select *,oid from monthlyexp')
    
    records=c.fetchall()
    
  
    #heading lable
    Label(top,text="catogery\t\tdate\t\tamount\t\tid").pack()
    for record in records:
        print_variable=''
        print_variable+=str(record[0])+'\t\t'+str(record[1])+"\t\t"+str(record[2])+"\t\t"+str(record[3])+"\n"
        
        Label(top,text=print_variable,bg="#EDC9Af").pack()
    #commit changes
    conn.commit()
    #close connection
    conn.close()
#function for graph
def graph():
    

    #connection with database
    conn=sqlite3.connect('monthly_expenses.db')
    #create curse
    c = conn.cursor()
    
    c.execute('select *,oid from monthlyexp')
    records=c.fetchall()
    value=[]
    i=0
    for record in records:
        value.insert(i,record[2])
        i+=1
    
    plt.pie(value,labels=option,shadow=True, startangle=90,autopct='%1.1f%%')
    plt.show()
    
    c.close()
    
    
        


#buttons
#submit button
submit_btn=Button(root,text="Submit record",command=submit)
submit_btn.config(width=30,font=('times',10))
submit_btn.grid(row=4,column=1,padx=10,pady=50)
#recoed button
show_btn=Button(root,text="Show records",command=showing_records)
show_btn.config(font=('times',10))
show_btn.grid(row=5,column=1)
#create a delete button
delete_btn=Button(root,text="delete record",command=delete_record)
delete_btn.config(font=('times',10))
delete_btn.grid(row=7,column=1,pady=(10,0))
#button for graph
graph_btn=Button(root,text="Show the graph",command=graph)
graph_btn.config(font=('times',10))
graph_btn.grid(row=5,column=3)

#commit changes

conn.commit()
#close connection
conn.close()

root.mainloop()