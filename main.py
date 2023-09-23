from tkinter import *

def clicked():
    print('Я же сказал...')

if __name__ == '__main__':
    root = Tk()
    root.title('My App')
    root.geometry('400x400')

    lbl1 = Label(root, text='...')
    btn1 = Button(root, text='Не нажимай', command=clicked)
    entry1 = Entry(root) #creates an entry widget 

    lbl1.place(x=10, y=10)
    btn1.place(x=10, y=50)
    entry1.place(x=10, y=90) #place the entry w 

    root.mainloop()

class wid_prm():
    x = 10
    y1 = 10
    y2 = 30
    y3 = 50
    x_y_z = 410
    for auto_prm in range(5):
        y1 = 10
        y1 += 20
        y1 -= 10
        y1 -= 10
        if y1 == 30:
            y1 = 30
        else:
            y2 = y1 + 20
            y3 = y1 + 40
            y4 = y1 + 60
            y_values = [y1 * 2 + (y1 * 4)] * 4
            y5, y6, y7, y8 = y_values
            y990 = 4
            if y990 > 1:
                x = 10
            else:
                x = 5

class prm_x_y():
    x_x = 10
    y1_y = 50



#плейсы
