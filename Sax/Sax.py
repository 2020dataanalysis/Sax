
#   SAX - Sam Personal Tax Assistant
#   Sam Portillo
#   12/15/2019

#   Version 1.0
#   pip install pyinstaller
# 

import os
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import pandas as pd         # pip install pandas
#import numpy as np

root = Tk()
file1 = 'global'
file2 = 'global'

# Create the menubar
menubar = Menu( root )
root.config( menu=menubar)


def get_file1():
    global file1
    file1 = "Chart_Of_Accounts.txt"
    tkinter.messagebox.showinfo('Test', 'Hello !')


def open_expense_file():
    global file1
    file1 = filedialog.askopenfilename()
    label_file1['text'] = file1
    p.set( os.path.dirname(file1) )         # Automatically set the path based on file1



def join():
    chase = pd.read_csv( file1, dtype={7: object}, skiprows = 1 )
    chase.columns.values
    print( chase.info() )
    #print ( chase )

    cnames = ["Details","Posting Date","Description","Amount","Type","Balance","Check","KEY"]
    chase.columns = cnames
    chase['KEY'] = chase['KEY'].fillna(0)

    file_coa = "Chart_Of_Accounts.txt"
    coa = pd.read_csv(file_coa, encoding='latin1', thousands=',')

    for i, row in chase.iterrows():
        for j, row in coa.iterrows():
            if coa.loc[j, 'DESCRIPTION'] in chase.loc[i, 'Description']:
                chase.loc[i, 'KEY'] = coa.loc[j, 'EXPENSE']
                print( i, chase.loc[i, 'KEY'], chase.loc[i, 'Description'], chase.loc[i, 'Amount'] )


    name = os.path.join(p.get(), "dataframe.csv")
    chase.to_csv( name )


    x = chase.groupby(['KEY'])[['Amount']]
    #x = chase.groupby(['KEY']).amount.sum()


    #print ( x )
    y = x.sum()

    key = pd.read_csv( 'Chart_Of_Accounts_Key.txt', encoding='latin1', thousands=',')
    #print( ".")
    e = pd.merge( key, y, how = 'outer', on = 'KEY')

    e['Amount'] = e['Amount'] * -1
    #e.drop(e.columns[[0]], axis=1, inplace=True)
    #e.reset_index()
    column_names = ["KEY", "ACCOUNT", "Amount"]
    #df = e[ column_names ].copy().reset_index()

    #print ( len(df.columns) )
    
    expense_sum = e.query('Amount > 0')
    print( expense_sum )
    name = os.path.join(p.get(), "Expense.csv")
    print ( "Your tax file is saved to the following location:")
    #expense_sum.reset_index()
    print ( name )

    expense_sum.to_csv(name)
    root.destroy()




# Create the submenu
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Sam\'s Tax Assistant', 'This indexes the Chart Of Account reference to your expenses.  Developed by Sam Portillo - 925.705.0592')


def help():
    tkinter.messagebox.showinfo('Help', 'Import tax file with header.\rThis header will be skipped with skiprows.')


def test():
    root.destroy()


# Main
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)
subMenu.add_command(label="Help Me", command=help)

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Tax", command=join)


root.geometry('350x300')
root.title('2019 Tax Assistant')
button1 = Button( text ="Import Expense File", command=open_expense_file ).grid(row=0, column=0, sticky=W)
label_file1 = Label( root, text='?')
label_file1.grid(row=0, column=1, sticky=W)

Label( root, text='Path').grid(row=3, column=0, sticky=W)
p = StringVar()
entry_path = Entry(root, textvariable=p)
p.set('?')
entry_path.grid(row=3, column=1)

root.mainloop()