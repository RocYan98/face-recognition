import show_camera
import tkinter.messagebox
from tkinter import *
import tkinter.filedialog
from tkinter.ttk import Treeview
import pymysql
from PIL import Image, ImageTk
import cv2 as cv
import os


def open_camera():
    show_camera.start()


def sql_conn(sql):
    conn = pymysql.connect(host="127.0.0.1", user="root", password="root", database="face_recognition",
                           charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    ret = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return ret


def get_file_name():
    L = []
    for root, dirs, files in os.walk(dataset):
        for file in files:
            if os.path.splitext(file)[1] == '.png':
                L.append(os.path.join(os.path.splitext(file)[0]))
    return L


class User:
    id = None
    object_name = None
    username = None


user = User
dataset = "/Users/Yan/Projects/PycharmProjects/face_rec/dataset/"


class LoginPage:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('人脸识别系统')
        self.root.maxsize(350, 180)
        Label(self.root, text='欢迎使用人脸识别系统', width=40, height=2,
              bg='#56764C').grid(row=0, sticky=W + E)

        self.frame = Frame()
        self.frame.grid(row=2, pady=10)
        self.username = StringVar()
        self.password = StringVar()
        Label(self.frame, text='账号: ').grid(row=1, pady=10)
        Entry(self.frame, textvariable=self.username).grid(row=1, column=1)
        Label(self.frame, text='密码: ').grid(row=2, pady=10)
        Entry(self.frame, textvariable=self.password, show='*').grid(row=2, column=1)
        Button(self.frame, text='注册', width=5, command=sign_up).grid(row=3, column=0, pady=10)
        Button(self.frame, text='修改密码', width=10, command=change_password).grid(row=3, column=1, pady=10)
        Button(self.frame, text='登陆', width=5, command=self.loginCheck).grid(row=3, column=2, pady=10)

        self.root.mainloop()

    def loginCheck(self):
        sql = """select * from account where username='%s' and pwd = '%s'""" % (
            self.username.get(), self.password.get())
        ret = sql_conn(sql)
        if len(ret) > 0:
            tkinter.messagebox.showinfo('', '登陆成功!')
            user.id = ret[0]['aid']
            user.username = ret[0]['username']
            self.root.destroy()
            MainPage()
        else:
            tkinter.messagebox.showerror(title='错误', message='账号或密码错误！')


def sign_up():
    def sign():
        try:
            if password1.get() == password2.get():
                sql = """insert into account (username, pwd) values ('%s','%s')""" % (username.get(), password1.get())
                sql_conn(sql)
                tkinter.messagebox.showinfo('', '注册成功!')
                top.destroy()
            else:
                tkinter.messagebox.showerror(title='注册失败', message='两次输入的密码不同！')
        except:
            tkinter.messagebox.showerror(title='警告', message='账号已存在！')

    top = Toplevel()
    top.title('注册')
    top.maxsize(350, 250)
    top.geometry('350x250')
    Label(top, text='欢迎注册', width=40, height=2,
          bg='#56764C').grid(row=0, sticky=W + E)

    username = StringVar()
    password1 = StringVar()
    password2 = StringVar()
    Label(top, text='用户名: ').place(x=54, y=60)
    Entry(top, textvariable=username).place(x=102, y=60)
    Label(top, text='请输入密码: ').place(x=26, y=110)
    Entry(top, textvariable=password1, show='*').place(x=102, y=110)
    Label(top, text='再次输入密码: ').place(x=13, y=160)
    Entry(top, textvariable=password2, show='*').place(x=102, y=160)
    Button(top, text='确认注册', width=10, command=sign).place(x=130, y=210)


def change_password():
    def change():
        sql1 = """select * from account where username='%s'""" % username.get()
        ret1 = sql_conn(sql1)
        sql2 = """select * from account where username='%s' and pwd='%s'""" % (username.get(), oldpassword.get())
        ret2 = sql_conn(sql2)
        if not (len(ret1) > 0):
            tkinter.messagebox.showerror(title='修改失败', message='账号不存在！')
        elif not (len(ret2) > 0):
            tkinter.messagebox.showerror(title='修改失败', message='原密码不正确！')
        elif password1.get() != password2.get():
            tkinter.messagebox.showerror(title='修改失败', message='两次输入的密码不同！')
        else:
            sql = "update account set pwd='" + password1.get() + "' where username='" + username.get() + "';"
            sql_conn(sql)
            tkinter.messagebox.showinfo('', '修改成功!')
            top.destroy()

    top = Toplevel()
    top.title('修改密码')
    top.maxsize(350, 250)
    top.geometry('350x250')
    Label(top, text='欢迎使用人脸识别系统', width=40, height=2,
          bg='#56764C').grid(row=0, sticky=W + E)

    username = StringVar()
    oldpassword = StringVar()
    password1 = StringVar()
    password2 = StringVar()
    Label(top, text='账号: ').place(x=66, y=60)
    Entry(top, textvariable=username).place(x=110, y=60)
    Label(top, text='请输入原密码: ').place(x=13, y=90)
    Entry(top, textvariable=oldpassword, show='*').place(x=110, y=90)
    Label(top, text='请输入新密码: ').place(x=13, y=120)
    Entry(top, textvariable=password1, show='*').place(x=110, y=120)
    Label(top, text='再次输入密码: ').place(x=13, y=150)
    Entry(top, textvariable=password2, show='*').place(x=110, y=150)
    Button(top, text='确认修改', width=10, command=change).place(x=130, y=200)


class MainPage:
    def __init__(self):

        self.root = tkinter.Tk()
        self.root.title('人脸识别系统')
        self.root.maxsize(600, 380)
        Label(self.root, text='欢迎使用人脸识别系统', width=40, height=2,
              bg='#56764C').grid(row=0, sticky=W + E)

        self.frame = Frame()
        self.frame.grid(row=2, pady=20)

        image_open = Image.open('logo/badge.png').resize((200, 200))
        image = ImageTk.PhotoImage(image=image_open)
        Label(self.frame, image=image).grid(row=1, columnspan=5, pady=20)
        Button(self.frame, text="开始使用", width=10, command=self.start).grid(row=2, column=0, pady=10, padx=10)
        Button(self.frame, text="上传照片", width=10, command=self.open_update).grid(row=2, column=1, pady=10, padx=10)
        Button(self.frame, text="选择目标", width=10, command=self.choose_person).grid(row=2, column=2, pady=10, padx=10)
        Button(self.frame, text="查询记录", width=10, command=self.open_records).grid(row=2, column=3, pady=10, padx=10)
        Button(self.frame, text="退出系统", width=10, command=self.root.destroy).grid(row=2, column=4, pady=10, padx=10)

        self.root.mainloop()

    def start(self):
        try:
            res = show_camera.start(user.object_name)
            total_time = list(res)[1]
            tkinter.messagebox.showinfo('', "本次在线总时长" + str(total_time) + "秒")
            records = list(res)[0]
            if len(records):
                for record in records:
                    sql = """insert into records(aid, object_name ,appear, disappear, last_time)
                    values ('%s', '%s', '%s', '%s', '%s')""" \
                          % (user.id, user.object_name, record['appear'], record['disappear'], record['last'])
                    sql_conn(sql)
        except TypeError:
            tkinter.messagebox.showerror('错误', '请先选取目标')

    def open_update(self):
        UpdatePic()

    def open_records(self):
        top = Toplevel()
        top.title('记录')
        top.maxsize(600, 600)
        Label(top, text='欢迎使用人脸识别系统', width=35, height=2,
              bg='#56764C').grid(row=0, columnspan=2, sticky=W + E)
        columns = ('所选目标', '出现时间', '消失时间', '持续时间')
        tree = Treeview(top, show='headings', columns=columns)
        tree.column('所选目标', width=150, anchor='center')
        tree.column('出现时间', width=150, anchor='center')
        tree.column('消失时间', width=150, anchor='center')
        tree.column('持续时间', width=150, anchor='center')
        tree.heading('所选目标', text='所选目标')
        tree.heading('出现时间', text='出现时间')
        tree.heading('消失时间', text='消失时间')
        tree.heading('持续时间', text='持续时间')
        sql = "select * from records where aid = '%s'" % user.id
        ret = sql_conn(sql)
        for i in range(len(ret)):
            tree.insert('', i,
                        values=(ret[i]['object_name'], ret[i]['appear'], ret[i]['disappear'], ret[i]['last_time']))
        tree.grid(row=1, column=0, sticky=NSEW)
        scrollbar = Scrollbar(top)
        scrollbar.grid(row=1, column=1, sticky=NS)
        scrollbar.config(command=tree.yview)

    def choose_person(self):
        global choose_one
        top = Toplevel()
        top.title('选取目标')
        top.maxsize(600, 600)
        Label(top, text='欢迎使用人脸识别系统', width=35, height=2, bg='#56764C').grid(row=0, columnspan=2, sticky=W + E)
        lb = Listbox(top, exportselection=0)

        lb.grid(row=1, columnspan=2, sticky=W + E)
        scr1 = Scrollbar(top)
        lb.configure(yscrollcommand=scr1.set)
        scr1['command'] = lb.yview
        scr1.grid(row=1, column=1, sticky=E + N + S)

        for item in get_file_name():
            lb.insert("end", item)

            def choose_one():
                user.object_name = lb.get(ACTIVE)
                top.destroy()

        Button(top, text="确定", command=choose_one).grid(row=2, columnspan=2, pady=10, ipadx=20)

        top.mainloop()


class UpdatePic:
    def __init__(self):
        self.root = tkinter.Toplevel()
        self.root.title('上传照片')
        self.root.maxsize(600, 600)
        Label(self.root, text='欢迎使用人脸识别系统', width=22, height=2,
              bg='#56764C').grid(row=0, sticky=W + E)

        self.frame = Frame(self.root)
        self.frame.grid(row=3, pady=20)
        self.filename = None

        self.canva = Canvas(self.frame, width=200, height=200, bg="gray")
        self.canva.grid(row=1, column=1)
        tkinter.Button(self.frame, text="选择文件", width=10, command=self.choose_file).grid(row=2, column=1, pady=10)
        tkinter.Button(self.frame, text="设置姓名", width=10, command=self.set_name).grid(row=3, column=1, pady=10)
        tkinter.Button(self.frame, text="确定", width=10, command=self.upload).grid(row=4, column=1, pady=10)

        self.root.mainloop()

    def choose_file(self):
        filename = tkinter.filedialog.askopenfilename(title='选择文件')
        img = cv.imread(filename)
        self.Showimage(img, self.canva, "fill")
        self.filename = filename

    def upload(self):
        img = Image.open(self.filename)
        try:
            img.save(dataset + user.object_name + '.png')
            tkinter.messagebox.showinfo('', '上传成功!')
            self.root.destroy()
        except TypeError:
            tkinter.messagebox.showerror('', '请设置姓名')

    def set_name(self):
        def set():
            user.object_name = object_name.get()
            top.destroy()

        top = Toplevel()
        top.title('设置姓名')
        top.maxsize(350, 250)
        top.geometry('350x250')
        Label(top, text='欢迎使用人脸识别系统', width=40, height=2,
              bg='#56764C').grid(row=0, sticky=W + E)

        object_name = StringVar()
        Label(top, text='输入姓名: ').place(x=45, y=60)
        Entry(top, textvariable=object_name).place(x=110, y=60)
        Button(top, text='确认', width=10, command=set).place(x=130, y=200)

    def Showimage(self, imgCV_in, canva, layout="null"):
        """
        Showimage()是一个用于在tkinter的canvas控件中显示OpenCV图像的函数。
        使用前需要先导入库
        import cv2 as cv
        from PIL import Image,ImageTktkinter
        并注意由于响应函数的需要，本函数定义了一个全局变量 imgTK，请不要在其他地方使用这个变量名!
        参数：
        imgCV_in：待显示的OpenCV图像变量
        canva：用于显示的tkinter canvas画布变量
        layout：显示的格式。可选项为：
            "fill"：图像自动适应画布大小，并完全填充，可能会造成画面拉伸
            "fit"：根据画布大小，在不拉伸图像的情况下最大程度显示图像，可能会造成边缘空白
            给定其他参数或者不给参数将按原图像大小显示，可能会显示不全或者留空
        """
        global imgTK
        canvawidth = int(canva.winfo_reqwidth())
        canvaheight = int(canva.winfo_reqheight())
        sp = imgCV_in.shape
        cvheight = sp[0]  # height(rows) of image
        cvwidth = sp[1]  # width(colums) of image
        if layout == "fill":
            imgCV = cv.resize(imgCV_in, (canvawidth, canvaheight), interpolation=cv.INTER_AREA)
        elif layout == "fit":
            if float(cvwidth / cvheight) > float(canvawidth / canvaheight):
                imgCV = cv.resize(imgCV_in, (canvawidth, int(canvawidth * cvheight / cvwidth)),
                                  interpolation=cv.INTER_AREA)
            else:
                imgCV = cv.resize(imgCV_in, (int(canvaheight * cvwidth / cvheight), canvaheight),
                                  interpolation=cv.INTER_AREA)
        else:
            imgCV = imgCV_in
        imgCV2 = cv.cvtColor(imgCV, cv.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
        current_image = Image.fromarray(imgCV2)  # 将图像转换成Image对象
        imgTK = ImageTk.PhotoImage(image=current_image)  # 将image对象转换为imageTK对象
        canva.create_image(0, 0, anchor=NW, image=imgTK)


if __name__ == '__main__':
    LoginPage()
