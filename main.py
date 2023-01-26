import cv2
import tkinter as tk
from tkinter import filedialog

DRAW_COLOR = "#000000"
NO_DRAW_COLOR = "#FFFFFF"

IMAGE_WIDTH = 32
IMAGE_HEIGHT = 32

MARK_TEXT = "X"

FONT = ("", 10)

THRESHOLD = 100

class Base():
    def __init__(self):
        self.app = tk.Tk()
        self.app.geometry("880x1080")
        self.app.minsize(880,840)
        self.app.title("PICROSS")
        self.select = Select(self.app)
        self.app.mainloop()

class Select():
    def __init__(self,app):
        self.app = app
        self.create_frame()
        self.create_select_widget()

    def create_frame(self):
            self.frame_0 = tk.Frame(self.app)
            self.frame_0.pack(side=tk.TOP, pady=100)

            self.frame_1 = tk.Frame(self.app)
            self.frame_1.pack(side=tk.TOP)

            self.frame_2 = tk.Frame(self.app)
            self.frame_2.pack(side=tk.TOP)

            self.frame_3 = tk.Frame(self.app)
            self.frame_3.pack(side=tk.TOP)

            self.frame_4 = tk.Frame(self.app)
            self.frame_4.pack(side=tk.TOP)

            self.frame_5 = tk.Frame(self.app)
            self.frame_5.pack(side=tk.TOP)

            self.frame_6 = tk.Frame(self.app)
            self.frame_6.pack(side=tk.TOP)

            self.frame_7 = tk.Frame(self.app)
            self.frame_7.pack(side=tk.TOP)

    def create_select_widget(self):
        self.Picross_OP(self.frame_0) #0
        self.create_button(self.frame_1) #1
        self.create_textbox1(self.frame_2) #2
        self.create_canvas(self.frame_3) #3
        self.create_textbox2(self.frame_4) #4
        self.DOD(self.frame_5) #5
        self.create_textbox3(self.frame_6) #6
        self.create_button1(self.frame_7) #7

    def Picross_OP(self,master):
        global canvas_image1
        self.canvas1 = tk.Canvas(master,width=320, height=60)
        self.canvas1.grid(column=0,row=0)
        canvas_image1 = tk.PhotoImage(file="./image/PICROSS.png")
        self.canvas1.create_image(160, 40, image=canvas_image1)

    def create_button(self,master):
        self.start = tk.Button(
            master,
            height = 2,
            width = 12,
            text = "画像を選択",
            command = lambda:[self.get_path(), self.activation()]
        )
        self.start.grid(column=0,row=0)

    def create_textbox1(self,master):
        self.text1 = tk.Label(
            master,
            text='あなたの選んだ画像',
        )
        self.text1.grid(column=0,row=0)

    def create_canvas(self,master):
        self.canvas = tk.Canvas(master, width=320, height=320,)
        self.canvas.grid(column=0,row=0)

    def get_path(self):
        global canvas_image
        global FILE_PATH
        typ = [('イメージファイル','*.png')] 
        dir = 'C:\\pg'
        FILE_PATH = filedialog.askopenfilename(filetypes = typ, initialdir = dir)
        image = cv2.imread(FILE_PATH)
        self.load_image = cv2.resize(image,dsize=[320, 320],interpolation=cv2.INTER_NEAREST)
        cv2.imwrite('./image/resize_image/resize_image1.png', self.load_image)
        canvas_image = tk.PhotoImage(file='./image/resize_image/resize_image1.png')
        self.canvas.create_image(160, 160, image=canvas_image)

    def create_textbox2(self,master):
        self.text2 = tk.Label(
            master,
            text='==========難易度==========',
        )
        self.text2.grid(column=0,row=0)

    def DOD(self,master):
            self.difficulty1 = tk.Button(
                master,
                height = 3,
                width = 6,
                text = "簡単",
                state="disable",
                command = lambda:[self.select_0(),self.activation_start()]
            )
            self.difficulty1.grid(column=0,row=0)

            self.difficulty2 = tk.Button(
                master,
                height = 3,
                width = 6,
                text = "普通",
                state="disable",
                command = lambda:[self.select_1(),self.activation_start()]
            )
            self.difficulty2.grid(column=1,row=0)

            self.difficulty3 = tk.Button(
                master,
                height = 3,
                width = 6,
                text = "鬼畜",
                state="disable",
                command = lambda:[self.select_2(),self.activation_start()]
            )
            self.difficulty3.grid(column=2,row=0)

    def select_0(self):
        global IMAGE_WIDTH
        global IMAGE_HEIGHT
        IMAGE_WIDTH = IMAGE_HEIGHT = 8

    def select_1(self):
        global IMAGE_WIDTH
        global IMAGE_HEIGHT
        IMAGE_WIDTH = IMAGE_HEIGHT = 16

    def select_2(self):
        global IMAGE_WIDTH
        global IMAGE_HEIGHT
        IMAGE_WIDTH = IMAGE_HEIGHT = 32

    def create_textbox3(self,master):
        self.text3 = tk.Label(
            master,
            text='========================',
        )
        self.text3.grid(column=0,row=0)

    def create_button1(self,master):
        self.start = tk.Button(
            master,
            height = 2,
            width = 12,
            text = "スタート",
            state="disable",
            command = self.new_life
        )
        self.start.grid(column=0,row=0)

    def activation(self):
        self.difficulty1["state"] = "normal"
        self.difficulty2["state"] = "normal"
        self.difficulty3["state"] = "normal"

    def activation_start(self):
        self.start["state"] = "normal"

    def new_life(self):
        self.frame_0.destroy()
        self.frame_1.destroy()
        self.frame_2.destroy()
        self.frame_3.destroy()
        self.frame_4.destroy()
        self.frame_5.destroy()
        self.frame_6.destroy()
        self.frame_7.destroy()
        self.picross = Picross(self.app)

