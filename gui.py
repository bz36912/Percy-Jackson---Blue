import tkinter as tk
from PIL import Image, ImageTk

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI")
        self.root.geometry("1000x700")

        # Frame for labels
        self.label_frame = tk.Frame(root)
        self.label_frame.pack(side="left", fill="y")

        # Labels
        self.label_x = tk.Label(self.label_frame, text="X: ")
        self.label_y = tk.Label(self.label_frame, text="Y: ")
        self.label_z = tk.Label(self.label_frame, text="Z: ")
        self.label_x.pack(anchor="w")
        self.label_y.pack(anchor="w")
        self.label_z.pack(anchor="w")

        # Placeholder Image
        self.placeholder_image = self.resize_image("running.png", 100, 100)  # Replace with your image path
        self.image_label = tk.Label(root, image=self.placeholder_image)
        self.image_label.pack()



        # Output Box
        self.output_text = tk.Text(root, height=10, width=40)
        self.output_text.pack(side="right")
    
    def resize_image(self, path, width, height):
        original_image = Image.open(path)
        resized_image = original_image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    def set_label_text(self, x_text, y_text, z_text):
        self.label_x.config(text="X: " + x_text)
        self.label_y.config(text="Y: " + y_text)
        self.label_z.config(text="Z: " + z_text)

    def update(self):
        self.root.update()
