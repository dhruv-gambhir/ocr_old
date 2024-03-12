import tkinter as tk   # 导入Tkinter库
import cv2   # 导入OpenCV库
from PIL import Image, ImageTk   # 导入Pillow库
import pytesseract   # 导入pytesseract库
import re# 读取正则 并拆分text
 
pytesseract.pytesseract.tesseract_cmd=r'C:\Users\HVS052\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
class App:
    def __init__(self, window, window_title):
        self.window = window   # 创建Tkinter窗口对象
        self.window.title("NESPRESSO Return")   # 设置窗口标题
        self.window.geometry("1300x480")  # 设置窗口大小为1300宽，480高
 
        # 打开视频源
        self.cap = cv2.VideoCapture(2)
 
        # 创建一个画布，大小可以容纳以上视频源的大小
        self.canvas = tk.Canvas(window, width=600, height=480)
        self.canvas.pack(side=tk.LEFT)   # 把画布放到左边
        # 创建一个新的画布，用于绘制灰色边框
        self.border_canvas = tk.Canvas(window, width=250, height=250)
        self.border_canvas.place(x=605, y=0)
        self.border_canvas.create_rectangle(2, 0, 252, 250, outline="grey", width=2)
 
 
 
 
 
        # 创建一个生产日期文本标签和文本框
        self.prod_date_label = tk.Label(window, text="生产日期:", font=("微软雅黑", 25))
        self.prod_date_label.place(x=870, y=0)
        self.prod_date_text = tk.Text(window, width=11, height=1, font=("微软雅黑", 40))
        self.prod_date_text.place(x=870, y=50)
 
        # 创建一个失效日期文本标签和文本框
        self.exp_date_label = tk.Label(window, text="失效日期:", font=("微软雅黑", 25))
        self.exp_date_label.place(x=870, y=130)
        self.exp_date_text = tk.Text(window, width=11, height=1, font=("微软雅黑", 40))
        self.exp_date_text.place(x=870, y=180)
 
        # 创建一个产品号文本标签和文本框
        self.prod_id_label = tk.Label(window, text="产品号:", font=("微软雅黑", 25))
        self.prod_id_label.place(x=870, y=260)
        self.prod_id_text = tk.Text(window, width=11, height=1, font=("微软雅黑", 40))
        self.prod_id_text.place(x=870, y=310)
 
        self.prod_date_label = tk.Label(window, text="↑↑↑截图显示区↑↑↑", font=("微软雅黑", 20), fg="grey")
        self.prod_date_label.place(x=610, y=260)
        #定义清空按钮
        self.clear_button = tk.Button(window, text="保存并清除", command=self.clear_all, width=10, height=1, font=("微软雅黑", 20), bg="mintcream", fg="black")
 
        self.clear_button.place(x=870, y=400)
 
 
 
 
        # 绑定回车键到capture_image函数
        self.window.bind('<Return>', self.capture_image)
 
 
 
 
 
        # update函数被调用一次后，每隔delay毫秒就会自动调用它
        self.delay = 15
        self.update()
 
        self.window.mainloop()
     #定义清空指令
    def clear_all(self):
        self.border_canvas.imgtk = None
        self.prod_date_text.delete(1.0, tk.END)
        self.exp_date_text.delete(1.0, tk.END)
        self.prod_id_text.delete(1.0, tk.END)
 
    def capture_image(self, event=None):
        # 捕捉当前视频源的帧
        ret, frame = self.cap.read()
        # 截取指定区域的图像
        x1, y1, x2, y2 = 175, 115, 425, 365
        frame = frame[y1:y2, x1:x2]
 
 
        # 把帧转换成ImageTk对象并显示在画布上
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.border_canvas.imgtk = imgtk
        self.border_canvas.create_image(2, 0, anchor=tk.NW, image=imgtk)
 
        # 使用Pillow库在捕捉的图像中识别文本，并在文本区域中显示它
        text = pytesseract.image_to_string(img)
 
 
             # 从识别结果中提取日期和产品号信息，并显示在文本框中
        pattern = r"\d{4}\.\d{2}\.\d{2}"  # 匹配yyyy.mm.dd格式的日期
        dates = re.findall(pattern, text)
        print(re.findall(pattern, text))
        print("test")
        print(pattern)
        print(text)
        if len(dates) >= 2:
            # 显示生产日期和失效日期
            self.prod_date_text.delete(1.0, tk.END)
            self.exp_date_text.delete(1.0, tk.END)
            self.prod_date_text.insert(tk.END, dates[0])
            self.exp_date_text.insert(tk.END, dates[1])
            print("x"+dates[0])
        if len(dates) >= 1:
            # 显示产品号
            prod_id_pattern = r"\d{10}"  # 匹配10位纯数字
            prod_id = re.search(prod_id_pattern, text)
            if prod_id:
                self.prod_id_text.delete(1.0, tk.END)
                self.prod_id_text.insert(tk.END, prod_id.group())
                print("y"+dates[0])
        else:
            print("none")
 
    def update(self):
        # 从视频源获取一帧
        ret, frame = self.cap.read()
 
        if ret:
            # 把帧转换成ImageTk对象并显示在画布上
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.imgtk = imgtk
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
 
        self.window.after(self.delay, self.update)
        self.canvas.create_rectangle(175, 115, 425, 365, outline="green", width=2)
 
 
App(tk.Tk(), "Tkinter和OpenCV")