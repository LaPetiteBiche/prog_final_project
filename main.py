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

# Create variables
categories = [
    "Toys & Games", "Clothing, Shoes & Jewelry", "Sports | Outdoors & Fitness",
    "Video Games", "Patio, Lawn & Garden", "Musical Instruments",
    "Tools & Home Improvement", "Electronics | Computers | Accessories"]
categories_final = []
df2 = pd.DataFrame()
df3 = pd.DataFrame()
any_var = "/Users/arthurbonetti/Desktop/chromedriver"

# Import data
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

# Update DataFrame to keep only categories of interest
for i in categories_final:
    temp_df = df[df['Category'] == i]
    df2 = df2.append(temp_df)

# Reset index
df2 = df2.reset_index(drop=True)

# Select 10 random elements
for i in range(10):
    x = random.randint(0, len(df2)-1)
    df3 = df3.append((df2.iloc[[x]]))

# Drop element in main list so that we don't choose them again
for i in df3[[]]:
    df2.drop(i)

# New column df3 for ML
df3['Score'] = 0
df3['Ml_score'] = 0

# Keep info we have to show
var = df3['Image'].values.tolist()
var2 = df3['Name'].values.tolist()
var3 = df3['Price'].values.tolist()

# Create Model with count, image, price, description (and ML score)
class Model(object):
    def __init__(self, img, descr, price):
        self.currentObject = 0
        self.img = img
        self.descr = descr
        self.price = price

# Initialise object
count_object = Model(var[0], var2[0], var3[0])

class Model_df(object):
    def __init__(self, data_f):
        self.data_f = data_f

my_df = Model_df(df3)
# ML -> Compute ML score
def ml_score(df3, df2) :
    dfml = df3[['Price','Net','FBA Fees','LQS','Sellers', 'Rank','Est. Sales',"Est. Revenue","Reviews Count","Rating","Weight","Colors","Sizes"]]
    X = dfml.values
    y = df3['Score'].values
    X_test = df2[['Price','Net','FBA Fees','LQS','Sellers', 'Rank','Est. Sales',"Est. Revenue","Reviews Count","Rating","Weight","Colors","Sizes"]].values
    min_max_scaler = preprocessing.MinMaxScaler()
    min_max_scaler.fit(X_test)
    X = min_max_scaler.transform(X)
    X_test = min_max_scaler.transform(X_test)
    clf = GaussianNB()
    model = clf.fit(X=X, y=y)
    #y_pred = model.predict(X_test)
    #print(y_pred)
    y_proba = model.predict_proba(X_test)[:,1]
    print(y_proba)
    m = np.asarray(y_proba)
    df2["Ml_score"] = m
    plot_mlscore(m)

def update_df3(df3, df2, var, var2, var3) :
    print(df2)
    for i in range(10) :
        x = df2['Ml_score'].idxmax()
        df3 = df3.append(df2.loc[x])
        df2 = df2.drop(x)


    temp = df3['Image'].tail(10).values.tolist()
    temp2 = df3['Name'].tail(10).values.tolist()
    temp3 = df3['Price'].tail(10).values.tolist()

    for i in range(10) :
        var.append(temp[i])
        var2.append(temp2[i])
        var3.append(temp3[i])
    #df3 = df3.iloc[:, :-1]
    df3 = df3.reset_index(drop=True)
    df3['Score'] = df3['Score'].fillna(0)
    my_df.data_f = df3

# Tkinter
# Update window with new infos
def update_tk(var_img, var2, var3, count):
    count.currentObject += 1
    count.img = var_img[count.currentObject]
    count.descr = var2[count.currentObject]
    count.price = var3[count.currentObject]
    im = Image.open(requests.get(count.img, stream=True).raw)
    im = im.resize((400, 400), Image.ANTIALIAS)
    photo = PIL.ImageTk.PhotoImage(image=im)
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    name.config(text=count.descr)
    price.config(text='Price = ' + str(count.price) + ' $')
    window.mainloop()

# When click yes -> Change score to 1
def button_yes():
    my_df.data_f.iloc[count_object.currentObject, -2] = 1
    if (count_object.currentObject + 1) % 10 == 0 :
        ml_score(my_df.data_f,df2)
        update_df3(my_df.data_f,df2,var,var2,var3)

    my_df.data_f.to_csv(f'data/data_prog_image.csv')
    print(my_df.data_f)
    update_tk(var, var2, var3, count_object)

# When click No
def button_no():
    if (count_object.currentObject + 1) % 10 == 0:
        ml_score(my_df.data_f, df2)
        update_df3(my_df.data_f, df2, var, var2, var3)

    print(my_df.data_f)
    update_tk(var, var2, var3, count_object)

def button_stop():
    window.destroy()

def button_buy():
    driver = webdriver.Chrome(executable_path=any_var)
    driver.get(my_df.data_f.iloc[count_object.currentObject, -4])


# 1st initialization window - Image
window = tkinter.Tk()
im = Image.open(requests.get(count_object.img, stream=True).raw)
im = im.resize((400, 400), Image.ANTIALIAS)
photo = PIL.ImageTk.PhotoImage(image=im)
canvas = tkinter.Canvas(window, width=400, height=400)
canvas.pack()
canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

# Labels
name = tkinter.Label(window, text =count_object.descr)
name.pack(anchor=tkinter.CENTER, expand=True)
price = tkinter.Label(window, text ='Price = ' + str(count_object.price) + ' $')
price.pack(anchor=tkinter.CENTER, expand=True)

# Button
btn_yes = tkinter.Button(window, text="Yes", width=50, command=button_yes)
btn_yes.pack(anchor=tkinter.CENTER, expand=True)
btn_no = tkinter.Button(window, text="No", width=50, command=button_no)
btn_no.pack(anchor=tkinter.CENTER, expand=True)
btn_stop = tkinter.Button(window, text="Stop", width=50, command=button_stop)
btn_stop.pack(anchor=tkinter.CENTER, expand=True)
btn_buy = tkinter.Button(window, text="Buy", width=50, command=button_buy)
btn_buy.pack(anchor=tkinter.CENTER, expand=True)
window.mainloop()



