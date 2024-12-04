import tkinter as tk
from Interface import DesignApp

class Main:
    """
    Main class to initialize and run the DesignApp interface.
    """

    def __init__(self):
        """
        Initializes the Tkinter root and the DesignApp application.
        """
        self.root = tk.Tk()
        self.app = DesignApp(self.root)

    def run(self):
        """
        Runs the main loop of the Tkinter application.
        """
        self.root.mainloop()


if __name__ == "__main__":
    # Create an instance of Main and run the application
    main_app = Main()
    main_app.run()
