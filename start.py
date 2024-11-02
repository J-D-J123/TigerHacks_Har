# start.py 
# this starts the main menu

import tkinter as tk
from PIL import Image, ImageTk 

# import py files 
from Game import Game

def makeMenu():

    # change size to your likeing 
    WIDTH               = 700 # 300 # 500 
    HEIGHT              = 600 # 200 # 400

    # load bg image
    originalImg         = Image.open("assets/pictures/menuBg.png")
    imgWidth            = originalImg.width
    imgHeight           = originalImg.height

    # set up the window 
    root = tk.Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.maxsize(imgWidth, imgHeight)

    photoBgImage = ImageTk.PhotoImage(originalImg)
    label = tk.Label(root, image=photoBgImage)
    label.place(relwidth=1, relheight=1)

    # create start button 
    startButton = tk.Button(root, text="Start", bg="green", fg="white", 
        width=15, height=2, font=("Arial", 14), command=startButtonPressed) # text was size 10 go back?
    startButton.grid(row=0, column=0, padx=20, pady=20)

    # center the buttons
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0,weight=1)

    # code below is for our game name if we have time 
    # text name for game - load picture and put it at the top 
    # gameNameImg             = Image.open("name.png")
    # gameNameTk              = ImageTk.PhotoImage(gameNameImg)
    # gameNameLabel           = tk.Label(root, image = gameNameTk)
    # gameNameLabel.image     = gameNameTk
    # gameNameLabel.place(x   = 5, y = 5)

    # window name and game main loop 
    root.title("Farm Harvester")

    root.mainloop()

def resizeImage(event, original_img, label):
    # return image.resize((width, height), Image.LANCZOS) 

    # resize the origainal image based on the current window size 
    newWidth            = event.width 
    newHeight           = event.height
    resizedImg          = original_img.resize((newWidth, newHeight), Image.LANCZOS)
    photoBgImgResized   = ImageTk.PhotoImage(resizedImg) 

    # update the label for the new img
    label.config(image  = photoBgImgResized)
    label.image         = photoBgImgResized

def startButtonPressed(): 
    print("starting game")
    game = Game()
    game.__init__()
    


def main(): 
    # game loop logic
    makeMenu()

if __name__ == "__main__":
    main()