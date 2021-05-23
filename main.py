import pandas as pd
import numpy as np
import welcome_message
import random
import tkinter
from selenium import webdriver
from PIL import Image
import PIL.ImageTk
import requests
from sklearn import preprocessing
from sklearn.naive_bayes import *
from plot import *

# Create variables and create categories with categories name from dataset
categories = [
    "Toys & Games", "Clothing, Shoes & Jewelry", "Sports | Outdoors & Fitness",
    "Video Games", "Patio, Lawn & Garden", "Musical Instruments",
    "Tools & Home Improvement", "Electronics | Computers | Accessories"]
categories_final = []
df2 = pd.DataFrame()
df3 = pd.DataFrame()

# Path to chromedriver
any_var = "/Users/arthurbonetti/Desktop/chromedriver"

# Import pre processed data from scv
df = pd.read_csv('data/data_prog_final.csv')

# Welcome message + input categories
categories_wanted = str(welcome_message.welcome())

# Save wanted categories in a list
for i in range(0, 9):
    if str(i) in categories_wanted:
        categories_final.append(categories[i - 1])
    else:
        continue

if categories_final == [] :
    for i in range(0, 9):
        categories_final.append(categories[i-1])

# Create new dataframe df2 to keep only categories of interest
for i in categories_final:
    temp_df = df[df['Category'] == i]
    df2 = df2.append(temp_df)

# Reset index
df2 = df2.reset_index(drop=True)

# Select 10 random elements from df2 and save into df3
for i in range(10):
    x = random.randint(0, len(df2)-1)
    df3 = df3.append((df2.iloc[[x]]))

# Drop element in df2 so that we don't choose them again
for i in df3[[]]:
    df2.drop(i)

# New column df3 for ML
df3['Score'] = 0
df3['Ml_score'] = 0

# Keep info we have to show
var = df3['Image'].values.tolist()
var2 = df3['Name'].values.tolist()
var3 = df3['Price'].values.tolist()

# Create Model with count, image, price, description
class Model(object):
    def __init__(self, img, descr, price):
        self.currentObject = 0
        self.img = img
        self.descr = descr
        self.price = price

# Initialise object with first element
count_object = Model(var[0], var2[0], var3[0])

# Object to stock dataframe
class Model_df(object):
    def __init__(self, data_f):
        self.data_f = data_f

# Create object with current df3
my_df = Model_df(df3)

# Function to compute Naive Bayes Classification algorithm
def ml_score(df3, df2) :
    # Columns name we use as X variables
    dfml = df3[['Price','Net','FBA Fees','LQS','Sellers', 'Rank','Est. Sales',"Est. Revenue","Reviews Count","Rating","Weight","Colors","Sizes"]]
    X = dfml.values
    # y is the score value
    y = df3['Score'].values
    # Same variable as before for the test dataset
    X_test = df2[['Price','Net','FBA Fees','LQS','Sellers', 'Rank','Est. Sales',"Est. Revenue","Reviews Count","Rating","Weight","Colors","Sizes"]].values
    # Normalize the data
    min_max_scaler = preprocessing.MinMaxScaler()
    min_max_scaler.fit(X_test)
    X = min_max_scaler.transform(X)
    X_test = min_max_scaler.transform(X_test)
    # initialize the Naive Bayes and fit
    clf = GaussianNB()
    model = clf.fit(X=X, y=y)
    # Compute the probabilities for score
    y_proba = model.predict_proba(X_test)[:,1]
    print(y_proba)
    # Save probabilities in new column and plot
    m = np.asarray(y_proba)
    df2["Ml_score"] = m
    plot_mlscore(m)

# Function to update df3
def update_df3(df3, df2, var, var2, var3) :
    print(df2)
    # Add the 10 elements with biggest predicted values from df2 and remove from df2
    for i in range(10) :
        x = df2['Ml_score'].idxmax()
        df3 = df3.append(df2.loc[x])
        df2 = df2.drop(x)

    # Add the new elements to the list used to show the product
    temp = df3['Image'].tail(10).values.tolist()
    temp2 = df3['Name'].tail(10).values.tolist()
    temp3 = df3['Price'].tail(10).values.tolist()

    for i in range(10) :
        var.append(temp[i])
        var2.append(temp2[i])
        var3.append(temp3[i])

    # Reset index and fill empty score values with 0
    df3 = df3.reset_index(drop=True)
    df3['Score'] = df3['Score'].fillna(0)
    # Update object with new df3
    my_df.data_f = df3

# Tkinter
# Update window with new infos
def update_tk(var_img, var2, var3, count):
    # Update the product count
    count.currentObject += 1
    # Update infos
    count.img = var_img[count.currentObject]
    count.descr = var2[count.currentObject]
    count.price = var3[count.currentObject]
    # Update window
    im = Image.open(requests.get(count.img, stream=True).raw)
    im = im.resize((400, 400), Image.ANTIALIAS)
    photo = PIL.ImageTk.PhotoImage(image=im)
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    name.config(text=count.descr)
    price.config(text='Price = ' + str(count.price) + ' $')
    window.mainloop()

# Function button Yes
def button_yes():
    # Select Score column and update to 1
    my_df.data_f.iloc[count_object.currentObject, -2] = 1
    # Condition for 10 products
    if (count_object.currentObject + 1) % 10 == 0 :
        # Compute classification score and update dataframe
        ml_score(my_df.data_f,df2)
        update_df3(my_df.data_f,df2,var,var2,var3)

    print(my_df.data_f)
    # Update tkinter window
    update_tk(var, var2, var3, count_object)

# Function button No
def button_no():
    # Condition for 10 products
    if (count_object.currentObject + 1) % 10 == 0:
        ml_score(my_df.data_f, df2)
        update_df3(my_df.data_f, df2, var, var2, var3)

    print(my_df.data_f)
    # Update tkinter window
    update_tk(var, var2, var3, count_object)

# Function button stop -> close window
def button_stop():
    window.destroy()

# Function button buy -> open chrome tav to the product URL
def button_buy():
    driver = webdriver.Chrome(executable_path=any_var)
    driver.get(my_df.data_f.iloc[count_object.currentObject, -4])


# 1st initialization tkinter window
window = tkinter.Tk()
# Get product picture from URL
im = Image.open(requests.get(count_object.img, stream=True).raw)
im = im.resize((400, 400), Image.ANTIALIAS)
# Create a PIL object and add to the canvas
photo = PIL.ImageTk.PhotoImage(image=im)
canvas = tkinter.Canvas(window, width=400, height=400)
canvas.pack()
canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

# Create labels
name = tkinter.Label(window, text =count_object.descr)
name.pack(anchor=tkinter.CENTER, expand=True)
price = tkinter.Label(window, text ='Price = ' + str(count_object.price) + ' $')
price.pack(anchor=tkinter.CENTER, expand=True)

# Create buttons
btn_yes = tkinter.Button(window, text="Yes", width=50, command=button_yes)
btn_yes.pack(anchor=tkinter.CENTER, expand=True)
btn_no = tkinter.Button(window, text="No", width=50, command=button_no)
btn_no.pack(anchor=tkinter.CENTER, expand=True)
btn_stop = tkinter.Button(window, text="Stop", width=50, command=button_stop)
btn_stop.pack(anchor=tkinter.CENTER, expand=True)
btn_buy = tkinter.Button(window, text="Buy", width=50, command=button_buy)
btn_buy.pack(anchor=tkinter.CENTER, expand=True)
window.mainloop()



