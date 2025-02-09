from menu import Menu,MenuItem

menuItems = []
menuItems.append(MenuItem("Planets", "The Planets", 0, 0, 0, 0))
menuItems.append(MenuItem("Satellites", "The ISS, Moon etc", 0, 0, 0, 0))
menuItems.append(MenuItem("Constellations blah blah blah", "The big dipper, orion etc", 0, 0, 0, 0))
menuItems.append(MenuItem("Stars", "Polarus,Betelgeuse , Sirus etc", 0, 0, 0, 0))

print(len(menuItems))

topMenu= Menu(isI2C=True,itemList=menuItems)
topMenu.showMenu()