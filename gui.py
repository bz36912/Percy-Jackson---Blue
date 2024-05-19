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

        self.save_image_paths()
        self.previous_image_label=tk.Label(root)
        # label.place(x=400, y=400)
        # self.previous_activity = self.resize_image(self.sitting_png) 
        self.previous_image_label = tk.Label(root, image=self.sitting_png)
        self.previous_image_label.pack()

        self.current_image_label = tk.Label(root)
        # self.current_activity = self.resize_image(self.sitting_png)
        self.current_image_label = tk.Label(root, image=self.sitting_png)
        self.current_image_label.pack()

        #stgImg = tk.PhotoImage(file="Images/sitting.png")
        #label=tk.Label(root, image=stgImg)
        #label.configure(image=stgImg)
        #label.place(x=400, y=400)



        # Output Box
        self.output_text = tk.Text(root, height=10, width=40)
        self.output_text.pack(side="right")

        
    
    def resize_image(self, original_image):
        # original_image = Image.open(path)
        # resized_image = original_image.resize((100, 100), Image.LANCZOS)
        # returned = ImageTk.PhotoImage(resized_image)
        # label.config()
        # label.image = returned
        resized_image = original_image.resize((100, 100), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

        # self.image_label = tk.Label(self.root, image=returned)
        # self.image_label.pack()

    def update_image(self, image, label):
        # img = self.resize_image(image)
        label.configure(image=image)
        label.image = image
    
    def open_resized_image(self, filePath):
        original_image = Image.open(filePath)
        resized_image = original_image.resize((100, 100), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    def save_image_paths(self):
        self.walking_png = self.open_resized_image("Images/walking.png")
        self.running_png = self.open_resized_image("Images/running.png")
        self.sitting_png = self.open_resized_image("Images/sitting.png")
        self.standing_png = self.open_resized_image("Images/standing.png")

    def update(self):
        self.root.update()

    def change_previous(self, activityClass):
        global previous_class
        global current_class
        if (activityClass == WALKING_ENCODE):
            self.previous_activity = self.update_image(self.walking_png, self.previous_image_label)
        elif (activityClass == RUNNING_ENCODE):
            self.previous_activity = self.update_image(self.running_png, self.previous_image_label)
        elif (activityClass == SITTING_ENCODE):
            self.previous_activity = self.update_image(self.sitting_png, self.previous_image_label)
        elif (activityClass == STANDING_ENCODE):
            self.previous_activity = self.update_image(self.standing_png, self.previous_image_label)
    
    def change_current(self, activityClass):
        global previous_class
        global current_class
        if (activityClass == WALKING_ENCODE):
            self.current_activity = self.update_image(self.walking_png, self.current_image_label)
        elif (activityClass == RUNNING_ENCODE):
            self.current_activity = self.update_image(self.running_png, self.current_image_label)
        elif (activityClass == SITTING_ENCODE):
            self.current_activity = self.update_image(self.sitting_png, self.current_image_label)
        elif (activityClass == STANDING_ENCODE):
            self.current_activity = self.update_image(self.standing_png, self.current_image_label)

    def change_images(self, predictedClass):
        global previous_class
        global current_class
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

    def output_text_message(self, message):
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, message + '\n')
