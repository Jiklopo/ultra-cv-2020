from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import image_processor


class application:
    def __init__(self, master):
        self.master = master
        self.c_size = (700, 500)
        self.setup_gui(self.c_size)
        self.img = None

    def setup_gui(self, s):
        f = Frame(self.master, bg='white', padx=10, pady=10)
        design = dict(bd=5, fg='white', bg='black', font=('', 15), )
        Button(f, text="Open New Image", **design, command=self.make_image).pack(side=LEFT)
        Button(f, text="Detect", **design, command=self.process).pack(side=RIGHT)
        Button(f, text="Blur", **design, command=self.blur).pack(side=RIGHT)
        Button(f, text="Gray", **design, command=self.gray).pack(side=RIGHT)
        Button(f, text="Thresh", **design, command=self.th).pack(side=RIGHT)
        Button(f, text="Edges", **design, command=self.edges).pack(side=RIGHT)

        f.pack()
        self.canvas = Canvas(self.master, height=800, width=1600, bd=10, bg='black', relief='ridge')
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.canvas.pack()
        self.status = Label(self.master, text='Current image: None', bg='gray', font=('', 15),
                            relief='sunken', bd=2, fg='black', anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

    def make_image(self):
        path = fd.askopenfilename()
        self.img_processor = image_processor.ImageProcessor(path)
        self.open_image(path)

    def process(self):
        path = self.img_processor.find_object()
        self.open_image(path)

    def blur(self):
        path = self.img_processor.blur()
        self.open_image(path)

    def gray(self):
        path = self.img_processor.gray()
        self.open_image(path)

    def th(self):
        path = self.img_processor.threshold()
        self.open_image(path)

    def edges(self):
        path = self.img_processor.edges()
        self.open_image(path)

    def open_image(self, path):
        self.pilImage = Image.open(path)
        width, height = self.img_processor.width, self.img_processor.height
        re = self.pilImage.resize((width, height), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(re)
        self.canvas.delete(ALL)
        self.canvas.config(width=self.img_processor.width, height=self.img_processor.height)
        self.canvas.create_image(width / 2 + 10, height / 2 + 10, anchor=CENTER, image=self.img)


if __name__ == '__main__':
    root = Tk()
    root.title("Image Viewer")
    root.resizable(1, 1)
    root.geometry('1000x1000')
    application(root)
    root.mainloop()
