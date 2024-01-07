import tkinter as tk


class Splash(tk.Toplevel):
    def __init__(self, master, image=None, timeout=3000):
        """
            create a splash screen from a specified image file
            keep splash screen up for timeout milliseconds
            """
        tk.Toplevel.__init__(self, master, borderwidth=5)
        self.main = master

        # don't show main window
        self.main.withdraw()
        self.overrideredirect(1)

        # use tkinter's PhotoImage for .gif files
        self.image = tk.PhotoImage(file=image)
        self.after_idle(self.centerOnScreen)

        self.update()
        self.after(timeout, self.destroySplash)

    def centerOnScreen(self):
        self.update_idletasks()
        self.width = self.image.width()
        self.height = self.image.height()
        screenWidth = (self.main.winfo_screenwidth() - self.width) // 2
        screenHeight = (self.main.winfo_screenheight() - self.height) // 2
        self.geometry("%ix%i+%i+%i" % (self.width + 10, self.height + 10, screenWidth, screenHeight))
        self.createSplash()

    def createSplash(self):
        # show the splash image
        self.canvas = tk.Canvas(self, height=self.height, width=self.width)
        self.canvas.create_image(0, 0, anchor='nw', image=self.image)
        self.canvas.pack()

    def destroySplash(self):
        # bring back main window and destroy splash screen
        self.main.update()
        self.main.deiconify()
        self.withdraw()
