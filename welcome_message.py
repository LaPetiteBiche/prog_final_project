
# Welcome message function that return the input
def welcome():
    print("Welcome to the gift selector !")
    print("------------------------------")
    print("We have 8 gift categories, please select the categories that you are interested in.")
    print("------------------------------")
    print("1. Toys and Games, 2. Clothing, Shoes and Jewelry, 3. Sports, outdoor and Fitness, 4. Video Games")
    print(", 5.Patio, Lawn and Garden, 6. Musical Instrument, 7.Tools and Home, 8. Electronics")
    category = input("Please type the numbers of the categories (eg:12378)")
    return(category)

