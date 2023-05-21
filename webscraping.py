import string
from xml.dom.minidom import Document
import requests
import urllib.request
from bs4 import BeautifulSoup
url = 'https://housing.ucdavis.edu/dining/menus/dining-commons/tercero/'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")




def getMeals(day, meal, soup):
    meals = []
    whatDay = "tab" + str(day) + "content"
    divs = soup.find_all("div", {"id": whatDay})
    theDiv = divs[0].findChildren(recursive=False) #0 will not change, array of length 1
    for span in theDiv[meal].select("span"):#dinner is 2, 3 is dinner, 4 is dinner
        mealString = str(span)
        mealString = mealString.replace("<span>", "")
        mealString = mealString.replace("</span>", "")
        meals.append(mealString)
    return meals

def getMacros(day, meal, soup):
    info = ""
    whatDay = "tab" + str(day) + "content"
    divs = soup.find_all("div", {"id": whatDay})

    #print("yooooooooooooooooooooooooo : " + str(len(divs)))

    theDiv = divs[0].findChildren(recursive=False) #0 will not change, array of length 1
    liCount = 0
    allMacros = []
    for li in theDiv[meal].select("li:not([class])"):#dinner is 2, 3 is dinner, 4 is dinner
        allValues = []
        for p in li.select("p"):
            pString = str(p)
            pString = pString.replace("<p>", "")
            pString = pString.replace("</p>", "")
            pString = pString.replace(": ", "")
            allValues.append(str(pString))
        liCount = liCount + 1
        essentialValueIndices = [0, 1, 2, 3, 4, 5]
        #print("li count: " + str(liCount))
        if len(allValues) >= 6:
            macros = [allValues[i] for i in essentialValueIndices]
            if not any(char.isdigit() for char in macros[0]):
                macros.pop(0)
            else:
                macros.pop(5)
        else:
            essentialValueIndices.pop(5)
            macros = [allValues[i] for i in essentialValueIndices]
        #print("macros: " + str(macros))
        allMacros.append(macros)
    return allMacros

def populateArray(soup):
    allMeals = []
    for dayCount in range(8): #days of the week
        if dayCount != 0:
            #print("doing day: " + str(dayCount))
            for mealCount in range(5): #breakfast lunch or dinner
                if mealCount != 0 and mealCount != 1:
                    #print("doing meal: " + str(mealCount))
                    macros = getMacros(dayCount, mealCount, soup)
                    names = getMeals(dayCount, mealCount, soup)
                    for index in range(len(names)):
                        meal = {
                            "name": names[index],
                            "servingSize": macros[index][0],
                            "cals": macros[index][1],
                            "fat": macros[index][2],
                            "protein": macros[index][3],
                            "carbs": macros[index][4]
                        }
                        allMeals.append(meal)
    uniqueMeals = []
    for meal in allMeals:
        if meal not in uniqueMeals:
            uniqueMeals.append(meal)
    #print(len(uniqueMeals))
    return uniqueMeals
    
def getAllMealsAndMacros():
    diningCommons = ["tercero", "segundo", "cuarto"]
    allMeals = []
    for dc in diningCommons:
        print(dc)
        url = 'https://housing.ucdavis.edu/dining/menus/dining-commons/' + dc + '/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        currentDCMeals = populateArray(soup)
        for meal in currentDCMeals:
            isEmpty = meal.get("servingSize")
            print(isEmpty)
            if isEmpty != "N/A" and isEmpty != "0.00":
                allMeals.append(meal)
            
    print(len(allMeals))
    return allMeals