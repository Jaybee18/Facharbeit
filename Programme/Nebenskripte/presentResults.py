from tkinter import *
from numpy import float64
from .showimage import showImage

class Editor(Tk):
    def __init__(self):
        super().__init__()
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 1000
        self.DEFAULT_PIXEL_SIZE = (20, 20)
        self.informationRight = True
        self.images = []
        self.information = []
        self.additionalImage = []
        self.geometry(str(self.WINDOW_WIDTH) + 'x' + str(self.WINDOW_HEIGHT))
        self.title("Result presentation")
        self.editor = Frame(master=self)
        self.scroll = Frame(master=self.editor)
        self.content = Frame(master=self.editor)

        # create the ui
        # this is the scrollView on the left that holds all the training examples
        # they will be colored red if the model predicted wrong and
        # green if the model was right
        self.scrollBar = Scrollbar(master=self.scroll)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.scrollView = Listbox(master=self.scroll, yscrollcommand = self.scrollBar.set, width=40)
        self.scrollView.bind("<Button-1>", self.itemSelected)
        self.scrollView.pack(side=LEFT, fill=BOTH)
        self.scrollBar.config(command=self.scrollView.yview)
        self.scrollView.selection_set(first=0)

        # create the content on the left
        # the info text is formatted like this:
        # Actual Label : {actual_label}
        # Predicted Label : {predicted_label}
        # after that the testing image is displayed
        self.infoText = StringVar()
        self.infoText.set("penis")
        self.info = Label(master=self.content, textvariable=self.infoText, anchor=W, justify=LEFT)
        self.info.pack(fill=X)
        #self.showAnotherImageButton1 = Button(master=self.content, command=self.showAdditionalImage1, width=20, text="Show another image")
        #self.showAnotherImageButton1.pack(anchor=W)
        self.canvas = Canvas(master=self.content, width=735, height=735)

        # since i can't get the currently selected value in the scrollView in the
        # scrollView select event, i'll bind the mouseButtonUp event to a
        # function that loads the currently selected value from the scrollView
        # (bc this event is called after the selectEvent is finished)
        self.bind("<ButtonRelease-1>", self.loadCorrectInformation)

        # "draw" all widgets into the window
        self.canvas.pack(fill=BOTH, expand=False, side=BOTTOM)
        self.content.pack(fill=BOTH, expand=True, side=RIGHT)
        self.scroll.pack(fill=Y, expand=True)
        self.editor.pack(fill=BOTH, expand=True, side=LEFT)

    def showAdditionalImage1( self ):
        if(self.additionalImage[self.scrollView.curselection()[0]] != None):
            showImage(self.additionalImage[self.scrollView.curselection()[0]][0], isGrayScale=True)

    def newEntry( self , name, image, information, correct, additionalImage=None):
        # here a new result entry is made
        # the needed information to display this result in the content Frame is saved in lists in this object
        # then, the test case is added to the scrollView and the scrollView is updated after this
        self.images.append(image)
        self.information.append(information)
        self.additionalImage.append(additionalImage)
        self.scrollView.insert(END, name)
        self.scrollView.itemconfig(len(self.images)-1, bg='green' if correct else 'red')
        self.scrollView.pack()
        self.scroll.pack()

    def colorToHex( self , color):
        # this converts a color tuple (eg. (255, 243, 75)) into
        # its corresponding hex value (eg. "#fff34b")
        if(type(color) == float64 or type(color) == float):
            color = (color, color, color)
        res = "#"
        for n in color:
            try:
                # image is rgb
                res += hex( n )[ 2: ].rjust(2, '0')
            except TypeError:
                # image is grayscale
                res += hex(int(n*255))[ 2: ].rjust(2, '0')
        return res

    def drawCurrentImage( self ):
        columns, rows = self.getImageDimensions(self.images[self.scrollView.curselection()[0]])
        tile_width, tile_height = self.DEFAULT_PIXEL_SIZE[0], self.DEFAULT_PIXEL_SIZE[1]
        if(tile_width*columns > 735):
            tile_width = 735/columns
        if(tile_height*rows > 735):
            tile_height = 735/rows

        # draws the currently selected image into the canvas
        image = self.images[self.scrollView.curselection()[0]]
        for j in range(rows):
            for i in range(columns):
                self.canvas.create_rectangle(i*tile_width, j*tile_height, i*tile_width+tile_width, j*tile_height+tile_height, fill=self.colorToHex(image[j][i]), width=0)

    def itemSelected( self , event=None):
        # an item was selected, so tell this object that the information
        # displayed in the content Frame is no longer accurate
        self.informationRight = False

    def loadCorrectInformation( self , event=None):
        if self.informationRight == True:
            return
        # load correct information regarding the currently selected test case
        self.infoText.set(self.information[self.scrollView.curselection()[0]])
        self.info.pack(fill=X)
        self.drawCurrentImage()
        self.canvas.pack()
        self.informationRight = True

    def getImageDimensions( self, image ):
        # returns the dimensions of an image (width, height)
        return len( image[ 0 ] ), len( image )

if __name__ == '__main__':
    root = Editor()
    root.mainloop()
