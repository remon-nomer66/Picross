import cv2
import tkinter as tk
from tkinter import filedialog


DRAW_COLOR = "#000000"
NO_DRAW_COLOR = "#FFFFFF"

MARK_TEXT = "X"

THRESHOLD = 100

class Base():

    def __init__(self):
        self.app = tk.Tk()
        self.app.geometry("1080x1080")
        self.select = Select(self.app)

        self.app.mainloop()

class Select():
    def __init__(self,app):
        self.app = app
        self.create_select_widget()

    def create_select_widget(self):
        self.create_button()
        self.create_textbox()
        self.create_canvas()

    def create_button(self):
        self.start = tk.Button(
            height = 2,
            width = 6,
            text = "画像を選択",
            command = self.get_path
        )
        self.start.pack()

    def get_path(self):
        global canvas_image
        global FILE_PATH
        typ = [('イメージファイル','*.png')] 
        dir = 'C:\\pg'
        FILE_PATH = filedialog.askopenfilename(filetypes = typ, initialdir = dir)
        canvas_image = tk.PhotoImage(file=FILE_PATH)
        self.canvas.create_image(640/2, 640/2, image=canvas_image)

        self.start2 = tk.Button(
            height = 2,
            width = 6,
            text = "スタート",
            command = self.new_life
        )
        self.start2.pack()

    def create_textbox(self):
        self.text = tk.Label(
            text='あなたの選んだ画像',
        )
        self.text.pack()

    def create_canvas(self):
        self.canvas = tk.Canvas(width=640, height=640,background='white')
        self.canvas.pack()

    def new_life(self):
        self.start.destroy()
        self.start2.destroy()
        self.text.destroy()
        self.canvas.destroy()
        self.picross = Picross(self.app)

class Picross():
    def __init__(self,app):
        self.column = []
        self.row = []

        self.create_frame(app)
        self.resize_img()
        self.binary_img()
        self.create_picross_widget()

    def create_frame(self,app):

        #写真表示
        self.frame_MM = tk.Frame(app)
        self.frame_MM.grid(column=0,row=0)
 
        #横の数字表示
        self.frame_MR = tk.Frame(app)
        self.frame_MR.grid(column=1,row=0)

        #縦向きの数字表示
        self.frame_BM = tk.Frame(app)
        self.frame_BM.grid(column=0,row=1)

        #ピクロス
        self.frame_BR = tk.Frame(app)
        self.frame_BR.grid(column=1,row=1)

    def resize_img(self):
        self.image = cv2.imread(FILE_PATH)
        self.resize_image = cv2.resize(self.image,dsize=[32, 32], interpolation=cv2.INTER_NEAREST)

    def binary_img(self):
        gray_image = cv2.cvtColor(self.resize_image, cv2.COLOR_BGR2GRAY)
        ret2, self.image1 = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)

    def create_picross_widget(self):

        self.create_label_button(self.frame_BR)
        self.create_pic_canvas(self.frame_MM)

        self.row_text(self.frame_MR)
        self.row_number()
        
        self.column_text(self.frame_BM)
        self.column_number()
    
    def create_pic_canvas(self,master):
        global canvas_image1
        self.canvas1 = tk.Canvas(master,width=200, height=200, background='white')
        self.canvas1.grid(row=1,column=0)
        self.image10 = cv2.imread(FILE_PATH)
        self.re_image = cv2.resize(self.image10,dsize=[200, 200], interpolation=cv2.INTER_NEAREST)
        gray_image = cv2.cvtColor(self.re_image, cv2.COLOR_BGR2GRAY)
        ret2, self.image2 = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)
        cv2.imwrite('/Users/lemon1366/Desktop/Pic/image/resize_image/resize_image.png', self.image2)
        canvas_image1 = tk.PhotoImage(file='/Users/lemon1366/Desktop/Pic/image/resize_image/resize_image.png')
        self.canvas1.create_image(100, 100, image=canvas_image1)

    def create_label_button(self,master):
        for j in range(32):
            for i in range(32):
                self.grid_label = tk.Label(
                    master,
                    height = 1,
                    width = 2,
                    bg=NO_DRAW_COLOR,
                    relief=tk.SUNKEN,
                )
                self.grid_label.grid(column=i,row=j)
    
    def row_number(self):
        for i in range(32):
            cnt = 0
            self.before_pixel = None
            row_list = []

            for j in range(32):
                self.pixel = self.image1[i,j]

                if self.pixel == 0:
                    cnt += 1
                else:
                    if self.before_pixel == 0:
                        row_list.append(cnt)
                        cnt = 0

                self.before_pixel = self.pixel

            self.row.append(row_list)

    def column_number(self):
        for i in range(32):
            cnt = 0
            self.before_pixel = None
            column_list = []

            for j in range(32):
                self.pixel = self.image1[j,i]

                if self.pixel == 0:
                    cnt += 1
                else:
                    if self.before_pixel == 0:
                        column_list.append(cnt)
                        cnt = 0

                self.before_pixel = self.pixel

            self.column.append(column_list)
    
    def row_text(self,master):
        for j in range(32):
            self.text = tk.Label(
                master,
                text = self.row[j],
                height=1,
            )
            self.text.pack(side=tk.TOP)

    def column_text(self,master):
        for i in range(32):
            self.text = tk.Label(
                master,
                text = self.column[i],
                wraplength=1,
                width=2,
            )
            self.text.pack(side=tk.LEFT)

    def setEvents(self):
        for j in range(32):
            for i in range(32):

                # gridへの配置場所からウィジェット取得
                widgets = self.frame_BR.grid_slaves(row=i,column=j)
                label = widgets[0]

                # 左クリック時のイベント設定
                label.bind("<ButtonPress-1>", self.draw)

                # 右クリック時のイベント設定
                label.bind("<ButtonPress-2>", self.mark)

    def draw(self,event):

        label = event.widget

        if label.cget("text") == MARK_TEXT:
            return
        
        if label.cget("text") != MARK_TEXT:
            label.config(
                text=''
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

if __name__ == "__main__":
    base = Base()
