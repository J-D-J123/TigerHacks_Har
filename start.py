# start.py 
# this starts the main menu

import tkinter as tk
from PIL import Image, ImageTk 

def makeMenu():

    WIDTH   = 500 # 300
    HEIGHT  = 400 # 200

    print("making menu")

    # set up the window 
    root = tk.Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    # root.configure(bg="black")

    # load bg image
    orginalImg   = Image.open("assets/pictures/menuBg.png")
    resizedImg   = resizeImage(orginalImg, WIDTH, HEIGHT)
    photoBgImage = ImageTk.PhotoImage(resizedImg)

    label = tk.Label(root, image=photoBgImage)
    label.place(relwidth=1, relheight=1)

    # create start button 
    startButton = tk.Button(root, text="Start")
    startButton.grid(row=0, column=0, padx=20, pady=20)

    # center the buttons
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0,weight=1)

    root.resizable(False, False)
    root.mainloop()

def resizeImage(image, width, height):
    return image.resize((width, height), Image.LANCZOS) 

def main(): 
    # game loop logic
    makeMenu()

if __name__ == "__main__":
    main()