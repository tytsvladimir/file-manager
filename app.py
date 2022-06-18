from tkinter import *
import os, fnmatch, shutil

PATH = r'C:\Users\Vladimir\Desktop'
# PATH = os.path.abspath('.')
directory = []

root = Tk()
root.geometry('535x355+500+300')
root.resizable(False, False)
root.iconbitmap('img/icon.ico')
root.title('File Manager')
font = ("Tahoma", 12)


def up_dir():
    '''Go up directory'''
    global PATH
    PATH = os.path.dirname(PATH)
    return PATH


class Buttons:
    def __init__(self):
        self.button_save_txt = Button(text='Save file', bg='#99ff66', padx=10,
                                      command=lambda: self.button_action('save'))
        self.button_clear_txt = Button(text='Clear file', padx=10,
                                       command=lambda: self.button_action('clear'))
        self.button_close_txt = Button(text='Close file', bg='#ff6666', padx=10,
                                       command=lambda: self.button_action('close'))

    def place(self):
        self.button_save_txt.place(x=20, y=10)
        self.button_clear_txt.place(x=130, y=10)
        self.button_close_txt.place(x=240, y=10)

    def forget(self):
        self.button_save_txt.place_forget()
        self.button_clear_txt.place_forget()
        self.button_close_txt.place_forget()

    def button_action(self, action):
        if action == 'save':
            text_content = text.get(0.0, END)
            try:
                with open(file_opened, 'w') as file:
                    file.write(text_content)
                info('Файл успешно сохранен', color='green', mode=1)
            except BaseException as error:
                info(f'{type(error)}', color='red', mode=1)
        elif action == 'clear':
            text.delete(0.0, END)
        elif action == 'close':
            self.forget()
            text.delete(0.0, END)
            text.pack_forget()
            entry_path.place(x=5, y=11)
            button_open.place(x=480, y=1)
            list.pack(side=RIGHT, fill=BOTH)
            refresh_window()


buttons = Buttons()

# Path entry field
entry_path = Entry(width=52, font=font)
entry_path.place(x=5, y=11)
label = Label()


def info(text, color=None, mode=0):
    label.config(text=text, fg=color)
    label.place(x=10, y=320)
    if mode:
        label.after(3000, label.place_forget)


button_exit = Button(text='Закрыть поиск', padx=10)
button_paste = Button(text='Вставить', padx=10)


def entry_action(n=None):
    '''Processing the entered path'''
    global PATH
    def search(pars):
        found = []
        path = pars[:-pars[::-1].index('/')].replace('/', '')
        pattern = pars[-pars[::-1].index('/'):]
        count = 0
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    found.append(os.path.join(root, name))
                    count += 1
        list.delete(0, END)
        button_exit.place(x=400, y=320)

        def exit_search():
            button_exit.place_forget()
            refresh_window()

        button_exit.config(command=exit_search)
        info(f'Найдено совпадений: {count}', color='black')
        for i in found:
            list.insert(END, i)

    abs_path = entry_path.get()
    if '/' in abs_path:
        search(abs_path)
    else:
        if os.path.isdir(abs_path):
            PATH = abs_path
        else:
            PATH = PATH[:-PATH[::-1].index('\\') - 1]
        refresh_window()


entry_path.bind('<Return>', entry_action)
# Button for open entered path
open_png = PhotoImage(file=os.path.abspath('img/open.png'))
button_open = Button(image=open_png, border=0, command=entry_action)
button_open.place(x=480, y=1)

frame_dir = Frame(root)
frame_dir.place(x=5, y=50)

scrollbar = Scrollbar(frame_dir)
scrollbar.pack(side=RIGHT, fill=Y)

# Box with list of directory
list = Listbox(frame_dir, yscrollcommand=scrollbar.set, font=font, width=56, height=13, selectmode=BROWSE)
list.pack(side=RIGHT, fill=BOTH)
scrollbar.config(command=list.yview)

# Text field
text = Text(frame_dir, yscrollcommand=scrollbar.set, font=font, width=56, height=13)


