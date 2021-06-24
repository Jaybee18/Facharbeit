import ast
from tkinter import *
from tkinter import filedialog
import os

from keras import datasets
from numpy import float64
from PIL import Image
import math


(t_images, train_labels), (tes_images, test_labels) = datasets.cifar10.load_data()

class Editor(Tk):
    def __init__(self):
        super().__init__()
        self.WINDOW_WIDTH = 710
        self.WINDOW_HEIGHT = 500
        self.image = None #(t_images[1] / 255.0).tolist()  # None
        self.initialImage = None if self.image is None else self.image.copy()
        self.title("Layer simulator")
        self.geometry(str(self.WINDOW_WIDTH) + 'x' + str(self.WINDOW_HEIGHT))
        self.menu = Frame(master=self)
        self.canvas = Canvas(master=self, width=500, height=500)

        # create the menu
        Label(master=self.menu, text="Layer").grid(row=0, column=0)
        self.layerSelector = Spinbox(master=self.menu, values=("Convolution", "Max Pooling", "Average Pooling"), )
        self.layerSelector.grid(row=0, column=1)
        Label(master=self.menu, text="Kernelwidth").grid(row=1, column=0)
        Label(master=self.menu, text="Kernelheight").grid(row=2, column=0)
        self.kernelWidthEntry, self.kernelHeightEntry = Spinbox(master=self.menu, from_=1, to=101), Spinbox(master=self.menu, from_=1, to=101)
        self.kernelWidthEntry.grid(row=1, column=1)
        self.kernelHeightEntry.grid(row=2, column=1)
        Label(master=self.menu, text="Kernel").grid(row=3, column=0)
        self.kernelPreset = Spinbox(master=self.menu, values=("Horizontal", "Vertical", "Diagonal1", "Diagonal2"))
        self.kernelPreset.grid(row=3, column=1)
        Label(master=self.menu, text="Step").grid(row=4, column=0)
        self.stepSize = Spinbox(master=self.menu, from_=1, to=10)
        self.stepSize.grid(row=4, column=1)
        self.samePaddingValue = IntVar()
        self.samePaddingToggle = Checkbutton( master=self.menu, text="Same Padding", variable=self.samePaddingValue )
        self.samePaddingToggle.grid( row=5, column=1 )
        self.applyButton = Button(master=self.menu, text="APPLY LAYER", command=self.applyButton)
        self.applyButton.grid(row=6, column=1)
        self.resetButton = Button(master=self.menu, text="RESET", command=self.resetButton)
        self.resetButton.grid(row=7, column=1)

        self.menu.grid(row=0, column=0, sticky='n')
        self.canvas.grid(row=0, column=1)

        if self.image is None:
            self.loadImage()

        self.drawCurrentImage()

    def convolution( self, image, filter):
        # applies the convolution algorithm to the parameter image
        #
        # The algorithm consists of taking the kernel and moving
        # it along the image. In every step the values "beneath"
        # the kernel are taken and multiplied with their positional
        # corresponding value in the kernel. The products are then
        # taken, summed up and put into a new image.
        #
        # TODO take the kernel- and stepsize from the self.menu
        stepSize = int(self.stepSize.get())
        if filter == 1:
            kernel = [(1, 2, 1), (0, 0, 0), (-1, -2, -1)]
        elif filter == 2:
            kernel = [(-1, 0, 1), (-2, 0, 2), (-1, 0, 1)]
        elif filter == 3:
            kernel = [(1, 0), (0, -1)]
        elif filter == 4:
            kernel = [(0, 1), (-1, 0)]
        newImage = []

        for y in range(len(image)-len(kernel)+1):
            newImage.append([])
            for x in range(len(image[0])-len(kernel)+1):
                res = 0
                for j in range(len(kernel)):
                    for i in range(len(kernel)):
                        one = image[y+j][x+i]
                        two = kernel[j][i]
                        res += one * two
                newImage[-1].append(res)
        return newImage

    def maxpooling( self , image):
        # applies the maxpooling algorithm on the parameter image
        #
        # the algorithm consists of a kernel moving along the image
        # and taking all the values it "covers" and putting
        # the highest value into a new image.
        # That way the image is cropped and de-noised.
        stepSize = int( self.stepSize.get() )
        kernelSize = (int(self.kernelWidthEntry.get()), int(self.kernelHeightEntry.get()))
        newImage = [ ]

        for y in range(0, int((len(image)-kernelSize[0])/stepSize+1)*2 , stepSize):
            newImage.append( [ ] )
            for x in range(0, int((len(image[0])-kernelSize[1])/stepSize+1)*2 , stepSize):
                l = [image[y+i][x+j] for j in range(kernelSize[1]) for i in range(kernelSize[0])]
                res = max(l)
                newImage[ -1 ].append( (res, res, res) )
        return newImage

    def avrPooling( self , image):
        # applies the maxpooling algorithm on the parameter image
        #
        # the algorithm consists of a kernel moving along the image
        # and taking all the values it "covers" and averaging
        # them. The new value is put into a new image.
        # That way the image is cropped.
        stepSize = int( self.stepSize.get() )
        kernelSize = (2, 2)
        newImage = [ ]

        for y in range(0, int((len(image)-kernelSize[1])/stepSize+1) , stepSize):
            newImage.append( [ ] )
            for x in range(0, int((len(image)-kernelSize[1])/stepSize+1) , stepSize):
                l = [ image[ j + y ][ i + x ] for j in range( 2 ) for i in range( 2 ) ]
                res = 0
                for f in l:
                    res += 255-f
                res /= 2*2
                newImage[ -1 ].append( (res, res, res) )
        return newImage

    def applyButton( self ):
        # method that is called when pressing on the apply-button
        # it applies the currently selected layer to
        # the currently displayed image (the image
        # saved in self.image)
        if self.layerSelector.get() == "Convolution":
            if self.samePaddingValue.get() == 1:
                self.increaseImageSize()
            res = self.devideIntoColorChannels()
            r1 = self.applyReLu(self.convolution(res[0], 1))
            g1 = self.applyReLu(self.convolution(res[1], 1))
            b1 = self.applyReLu(self.convolution(res[2], 1))
            image_ho = self.imageFromRGB(r1, g1, b1)
            r2 = self.applyReLu(self.convolution(res[0], 2))
            g2 = self.applyReLu(self.convolution(res[1], 2))
            b2 = self.applyReLu(self.convolution(res[2], 2))
            image_ve = self.imageFromRGB(r2, g2, b2)
            self.image = self.connectImages(image_ho, image_ve)# self.addChannels(image_ho, image_ve)
            self.drawCurrentImage()
        elif self.layerSelector.get() == "Max Pooling":
            res = self.devideIntoColorChannels()
            self.image = self.maxpooling(res[0])
            self.drawCurrentImage()
        elif self.layerSelector.get() == "Average Pooling":
            res = self.devideIntoColorChannels()
            self.image = self.avrPooling(res[0])
            self.drawCurrentImage()

    def resetButton( self ):
        # replaces the currently displayed image
        # with the initially loaded image
        # (reverses all actions taken on that image)
        self.image = self.initialImage
        self.drawCurrentImage()

    def connectImages( self , ho, ve):
        res = []
        for i in range(len(ho)):
            res.append([])
            for j in range(len(ho[0])):
                v = ho[i][j][0]+ve[i][j][0]
                res[-1].append((v, v, v))
        return res

    def applyReLu( self , image):
        # this function applies the ReLu function to a
        # single channel image and returns a new image
        # where the function is applied to every single
        # pixel.
        # The ReLu function returns 0 if the input is
        # negative and the input if it is positive
        res = []
        for i in range(len(image)):
            res.append([])
            for j in range(len(image[i])):
                value = image[i][j]
                if(value < 0):
                    value = 0
                res[-1].append(value)
        return res

    def imageFromRGB( self , r, g, b):
        # creates a rgb image from three separate channels
        # (all channels must have the same dimensions)
        res = [[(r[i][j], g[i][j], b[i][j]) for j in range(len(r[i]))] for i in range(len(r))]
        return res

    def addChannels( self , r, g, b):
        # adds the pixels values of three separate
        # channels (r, g, b) together and
        # creates a grayscale image with the new values
        res = []
        for j in range(len(r)):
            res.append([])
            for i in range(len(r[0])):
                s = r[j][i] + g[j][i] + b[j][i]
                res[-1].append((s, s, s))
        return res

    def increaseImageSize( self ):
        # increases the picture size by adding a border
        # of fillcolor colored pixels (used for same
        # padding in convolutional layers)
        width, height = self.getImageDimensions(self.image)
        fillcolor = (0, 0, 0)
        for i in range(height):
            self.image[i].insert(0, fillcolor)
            self.image[i].append(fillcolor)
        self.image.insert(0, [fillcolor for i in range(width+2)])
        self.image.append([fillcolor for i in range(width+2)])

    def devideIntoColorChannels( self ):
        # returns separate images for each color channel in an rgb image
        r = [[self.image[i][j][0] for j in range(len(self.image[i]))] for i in range(len(self.image))]
        g = [[self.image[i][j][1] for j in range(len(self.image[i]))] for i in range(len(self.image))]
        b = [[self.image[i][j][2] for j in range(len(self.image[i]))] for i in range(len(self.image))]
        return r, g, b

    def colorToHex( self , color):
        # this converts a color tuple (eg. (255, 243, 75)) into
        # its corresponding hex value (eg. "#fff34b")
        #
        # values greater than 255 or lower than 0 are corrected
        # to 255 or 0. But they don't overwrite the image
        # stored in self.image !!
        if(type(color) == float64 or type(color) == float or type(color) == int):
            color = (color, color, color)
        res = "#"
        for n in color:
            try:
                # image is rgb
                if n > 255:
                    n = 255
                res += hex( n )[ 2: ].rjust(2, '0')
            except TypeError:
                # image is grayscale
                if n > 1:
                    n = 1
                res += hex(int(n*255))[ 2: ].rjust(2, '0')
        return res

    def getImageDimensions( self, image ):
        # returns the dimensions of an image (width, height)
        return len( image[ 0 ] ), len( image )

    def convert( self , image, width, height):
        # converts a 2D-array read from an image file wirh PIL.Image.open()
        # into a list, which will be better understood by this program
        res = []
        for j in range(height):
            res.append([])
            for i in range(width):
                res[-1].append(image[i, j])
        return res

    def drawCurrentImage( self ):
        # draws the image, that is currently saved in self.image,
        # onto the canvas. tile_width and "_height are initialised
        # as preferred pixel sizes. When the image gets to large in
        # one dimension with these sizes, the image will be cropped
        # to fit and the preferred pixel size will be ignored
        columns, rows = self.getImageDimensions(self.image)
        print(columns, rows)
        tile_width, tile_height = 100000, 100000
        if(tile_width*columns > 500):
            tile_width = 500/columns
        if(tile_height*rows > 500):
            tile_height = 500/rows

        # draws the currently selected image into the canvas
        for j in range(rows):
            for i in range(columns):
                self.canvas.create_rectangle(i*tile_width, j*tile_height, i*tile_width+tile_width, j*tile_height+tile_height, fill=self.colorToHex(self.image[j][i]), width=0)

    def loadImage( self ):
        # let the user browse for files he wants to open
        # they can be .dataset files created by the datasetgenerator.py script
        # or .png, .jpg, etc. files
        # Bigger images will load a lot longer than smaller images !!
        filename = filedialog.askopenfilename( initialdir=os.curdir, title="Select image", filetypes=(("Dataset files", "*.dataset"), ("all files", "*.*")) )
        file = open(filename, 'r')
        try:
            content = file.read()
            file.close()
            image = ast.literal_eval( content[ :content.index( ';' ) ] )
            if type( image[ 0 ][ 0 ] ) != tuple:
                self.image = image[ 0 ]
            else:
                self.image = image
            print("loaded file with open")
        except UnicodeDecodeError:
            file.close()
            # load the image file with PIL, because its not a dataset file
            raw = Image.open(filename)
            img = raw.load()
            self.image = self.convert(img, raw.size[0], raw.size[1])
            print("loaded file with PIL.Image")
        self.initialImage = self.image


if __name__ == '__main__':
    root = Editor()
    root.mainloop()