import tkinter as tk


def open_windows():
    url_list = []
    root = tk.Tk()

    canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
    canvas1.pack()

    label1 = tk.Label(root, text='Summarization')
    label1.config(font=('helvetica', 14))
    canvas1.create_window(200, 25, window=label1)

    label2 = tk.Label(root, text='Enter your url:')
    label2.config(font=('helvetica', 10))
    canvas1.create_window(200, 100, window=label2)

    entry1 = tk.Entry(root, width=50)
    canvas1.create_window(200, 140, window=entry1)

    def get_text():
        url_list.append(entry1.get())
        root.destroy()

    button1 = tk.Button(text='Enter', command=get_text, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 180, window=button1)

    root.mainloop()
    return str(url_list[0])
