import tkinter as tk
import tkinter.font as tf

import settings
import wjx


class window:
    __width = 600
    __height = 300
    __root = tk.Tk()

    def update(self):
        ACCESS_URL = self.var_access_url.get()
        SAMPLE_NO = self.var_sample_no.get()
        SUBMIT_DATA = self.var_submit_data.get()
        print(ACCESS_URL)
        print(SAMPLE_NO)
        print(SUBMIT_DATA)
        my_wjx = wjx.WenJuanXing(settings.ACCESS_URL,
                                  settings.SAMPLE_NO, settings.SUBMIT_DATA)
        my_wjx.mul_run()

    def __init__(self):

        window = self.__root
        width = self.__width
        height = self.__height

        window.title('问卷星自动填写脚本')
        window.geometry("%sx%s" % (width, height))
        window.resizable(width=False, height=False)

        canvas = tk.Canvas(window, width=width,
                           height=height/3, bg='yellowgreen')
        image_file = tk.PhotoImage(file='logo.png')
        image = canvas.create_image(width/2, 10, anchor='n', image=image_file)
        canvas.grid(row=0, column=0, columnspan=3)

        font_style = tf.Font(family="Times", size=12, weight=tf.BOLD)

        tk.Label(window, text='问卷发布网址:', font=font_style).grid(row=1, column=0, columnspan=1,rowspan=2,pady=10)
        tk.Label(window, text='生成答卷数:', font=font_style).grid(row=3, column=0, columnspan=1,rowspan=2,pady=10)
        tk.Label(window, text='提交数据:', font=font_style).grid(row=5, column=0, columnspan=1,rowspan=2,pady=10)

        self.var_access_url = tk.StringVar()
        self.var_access_url.set(settings.ACCESS_URL)
        entry_access_url = tk.Entry(
            window, textvariable=self.var_access_url, font=font_style).grid(row=1, column=1, columnspan=2,rowspan=2,pady=1,sticky='w'+'e',padx=30)

        self.var_sample_no = tk.StringVar()
        self.var_sample_no.set(settings.SAMPLE_NO)
        entry_sample_no = tk.Entry(
            window, textvariable=self.var_sample_no, font=font_style).grid(row=3, column=1, columnspan=2,rowspan=2,pady=1,sticky='w'+'e',padx=30)

        self.var_submit_data = tk.StringVar()
        self.var_submit_data.set(settings.SUBMIT_DATA)
        entry_submit_data = tk.Entry(
            window, textvariable=self.var_submit_data, font=font_style).grid(row=5, column=1, columnspan=2,rowspan=2,pady=1,sticky='w'+'e',padx=30)

        btn_run = tk.Button(window, text='开始自动填写', command=self.update, font=font_style,
                            borderwidth=0, cursor='heart', bg='#D3D3D3', activeforeground='#A9A9A9').grid(row=7, column=1, columnspan=2,rowspan=1,pady=10)

        window.mainloop()