def sub_window(name):
    def operation(name=name):
        global PATH
        edited_name = entry_name.get()
        if name == 'Create folder':
            try:
                os.mkdir(os.path.join(PATH, edited_name))
            except OSError:
                print('A directory with the same name already exists')
        elif name == 'Create file':
            try:
                with open(os.path.join(PATH, edited_name), 'w+') as file:
                    pass
            except BaseException as error:
                return type(error)

        elif name == 'Rename':
            try:
                old_name = os.path.join(PATH, directory[list.curselection()[0]])
                new_name = os.path.join(PATH, edited_name)
                os.rename(old_name, new_name)
            except BaseException as error:
                info(f'{type(error)}', color='red', mode=1)
        sub_win.destroy()
        refresh_window()

    global PATH, directory, copied_object, moveable_object
    if name == 'Rename':
        if not len(list.curselection()):
            info(f'Выберите объект', color='red', mode=1)
            return
    elif name == 'Copy':
        if not len(list.curselection()):
            info(f'Выберите объект', color='red', mode=1)
            return
        else:
            name_object = directory[list.curselection()[0]]
            abs_path = os.path.join(PATH, name_object)
            button_paste.place(x=420, y=320)

            def paste_dir():
                def copy(src, dsc, mode):
                    shutil.copytree(src, dsc) if mode else shutil.copyfile(src, dsc)

                if os.path.isfile(abs_path):
                    try:
                        dsc = os.path.join(PATH, name_object)
                        copy(abs_path, dsc, mode=0)
                        button_paste.place_forget()
                        refresh_window()
                    except shutil.SameFileError:
                        info(f'В данной дериктории уже есть такой файл', color='red', mode=1)
                elif os.path.isdir(abs_path):
                    try:
                        dsc2 = os.path.join(PATH, name_object)
                        copy(abs_path, dsc2, mode=1)
                        button_paste.place_forget()
                        refresh_window()
                    except FileExistsError:
                        info(f'В данной дериктории уже есть такой файл', color='red', mode=1)

            button_paste.config(command=paste_dir)
            info(f'Перейдите в директорию и нажмите кнопку "Вставить"', color='green')
            return

    elif name == 'Move':
        if not len(list.curselection()):
            info(f'Выберите объект', color='red', mode=1)
            return
        else:
            name_object = directory[list.curselection()[0]]
            abs_path = os.path.join(PATH, name_object)
            button_paste.place(x=420, y=320)

            def paste_dir():
                try:
                    dsc = os.path.join(PATH, name_object)
                    shutil.move(abs_path, dsc)
                    button_paste.place_forget()
                    refresh_window()
                except shutil.Error:
                    info(f'Cannot move a directory into itself', color='red', mode=1)

            button_paste.config(command=paste_dir)
            info(f'Перейдите в директорию и нажмите кнопку "Вставить"', color='green')
            return

    sub_win = Toplevel()
    sub_win.geometry('300x150+650+450')
    sub_win.resizable(False, False)
    sub_win.title(name)
    # sub_win.overrideredirect(True)
    entry_name = Entry(sub_win, width=30, font=8)
    entry_name.pack(side=TOP, padx=20, pady=20)
    # entry_name.insert(0, directory[list.curselection()[0]])
    entry_name.focus()
    entry_name.bind('<Return>', operation)  # Почему-то не работает
    Button(sub_win, text='Cancel', font=8, command=lambda: sub_win.destroy()).pack(side=LEFT, padx=20)
    Button(sub_win, text='Ok', font=8, fg='green', command=operation).pack(side=RIGHT, padx=20)


def delete():
    def del_object():
        abs_path = os.path.join(PATH, directory[list.curselection()[0]])  # Получили абсолютный путь к файлу
        if os.path.isdir(abs_path):
            try:
                shutil.rmtree(abs_path)  # Удалаем папку со всем содержимым
            except BaseException:
                return type(BaseException)
        elif os.path.isfile(abs_path):
            try:
                os.remove(abs_path)
            except BaseException as error:
                return type(error)
        refresh_window()
        sub_win.destroy()

    if len(list.curselection()):
        sub_win = Toplevel(root)
        sub_win.geometry('300x150+650+450')
        sub_win.resizable(False, False)
        sub_win.overrideredirect(True)
        Message(sub_win, text='Are you sure you want to delete this?', fg='red').pack(side=LEFT, padx=20, pady=20)
        Button(sub_win, text='Cancel', font=8, command=lambda: sub_win.destroy()).pack(side=LEFT, padx=10)
        b = Button(sub_win, text='Ok', font=8, fg='red', command=del_object)
        b.pack(side=RIGHT, padx=10)
        b.focus()
        b.bind('<Return>', del_object)


class Post_menu:
    def __init__(self):
        self.menu = Menu(tearoff=0)
        self.menu.add_command(font=font, label='Create folder', command=lambda: sub_window('Create folder'))
        self.menu.add_command(font=font, label='Create file', command=lambda: sub_window('Create file'))
        self.menu.add_command(font=font, label='Copy', command=lambda: sub_window('Copy'))
        self.menu.add_command(font=font, label='Move', command=lambda: sub_window('Move'))
        self.menu.add_command(font=font, label='Rename', command=lambda: sub_window('Rename'))
        self.menu.add_command(font=font, label='Delete', command=delete)

    def popup(self, event):
        self.menu.post(event.x_root, event.y_root)


m = Post_menu()

list.bind("<Button-3>", m.popup)


def action(self):
    global PATH
    # Getting name selected object
    try:
        object = directory[list.curselection()[0]]
        # If selected '...'
        if object == directory[0]:
            up_dir()
            refresh_window()
        else:
            PATH = os.path.join(PATH, object)
            # If this folder
            if os.path.isdir(PATH):
                refresh_window()
            # If this file
            elif os.path.isfile(PATH) and PATH[-4:] == '.txt':
                global file_opened
                file_opened = PATH
                entry_path.place_forget()
                button_open.place_forget()
                list.pack_forget()
                buttons.place()
                text.pack(side=LEFT, fill=BOTH)
                with open(PATH, 'r') as file:
                    file_content = file.read()
                text.insert(0.0, file_content)
                file_opened = PATH
                info(f'Просмотр и редактирование файла {object}', color='black')
                up_dir()
            else:
                os.system(f'explorer.exe {PATH}')
                up_dir()
    except IndexError:
        info('File was not selected', color='red', mode=1)


list.bind('<Return>', action)
list.bind('<Double-Button-1>', action)


def refresh_window():
    global directory
    directory = os.listdir(PATH)
    directory.insert(0, '...')
    entry_path.delete(0, END)
    entry_path.insert(0, PATH)
    list.delete(0, END)
    info(f'Количество элементов: {len(directory) - 1}', color='black')
    for i in directory:
        list.insert(END, i)


if __name__ == '__main__':
    refresh_window()
    root.mainloop()