class Picross():
    def __init__(self, app):
        self.app = app
        self.load_image = None
        self.image = None

        self.iamge_width = 0
        self.image_height = 0

        self.row = []
        self.column = []

        self.readImage()
        self.createBinaryImage()
        self.getRowPixels()
        self.getColumnPixels()
        self.createWidgets()
        self.setEvents()

    def readImage(self):
        if len(FILE_PATH) != 0:
            image = cv2.imread(FILE_PATH)
            self.load_image = cv2.resize(
                image,
                dsize=[IMAGE_WIDTH, IMAGE_HEIGHT],
                interpolation=cv2.INTER_NEAREST
            )

    def createBinaryImage(self):
        gray_image = cv2.cvtColor(self.load_image, cv2.COLOR_BGR2GRAY)
        ret, self.image = cv2.threshold(
            gray_image, THRESHOLD, 255,
            cv2.THRESH_BINARY
        )
        self.image_width = self.image.shape[1]
        self.image_height = self.image.shape[0]

    def getRowPixels(self):
        for j in range(self.image_height):
            row_list = []
            before_pixel = None
            count = 0

            for i in range(self.image_width):
                pixel = self.image[j, i]
                if pixel == 0:
                    count += 1
                else:
                    if before_pixel == 0:
                        row_list.append(count)
                        count = 0
                        row_list.append('　')

                before_pixel = pixel

            if count != 0:
                row_list.append(count)

            self.row.append(row_list)

    def getColumnPixels(self):
        for i in range(self.image_width):
            column_list = []
            before_pixel = None
            count = 0

            for j in range(self.image_height):
                pixel = self.image[j, i]
                if pixel == 0:
                    count += 1
                else:
                    if before_pixel == 0:
                        column_list.append(count)
                        count = 0
                        column_list.append('　')

                before_pixel = pixel

            if count != 0:
                column_list.append(count)

            self.column.append(column_list)

    def createWidgets(self):
        self.frame_UL = tk.Frame(self.app,)
        self.frame_UL.grid(column=0, row=0)

        self.frame_UR = tk.Frame(self.app,)
        self.frame_UR.grid(column=1, row=0)

        self.frame_BL = tk.Frame(self.app,)
        self.frame_BL.grid(column=0, row=1)

        self.frame_BR = tk.Frame(self.app,)
        self.frame_BR.grid(column=1, row=1)

        self.createSquares(self.frame_BR)
        self.createVtclAxis(self.frame_BL)
        self.createHztlAxis(self.frame_UR)
        self.createButtons(self.frame_UL)
        self.create_pic_canvas(self.frame_UL)

    def createButtons(self, master):
        self.button_answer = tk.Button(
            master,
            text="解答表示",
            command=self.drawAnswer
        )
        self.button_answer.grid(column=0,row=0)

    def create_pic_canvas(self,master):
        global canvas_image1
        self.canvas1 = tk.Canvas(master,width=200, height=200, background='white')
        self.canvas1.grid(row=1,column=0)
        self.image10 = cv2.imread(FILE_PATH)
        self.re_image = cv2.resize(self.image10,dsize=[200, 200], interpolation=cv2.INTER_NEAREST)
        gray_image = cv2.cvtColor(self.re_image, cv2.COLOR_BGR2GRAY)
        ret2, self.image2 = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)
        cv2.imwrite('./image/resize_image/resize_image.png', self.image2)
        canvas_image1 = tk.PhotoImage(file='./image/resize_image/resize_image.png')
        self.canvas1.create_image(100, 100, image=canvas_image1)

    def createSquares(self, master):
        for j in range(self.image_height):
            for i in range(self.image_width):
                label = tk.Label(
                    master,
                    width=2,
                    height=1,
                    bg=NO_DRAW_COLOR,
                    relief=tk.SUNKEN,
                    font=FONT
                )
                label.grid(column=i, row=j)

    def createVtclAxis(self, master):
        for j in range(self.image_height):
            text = tk.Label(
                master,
                text=self.row[j],
                height=1,
                font=FONT
            )
            text.pack(side=tk.TOP)

    def createHztlAxis(self, master):
        for i in range(self.image_width):
            text = tk.Label(
                master,
                text=self.column[i],
                wraplength=1,
                width=2,
                font=FONT
            )
            text.pack(side=tk.LEFT)

    def setEvents(self):
        for j in range(self.image_height):
            for i in range(self.image_width):
                widgets = self.frame_BR.grid_slaves(column=i, row=j)
                label = widgets[0]
                label.bind("<ButtonPress-1>", self.draw)
                label.bind("<ButtonPress-2>", self.mark)
                label.bind("<Shift-Enter>", self.multiDraw)
                label.bind("<Control-Enter>", self.multiMark)

    def draw(self, event):
        label = event.widget

        if label.cget("text") == MARK_TEXT:
            return

        if label.cget("bg") == NO_DRAW_COLOR:
            label.config(
                bg=DRAW_COLOR,
            )
        else:
            label.config(
                bg=NO_DRAW_COLOR,
            )

    def mark(self, event):
        label = event.widget

        if label.cget("bg") == DRAW_COLOR:
            return

        if label.cget("text") != MARK_TEXT:
            label.config(
                text=MARK_TEXT
            )
        else:
            label.config(
                text=''
            )

    def multiDraw(self, event):
        self.draw(event)

    def multiMark(self, event):
        self.mark(event)

    def drawAnswer(self):
        for j in range(self.image_height):
            for i in range(self.image_width):
                widgets = self.frame_BR.grid_slaves(column=i, row=j)

                if self.image[j, i] == 0:
                    color = DRAW_COLOR
                else:
                    color = NO_DRAW_COLOR

                widgets[0].config(
                    bg=color,
                    text=""
                )

if __name__ == "__main__":
    base = Base()