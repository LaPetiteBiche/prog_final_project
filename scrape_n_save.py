import pandas as pd
import numpy as np
from imgscrape import imgscrape

# Create empty dataframe and give path to chromedriver
df3 = pd.DataFrame()
any_var = "/Users/arthur/Desktop/chromedriver"

# Import raw data
df = pd.read_csv('data/data_prog.csv')

# Cleaning - Deleting info we don't need
df = df.drop("Brand",axis=1)
df = df.drop("Available From",axis=1)
df = df.drop("Seller",axis=1)
df = df.drop("Shipping Weight",axis=1)
df = df.drop("Size",axis=1)
df = df.drop("Oversize",axis=1)
df = df.drop("ASIN",axis=1)
df = df.dropna()

# Scrap function
def scrape_img(lst_var):
    var = imgscrape(*lst_var, path=any_var)
    return(var)

# Iterating over dataframe 10 rows at a time and save image into df
def iter_image(df, df3) :
    x = 10
    while x < df.shape[0] :
        for i in range(x-10,x):
            df3 = df3.append((df.iloc[[i]]))
        lst_var_df = df3['URL']
        lst_var = lst_var_df.values.tolist()
        y = scrape_img(lst_var)
        m = np.asarray(y)
        df3["Image"] = m
        df3.to_csv(f'data/data_prog_{x}.csv')
        x+=10
        df3 = pd.DataFrame()

# Call function
iter_image(df, df3)

# Create variables
x=10
liste = []

# Create a list with all the csv
while x < 890 :
    df = pd.read_csv(f'data/data_prog_{x}.csv')
    liste.append(df)
    x+=10

# Concat the csv and do some additional cleaning -> save the end result
result = pd.concat(liste)
result.to_csv(f'data/data_prog_final.csv')
df = pd.read_csv(f'data/data_prog_final.csv')
df = df.drop(df.columns[0],axis=1)
df = df.drop(df.columns[0],axis=1)
df.to_csv(f'data/data_prog_final.csv')