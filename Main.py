import cv2
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog


DRAW_COLOR = "#000000"
NO_DRAW_COLOR = "#FFFFFF"

class Base():

    def __init__(self):
        self.app = tk.Tk()
        self.app.geometry("1080x1080")
        self.select = Select()

        self.app.mainloop()

class Select():
    def __init__(self):
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
        self.picross = Picross()

class Picross():
    def __init__(self):
        self.resize_img()
        self.binary_img()
        self.create_picross_widget()
        self.row = []
        self.row_text()
        self.column_text()

    def resize_img(self):
        self.image = cv2.imread(FILE_PATH)
        self.resize_image = cv2.resize(self.image,dsize=[32, 32], interpolation=cv2.INTER_NEAREST)

    def binary_img(self):
        gray_image = cv2.cvtColor(self.resize_image, cv2.COLOR_BGR2GRAY)
        ret2, self.image1 = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)

    def create_picross_widget(self):
        self.create_pic_button()
        self.create_label_button()
        self.create_pic_canvas()
        self.row_number()
        self.column_number()

    def create_pic_button(self):
        self.ans_button = tk.Button(
            height = 2,
            width = 18,
            text = "解答表示",
        )
        self.ans_button.grid(row=0,column=0)
    
    def create_pic_canvas(self):
        global canvas_image1
        self.canvas1 = tk.Canvas(width=200, height=200, background='white')
        self.canvas1.grid(row=1,column=0)
        self.image10 = cv2.imread(FILE_PATH)
        self.re_image = cv2.resize(self.image10,dsize=[200, 200], interpolation=cv2.INTER_NEAREST)
        gray_image = cv2.cvtColor(self.re_image, cv2.COLOR_BGR2GRAY)
        ret2, self.image2 = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)
        cv2.imwrite('/Users/lemon1366/Desktop/Pic/image/resize_image/resize_image.png', self.image2)
        canvas_image1 = tk.PhotoImage(file='/Users/lemon1366/Desktop/Pic/image/resize_image/resize_image.png')
        self.canvas1.create_image(100, 100, image=canvas_image1)

    def create_label_button(self):
        for i in range(32):
            for j in range(32):
                self.grid_label = tk.Label(
                    height = 1,
                    width = 2,
                    bg=NO_DRAW_COLOR,
                    relief=tk.SUNKEN,
                )
                self.grid_label.grid(row=i+2,column=j+2)
    
    def row_number(self):
        global row
        self.row = []
        for i in range(32):
            cnt = 0
            self.before_pixel = None
            self.row_list = []

            for j in range(32):
                self.pixel = self.image1[j,i]
                # print(self.pixel)

                if self.pixel == 0:
                    cnt += 1
                else:
                    if self.before_pixel == 0:
                        self.row_list.append(cnt)
                        cnt = 0

                self.before_pixel = self.pixel

                # if cnt != 0:
                #     self.row_list.append(cnt)
            # print(self.row_list)
            self.row.append(self.row_list)
        print(self.row)

    def column_number(self):
        global column
        self.column = []
        for i in range(32):
            cnt = 0
            self.before_pixel = None
            self.column_list = []

            for j in range(32):
                self.pixel = self.image1[i,j]
                # print(self.pixel)

                if self.pixel == 0:
                    cnt += 1
                else:
                    if self.before_pixel == 0:
                        self.column_list.append(cnt)
                        cnt = 0

                self.before_pixel = self.pixel

                # if cnt != 0:
                #     self.row_list.append(cnt)
            # print(self.row_list)
            self.column.append(self.column_list)
        print(self.column)
    
    def row_text(self):
        for i in range(32):
            self.text = tk.Label(
                # text=self.row[0][i],
                text=i+1,
            )
            self.text.grid(row=i+2,column=0)

    def column_text(self):
        for i in range(32):
            self.text = tk.Label(
                # text=self.column[i][0],
                text=i+1,
            )
            self.text.grid(row=1,column=i+2)

if __name__ == "__main__":
    base = Base()
