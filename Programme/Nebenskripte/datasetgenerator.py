from tkinter import *

class Editor(Tk):
    def __init__(self, singleImageMode=False):
        super().__init__()
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 1000
        self.tile_width = 1000 // 32
        self.tile_height = 1000 // 32
        self.isSingleImageMode = singleImageMode
        self.useBooloans = False
        self.drawingColor = (0, 0, 0)
        self.currentLabel = None
        self.wm_title("Tool for generating datasets for Convolutional Neural Networks")
        self.isDrawing = False
        self.currentDrawingColors = [[False if self.useBooloans else (255, 255, 255) for i in range(32)] for i in range(32)]
        self.allDrawingArrays = []
        self.allLabels = []

        # create the window
        self.geometry(str(self.WINDOW_WIDTH) + 'x' + str(self.WINDOW_HEIGHT))
        self.menu = Frame(master=self, height=40, relief=RAISED, borderwidth=2)
        self.editor = Frame(master=self)
        self.canvas = Canvas(master=self.editor, height=self.WINDOW_WIDTH-40)

        # create the label entry
        self.entry_label = Entry(master=self.menu, width=20)
        self.entry_label.place(x=10, y=7)
        self.entry_label.bind('<Return>', self.entryEnterRefreshGrid)
        # width entry
        self.entry_width = Entry(master=self.menu, width=3)
        self.entry_width.insert(0, "32")
        self.entry_width.place(x=160, y= 7)
        self.entry_width.bind('<Return>', self.entryEnterRefreshGrid)
        # height entry
        self.entry_height = Entry(master=self.menu, width=3)
        self.entry_height.insert(0, "32")
        self.entry_height.place(x=190, y=7)
        self.entry_height.bind('<Return>', self.entryEnterRefreshGrid)
        self.xlabel = Label(master=self.menu, text="x")
        self.xlabel.place(x=180, y=7)

        # refresh when 'r' is pressed
        self.bind( 'r', self.refreshGrid)

        # save the current drawing
        self.bind('s', self.saveDrawing)

        # export the current saved images
        self.bind('e', self.export)

        # start drawing when the mousebutton was clicked or is hold down  penis hitler
        self.bind("<Button-1>", self.mouseClick)

        # draw, or not, when the mouse is moved
        self.bind("<Motion>", self.mouseMotion)

        # draw the initial grid
        self.drawGrid()

        # finalize the seperate
        self.menu.pack(fill=X, expand=1)
        self.editor.pack(fill=BOTH, expand=1)

    def saveDrawing( self , event=None):
        if self.focus_get() == self.entry_label or self.focus_get() == self.entry_width or self.focus_get() == self.entry_height:
            return
        # the drawing currently on the canvas is being saved into variables
        self.allDrawingArrays.append(self.currentDrawingColors)
        self.allLabels.append(str(self.entry_label.get()))
        print("saved drawing")

    def mouseMotion( self , event=None):
        if not self.isDrawing:
            return

        x, y = event.x, event.y

        # don't draw, when the mouse is in the menu
        if (not event.widget == self.canvas):
            return

        # calculate the grid position of the mouse
        grid_x = x - x%self.tile_width
        grid_y = y - y%self.tile_height

        self.canvas.create_rectangle(grid_x, grid_y, grid_x+self.tile_width, grid_y+self.tile_height, fill="#000")

        self.currentDrawingColors[int(grid_y//self.tile_height)][int(grid_x//self.tile_width)] = True if self.useBooloans else self.drawingColor

    def mouseClick( self , event=None):
        # toggle whether or not the mouse should be drawing
        # except for when it is in the menu
        if event.y < 40:
            return
        self.isDrawing = not self.isDrawing

    def refreshGrid( self , event=None):
        if self.focus_get() == self.entry_label or self.focus_get() == self.entry_width or self.focus_get() == self.entry_height:
            return
        # the whole canvas is wiped
        self.editor.focus_set()
        self.drawGrid()
        self.currentDrawingColors = [[False if self.useBooloans else (255, 255, 255) for i in range(int(self.WINDOW_WIDTH//self.tile_width))] for i in range(int(self.WINDOW_HEIGHT//self.tile_height))]
        self.currentLabel = str(self.entry_label.get())

    def entryEnterRefreshGrid( self , event=None):
        # wipe the canvas
        self.editor.focus_set()
        self.drawGrid()
        self.currentDrawingColors = [[False if self.useBooloans else (255, 255, 255) for i in range(int(self.WINDOW_WIDTH//self.tile_width))] for i in range(int(self.WINDOW_HEIGHT//self.tile_height))]
        self.currentLabel = str(self.entry_label.get())

    def drawGrid( self ):
        # deletes all objects on the canvas and draws only the grid
        rows = int(self.entry_width.get())
        columns = int(self.entry_height.get())
        width = self.WINDOW_WIDTH
        height = self.WINDOW_HEIGHT-40
        self.canvas.delete("all")
        self.tile_width = width/columns
        self.tile_height = height/rows

        for x in range( rows ):
            for y in range( columns ):
                self.canvas.create_line( x * (width / rows), 0, x * (width / rows), height, width=2 )
                self.canvas.create_line( 0, y * (height / columns), width, y * (height / columns),
                                         width=2 )

        self.canvas.pack(fill=BOTH, expand=1)

    def export( self , event=None):
        if self.focus_get() == self.entry_label or self.focus_get() == self.entry_width or self.focus_get() == self.entry_height:
            return
        if self.isSingleImageMode:
            self.quit()
            return
        # exports the currently saved images into a .dataset file
        filename = str(input("Filename : "))
        file = open(filename+'.dataset', 'w')
        file.write(str(self.allDrawingArrays) + ';' + str(self.allLabels))

        file.close()

    def quit( self ):
        self.destroy()

if __name__ == '__main__':
    root = Editor()
    root.mainloop()