import tkinter
import cv2
from tkinter import filedialog

# 読み込ませる画像のファイルパス
FILE_PATH = "image/image1.png"

# 画像のサイズ
IMAGE_WIDTH = 32
IMAGE_HEIGHT = 32

# 色設定
DRAW_COLOR = "#000000"
NO_DRAW_COLOR = "#FFFFFF"

# 印を表すテキスト
MARK_TEXT = "X"

# フォント
FONT = ("", 10)

# 白黒化時の閾値
THRESHOLD = 100

class Select():
    def __init__(self,app):
        self.app = app
        self.create_select_widget()

    def create_select_widget(self):
        self.create_button()
        self.create_textbox()
        self.create_canvas()

    def create_button(self):
        self.start = tkinter.Button(
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

        self.start2 = tkinter.Button(
            height = 2,
            width = 6,
            text = "スタート",
            command = self.new_life
        )
        self.start2.pack()

    def create_textbox(self):
        self.text = tkinter.Label(
            text='あなたの選んだ画像',
        )
        self.text.pack()

    def create_canvas(self):
        self.canvas = tkinter.Canvas(width=640, height=640,background='white')
        self.canvas.pack()

    def new_life(self):
        self.start.destroy()
        self.start2.destroy()
        self.text.destroy()
        self.canvas.destroy()
        self.picross = Picross(self.app)


class Picross():
    def __init__(self, app):
        self.file_path = FILE_PATH
        self.load_image = None

        # 白黒化した画像オブジェクト
        self.image = None

        # 画像のサイズ
        self.iamge_width = 0
        self.image_height = 0

        # 各行に対して塗り潰すマス数のリスト
        self.row = []

        # 各列に対して塗り潰すマス数のリスト
        self.column = []

        # 画像を読み込む
        self.readImage()

        # 画像を白黒化する
        self.createBinaryImage()

        # 塗りつぶすマス数を取得する
        self.getRowPixels()
        self.getColumnPixels()

        # ウィジェットを作成する
        self.createWidgets()

        # イベント処理を設定する
        self.setEvents()

    def readImage(self):
        '画像を読み込む'

        if len(self.file_path) != 0:

            # ファイルを開いて読み込む
            image = cv2.imread(self.file_path)

            # 画像のリサイズ
            self.load_image = cv2.resize(image,dsize=[IMAGE_WIDTH, IMAGE_HEIGHT],interpolation=cv2.INTER_NEAREST
            )

    def createBinaryImage(self):
        '画像を白黒化する'

        # 画像をグレースケール化
        gray_image = cv2.cvtColor(self.load_image, cv2.COLOR_BGR2GRAY)

        # 画像を白黒化（閾値は自動設定）
        ret, self.image = cv2.threshold(
            gray_image, THRESHOLD, 255,
            cv2.THRESH_BINARY
        )

        # 画像のサイズを取得
        self.image_width = self.image.shape[1]
        self.image_height = self.image.shape[0]

    def getRowPixels(self):
        '各行の塗りつぶすマス数を取得'

        # 各行に対するループ
        for j in range(self.image_height):

            # 行単位でリストを作成
            row_list = []

            # 行単位でカウント等を初期化
            before_pixel = None
            count = 0

            # 行内に対するループ
            for i in range(self.image_width):

                # ピクセルの色を取得
                pixel = self.image[j, i]

                # 塗り潰すべきマスがいくつ連続しているかをカウント
                if pixel == 0:
                    count += 1
                else:
                    # 塗り潰すべきマスが途切れた場合
                    if before_pixel == 0:

                        # リストにカウントした数を追加
                        row_list.append(count)
                        count = 0

                        # 区切りが分かるように全角スペースも追加
                        row_list.append('　')

                # 前のピクセルの情報を覚えておく
                before_pixel = pixel

            # 1行分カウントが終わったらリストに最後に追加
            if count != 0:
                row_list.append(count)

            # １行分のリストを全行分管理するリストに追加
            self.row.append(row_list)

    def getColumnPixels(self):
        '各行の塗りつぶすマス数を取得'

        # 各列に対するループ
        for i in range(self.image_width):

            # 列単位でリストを作成
            column_list = []

            # 列単位でカウント等を初期化
            before_pixel = None
            count = 0

            # 列内に対するループ
            for j in range(self.image_height):

                # ピクセルの色を取得
                pixel = self.image[j, i]

                # 塗り潰すべきマスがいくつ連続しているかをカウント
                if pixel == 0:
                    count += 1
                else:
                    # 塗り潰すべきマスが途切れた場合
                    if before_pixel == 0:

                        # リストにカウントした数を追加
                        column_list.append(count)
                        count = 0

                        # 区切りが分かるように全角スペースも追加
                        column_list.append('　')

                # 前のピクセルの情報を覚えておく
                before_pixel = pixel

            # 1列分カウントが終わったらリストに最後に追加
            if count != 0:
                column_list.append(count)

            # １列分のリストを全列分管理するリストに追加
            self.column.append(column_list)

    def createWidgets(self):
        '各種ウィジェットを作成・配置するメソッド'

        # 左上のフレームを作成・配置
        self.frame_UL = tkinter.Frame(
            self.app,
        )
        self.frame_UL.grid(column=0, row=0)

        # 右上のフレームを作成・配置
        self.frame_UR = tkinter.Frame(
            self.app,
        )
        self.frame_UR.grid(column=1, row=0)

        # 左下のフレームを作成・配置
        self.frame_BL = tkinter.Frame(
            self.app,
        )
        self.frame_BL.grid(column=0, row=1)

        # 右下のフレームを作成・配置
        self.frame_BR = tkinter.Frame(
            self.app,
        )
        self.frame_BR.grid(column=1, row=1)

        # マスを右下のフレーム上に作成
        self.createSquares(self.frame_BR)

        # 縦軸を左下のフレーム上に作成
        self.createVtclAxis(self.frame_BL)

        # 横軸を右上のフレーム上に作成
        self.createHztlAxis(self.frame_UR)

        # ボタンを左上のフレームに作成
        self.createButtons(self.frame_UL)

    def createButtons(self, master):
        'ボタンを作成'

        # 解答表示用のボタンの作成・配置
        self.button_answer = tkinter.Button(
            master,
            text="解答表示",
            command=self.drawAnswer
        )
        self.button_answer.pack()

    def createSquares(self, master):
        'マスと見立てたラベルを作成'

        for j in range(self.image_height):
            for i in range(self.image_width):

                # ラベルウィジェットを作成
                label = tkinter.Label(
                    master,
                    width=2,
                    height=1,
                    bg=NO_DRAW_COLOR,
                    relief=tkinter.SUNKEN,
                    font=FONT
                )
                # ラベルを配置
                label.grid(column=i, row=j)

    def createVtclAxis(self, master):
        '縦軸に各行の塗りつぶすマス数を記載したラベルを作成'

        for j in range(self.image_height):
            text = tkinter.Label(
                master,
                text=self.row[j],
                height=1,
                font=FONT
            )
            # 上方向から順にパック
            text.pack(side=tkinter.TOP)

    def createHztlAxis(self, master):
        '横軸に各列の塗りつぶすマス数を記載したラベルを作成'

        for i in range(self.image_width):
            text = tkinter.Label(
                master,
                text=self.column[i],
                wraplength=1,  # １文字で改行
                width=2,
                font=FONT
            )
            # 左方向から順にパック
            text.pack(side=tkinter.LEFT)

    def setEvents(self):
        '各種イベントを設定するメソッド'

        # 全ラベルに対してイベントを設定
        for j in range(self.image_height):
            for i in range(self.image_width):

                # gridへの配置場所からウィジェット取得
                widgets = self.frame_BR.grid_slaves(column=i, row=j)
                label = widgets[0]

                # 左クリック時のイベント設定
                label.bind("<ButtonPress-1>", self.draw)

                # 右クリック時のイベント設定
                label.bind("<ButtonPress-2>", self.mark)

                # Shiftキー押しながらマウスインした時のイベント設定
                label.bind("<Shift-Enter>", self.multiDraw)

                # Ctrlキー押しながらマウスインした時のイベント設定
                label.bind("<Control-Enter>", self.multiMark)

    def draw(self, event):
        '''
        ラベルを左クリックされた時に
        マスに色を塗るorマスの色を元に戻すメソッド
        '''

        # クリックされたラベルを取得
        label = event.widget

        if label.cget("text") == MARK_TEXT:
            # 既にマークがつけられている場合は塗りつぶさない
            return

        if label.cget("bg") == NO_DRAW_COLOR:
            # まだ塗りつぶされていない場合は塗り潰す
            label.config(
                bg=DRAW_COLOR,
            )

        else:
            # 既に塗りつぶされている場合は元に戻す
            label.config(
                bg=NO_DRAW_COLOR,
            )

    def mark(self, event):
        '''
        ラベルを右クリックされた時に
        マスに印をつけるor元に戻すメソッド
        '''
        # クリックされたラベルを取得
        label = event.widget

        if label.cget("bg") == DRAW_COLOR:
            # 既に塗りつぶされていればマークつけない
            return

        if label.cget("text") != MARK_TEXT:
            # まだマーク付けられていない場合はマークつける
            label.config(
                text=MARK_TEXT
            )

        else:
            # 既にマークつけられている場合は元に戻す
            label.config(
                text=''
            )

    def multiDraw(self, event):
        'Shift押しながらマウスインした場合にマスに色を塗る'
        self.draw(event)

    def multiMark(self, event):
        'Control押しながらマウスインした場合にマスに印つける色'
        self.mark(event)

    def drawAnswer(self):
        '解答を表示する'

        for j in range(self.image_height):
            for i in range(self.image_width):

                # gridへの配置場所からウィジェット取得
                widgets = self.frame_BR.grid_slaves(column=i, row=j)

                # ピクセルの色からマスにつける色を設定
                if self.image[j, i] == 0:
                    color = DRAW_COLOR
                else:
                    color = NO_DRAW_COLOR

                # 答えとなるマスの色を設定
                widgets[0].config(
                    bg=color,
                    text=""
                )

app = tkinter.Tk()
picross = Picross(app, FILE_PATH)
app.mainloop()