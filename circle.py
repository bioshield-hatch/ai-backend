
from PIL import Image, ImageFont, ImageDraw

img = Image.open("C:/Users/JamesNorris/Downloads/sark.jpg")
def drawCircles( cleanImage, coordinatesx, coordinatesy, category):
#accepts an image variable, a list of x coords, ycoords, and associated values

    draw = ImageDraw.Draw(cleanImage)
    #initiate the ImageDraw function from PIL

    i = 0
    # get a font
    fnt = ImageFont.truetype("C:/Users/JamesNorris/Documents/python/American Captain.ttf", 40)
    rad = 20
    #initiates some variables so I can change them during testing

    mult = 255/len(coordinatesx)
    #figures out how many items are needed to display so it can make as large a difference in color as possible
    
    for x,y,val in zip(coordinatesx, coordinatesy, category):
    #loop through the list recieved

        draw.circle((x,y), radius=rad, outline=(255,0,int(i*mult)))
        #draws a circle using the x,y values and iterates the color used so a label can be made
        draw.text((x-((len(val)*5)),y+(rad*0.75)), text=val, font=fnt, fill=(255,0,int(i*mult)))
        #labels the circle in the same color
        i += 1
    #return the image with the circles and labels drawn on it
    return cleanImage


finalImage = drawCircles(img, (500, 1200),(900, 700),("shark", "tail"))