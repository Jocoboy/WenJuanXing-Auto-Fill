import tkinter as tk

# import settings
import wjx


def main():
    ACCESS_URL = var_access_url.get()
    SAMPLE_NO = var_sample_no.get()
    REG_EXP = var_reg_exp.get()
    # print(ACCESS_URL)
    # print(SAMPLE_NO)
    # print(REG_EXP)
    my_wjx = wjx.WengJuanXing(ACCESS_URL,
                       SAMPLE_NO, REG_EXP)
    my_wjx.mul_run()


if __name__ == "__main__":

    window = tk.Tk()
    window.title('问卷星自动填写脚本')
    window.geometry('500x300')
    window.resizable(width=False, height=False)

    canvas = tk.Canvas(window, width=500, height=100, bg='yellowgreen')
    image_file = tk.PhotoImage(file='logo.png')
    image = canvas.create_image(250, 10, anchor='n', image=image_file)
    canvas.pack(side='top')

    tk.Label(window, text='问卷发布网址:', font=('YaHei', 12)).place(x=30, y=120)
    tk.Label(window, text='生成答卷数:', font=('YaHei', 12)).place(x=30, y=160)
    tk.Label(window, text='正则表达式:', font=('YaHei', 12)).place(x=30, y=200)

    var_access_url = tk.StringVar()
    var_access_url.set('https://www.wjx.cn/jq/********.aspx')
    entry_access_url = tk.Entry(
        window, textvariable=var_access_url, font=('YaHei', 12),width=35)
    entry_access_url.place(x=170, y=120)

    var_sample_no = tk.StringVar()
    var_sample_no.set('200')
    entry_sample_no = tk.Entry(
        window, textvariable=var_sample_no, font=('YaHei', 12),width=5)
    entry_sample_no.place(x=170, y=160)

    var_reg_exp = tk.StringVar()
    var_reg_exp.set('1$2}2$2|3|4}3$数字媒体技术')
    entry_reg_exp = tk.Entry(
        window, textvariable=var_reg_exp, font=('YaHei', 12),width=35)
    entry_reg_exp.place(x=170, y=200)

    btn_run = tk.Button(window, text='开始自动填写', command=main)
    btn_run.place(x=200, y=240)

    window.mainloop()
