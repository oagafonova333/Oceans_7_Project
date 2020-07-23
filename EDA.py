 # FUNCTIONS
import datetime
import numpy as np
from datetime import date
import matplotlib.pyplot as plt

def f_protected (x, i= 0):
    """
    Create, in your library/module, a protected function called 'f_protected' that creates a lambda function.
    The lambda function must receive a param 'x' and return a boolean True if 'x' is higher than 5.
    Also, 'f_protected' must create a list ('l1') with 'list comprehesion' that generates a list from 0 to 15. 
    Finally, 'f_protected' must return 'l1' filtered (using function 'filter') using the lambda function.
    After that, create a decorator called "prepost". The decorator must receive an *args and a **kwargs argument.
    If in 'kwargs' there is a key called "url", then it must do the next:
            1. Open with a pandas the url as 'csv'. The variable is called 'df'.
            2. Do what normal function does (the function wrapped with the decorator).
            3. Plot histograms of each column in 'df'.
    """
    filter_f = lambda x: True if len(x) > 5 else False
    l1=[{(yield i) for i in range(15)}]
    
    return filter_f(x = l1)

def general_info (df):
    """
                        ---What it does--
    This function checks the info, columns and shape of the df, printing them. Also it checks the presence of NaNs values on the df and prints them in case it founds them.

                        ---What it needs---
    A df object
    """

    # df columns info
    print('-dtype, length and name of columns-')
    print(df.info())
    print()
    print(df.columns)
    print()
    print(df.shape)
    print()

    # Presence of NaNs in df
    need_to_print =  False
    nulls = df.isnull().any()
    print('-Presence of NaNs in df-')
    print (nulls)
    for e in list(nulls):
        if e == True:
            need_to_print = True
    if need_to_print == True:
        print()
        print('-Number of NaNs in df-')
        print (df.isnull().sum() )

def time_indexer (df):
    """
                        What it does
    Groups your data by the time scale that you want (Year, Month, Day...) creating a new column in the process

                        What it needs
    A dataframe and your input
    """
    t_input = input("Select time scale (year, week, day). Please type this as given here>")
    if t_input == "year":
        df['year'] = df.index.year
    elif t_input == "month":
        df['month'] = df.index.month
    elif t_input == "day":
        df['day'] = df.index.day

def df_save (df):
    """
                        ---What it does---
    Saves your df of choice to a .csv file in the same directory of the parent file

                        ---What it needs---
    * Your input for the name (be careful with adding spaces)
    * Your ready-to-save df
    """
    name = input("Type the name of your df> ")
    name = name + ".csv"
    df.to_csv(name, sep = ',')

def null_count (df):
    """
                        ---What it does---
    Identifies and counts the number of null values in any given df. Does not return anything.

                        ---What it needs---
    A DataFrame
    """
    null_in_df = df.isnull().any()
    is_null = df.isnull().sum()
    print (f'Presence of null in clolumns:\n{null_in_df}\n\nNumber of null in columns:\n{is_null}')



def value_counter(df):
    """
                        ---What it does---
    Counts the values of all columns of a given df and prints them in succesion.
                        ---What it needs---
    A df object
    """
    for e in df.columns:
        print(f"\n{e}:\n{df[e].value_counts()}")
        print('----------------')
       
def counter(counter):
    """
    ---What it does---
    Counter system to show progress of function
    """
    counter += 1
    sys.stdout.write("\r {0} %".format(counter))
    sys.stdout.flush()

def test():
    print('EDA lib ready')
test()

                                    # LAMBDAS

# Gender transforms data into genders (male/female)
gender = lambda x: "Female" if x == 1 else ("Male" if x == 2 else x)

                                    # GRÁFICOS

def plot_bar(df_column, save_image = 0):
    """
                        ---What it does---
    Plots a barplot with the variable given. And if desired, saves the plot in the same directory as parent file with "<current date>_barplot.jpg" as name.
                        ---What it needs---
    A df_column, panda series or dictionary with numerical values
                        ---What it returns---
    If desired (save_image != 0), a jpg image file in the same directory using "<current date>_barplot.jpg" as name.
    """
    if df_column.sum() > 0:
        df_column.plot(kind = 'bar')
        if save_image != 0:
            name = str(date.today()) + '_barplot.jpg'
            plt.savefig(name)
    else:
        print(f'No numeric data to plot')

def plot_line(df_column, save_image = 0):
    """
                        ---What it does---
    Plots a lineplot with the variable given. And if desired, saves the plot in the same directory as parent file with "<current date>_lineplot.jpg" as name.
                        ---What it needs---
    A df_column, panda series or dictionary with numerical values
                        ---What it returns---
    If desired (save_image != 0), a jpg image file in the same directory using "<current date>_lineplot.jpg" as name.
    """
    if df_column.sum() > 0:
        df_column.plot()
        if save_image != 0:
            name = str(date.today()) + '_lineplot.jpg'
            plt.savefig(name)
    else:
        print(f'No numeric data to plot')

def plot_pie(df_column, save_image = 0):
    """
                        ---What it does---
    Plots a pieplot with the variable given. And if desired, saves the plot in the same directory as parent file with "<current date>_pieplot.jpg" as name.
                        ---What it needs---
    A df_column, panda series or dictionary with numerical values
                        ---What it returns---
    If desired (save_image != 0), a jpg image file in the same directory using "<current date>_pieplot.jpg" as name.
    """
    if df_column.sum() > 0:
        data = df_column
        # Create lables
        labels = dict(df_column).keys()

        # Plot pie chart
        plt.pie(data, autopct='%1.1f%%', startangle=0, shadow= True, pctdistance = 0.5, labeldistance = 1.2)

        # Legend and titles
        plt.legend(labels, loc= 'best')
        plt.title(df_column.name, loc='center')

        plt.tight_layout()
        plt.show()
        
        if save_image != 0:
            name = str(date.today()) + '_pieplot.jpg'
            plt.savefig(name)
    else:
        print ("No numeric data to plot")