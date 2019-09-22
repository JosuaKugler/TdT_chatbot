from tkinter import *

class Trump():

    def __init__(self):
        self.canvas = Canvas(root, width = 450, height = 600)      
        self.canvas.grid(column=0,row=0,columnspan=3)           
        self.canvas.create_image(20,20, anchor=NW, image=img)
        self.L = Label(root, text="Question:")
        self.L.grid(column=0,row=2)
        self.E = Entry(root, bd =1, width=65)
        self.E.grid(column=1,row=2,padx=10)
        self.E.bind("<Return>", self.Return)
        self.button = Button( text="Answer", command=self.Return)
        self.button.grid(column=2,row=2,padx=10, pady=20)
        self.text = Text(root, height=9, width=49, padx=40, fg = "red")
        self.text.grid(column=0,row=1,columnspan=3)
        root.mainloop()

    def Return (self, event=None):
        print(self.E.get())

    
root = Tk()
root.title("Artificial stupidity")
photo = PhotoImage(file = "flag.png")
root.iconphoto(False, photo)
img = PhotoImage(file="trump.png") 
Trump()



