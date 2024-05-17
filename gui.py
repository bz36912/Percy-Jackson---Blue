import tkinter as tk
from PIL import Image, ImageTk
from ML import WALKING_ENCODE, RUNNING_ENCODE, SITTING_ENCODE, STANDING_ENCODE, DO_NOTHING_ENCODE


previous_class = None
current_class  = None



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

        self.previous_activity = self.resize_image("Images/sitting.png", 100, 100) 
        self.image_label = tk.Label(root, image=self.previous_activity)
        self.image_label.pack()

        self.current_activity = self.resize_image("Images/running.png", 100, 100)
        self.image_label = tk.Label(root, image=self.current_activity)
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

    def change_previous(self, activityClass):
        if (activityClass == WALKING_ENCODE):
            self.previous_activity = self.resize_image("Images/walking.png")
        elif (activityClass == RUNNING_ENCODE):
            self.previous_activity = self.resize_image("Images/running.png")
        elif (activityClass == SITTING_ENCODE):
            self.previous_activity = self.resize_image("Images/sitting.png")
        elif (activityClass == STANDING_ENCODE):
            self.previous_activity = self.resize_image("Images/standin.png")
    
    def change_current(self, activityClass):
        if (activityClass == WALKING_ENCODE):
            self.current_activity = self.resize_image("Images/walking.png")
        elif (activityClass == RUNNING_ENCODE):
            self.current_activity = self.resize_image("Images/running.png")
        elif (activityClass == SITTING_ENCODE):
            self.current_activity = self.resize_image("Images/sitting.png")
        elif (activityClass == STANDING_ENCODE):
            self.current_activity = self.resize_image("Images/standin.png")

    def change_images(self, predictedClass):
        if previous_class is not None:
            self.change_current(predictedClass)
            previous_class = current_class
            current_class = predictedClass
            self.change_previous(previous_class)
        elif previous_class is None:
            previous_class = predictedClass
            current_class = predictedClass
            self.change_current(predictedClass)
            self.change_previous(predictedClass)
