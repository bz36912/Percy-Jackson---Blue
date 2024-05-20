"""
gui.py written by Daniel Barone
This program runs the GUI that displays the results predicted in main.py.
The gui is initialized in the main files by using gui = GUI(root)
The only other functions that are used externally are Update(), change_images(), and output_text_message()
"""


import customtkinter as ctk
from PIL import Image, ImageTk
from ML import WALKING_ENCODE, RUNNING_ENCODE, SITTING_ENCODE, STANDING_ENCODE, DO_NOTHING_ENCODE

# Global variables that keep track of the previous and current activity
previous_class = None
current_class  = None

# GUI class that the gui program runs in
# Is initialised and called in the main.py file
class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI")
        self.root.geometry("200x400")
        ctk.set_appearance_mode("light")

        self.save_image_paths()

        # Previous activity image label - shows the image of the previous activity performed by the user
        self.previous_activity_label = ctk.CTkLabel(root, image=self.sitting_png, text="Previous Activity", compound="top", fg_color="#8f8483")
        self.previous_activity_label.pack(pady=10)

        # Current activity image label - shows the image of the current activity being performed by the user
        self.current_activity_label = ctk.CTkLabel(root, image=self.sitting_png, text="Current Activity",compound="top", fg_color="#8f8483")
        self.current_activity_label.pack(pady=10)

        # Output Text Box - displays the probability of the detected action
        self.output_text = ctk.CTkTextbox(root, height=100, width=100, fg_color="#8f8483")
        self.output_text.pack(pady=10)

    # FUnction that update the image of either the previous activity image of the current acitivty image depending on th label input
    def update_image(self, image, label):
        label.configure(image=image)
        label.image = image

    # Opens the image from the given path and resizes it to 100x100 pixels
    # returns a photoTk.PhotoImage variable
    def open_resized_image(self, filePath):
        original_image = Image.open(filePath)
        resized_image = original_image.resize((100, 100), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    # function opens all image paths at once
    # Used upon initialization 
    def save_image_paths(self):
        self.walking_png = self.open_resized_image("Images/walking.png")
        self.running_png = self.open_resized_image("Images/running.png")
        self.sitting_png = self.open_resized_image("Images/sitting.png")
        self.standing_png = self.open_resized_image("Images/standing.png")

    # Function called in main.py to update the gui
    def update(self):
        self.root.update()

    # Function that changes the previous_activity variables depending on the inputted activity class
    def change_previous(self, activityClass):
        global previous_class
        if activityClass == WALKING_ENCODE:
            self.previous_activity = self.update_image(self.walking_png, self.previous_activity_label)
        elif activityClass == RUNNING_ENCODE:
            self.previous_activity = self.update_image(self.running_png, self.previous_activity_label)
        elif activityClass == SITTING_ENCODE:
            self.previous_activity = self.update_image(self.sitting_png, self.previous_activity_label)
        elif activityClass == STANDING_ENCODE:
            self.previous_activity = self.update_image(self.standing_png, self.previous_activity_label)

    # Function that changes the current_activity variables depending on the inputted activity class
    def change_current(self, activityClass):
        global current_class
        if activityClass == WALKING_ENCODE:
            self.current_activity = self.update_image(self.walking_png, self.current_activity_label)
        elif activityClass == RUNNING_ENCODE:
            self.current_activity = self.update_image(self.running_png, self.current_activity_label)
        elif activityClass == SITTING_ENCODE:
            self.current_activity = self.update_image(self.sitting_png, self.current_activity_label)
        elif activityClass == STANDING_ENCODE:
            self.current_activity = self.update_image(self.standing_png, self.current_activity_label)

    # Function called in main.py while inputting the predictedClass to change the images on the GUI
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

    # FUnction which outputs the probability of the predicted class on the gui
    def output_text_message(self, message):
        self.output_text.delete('1.0', ctk.END) # This line can be remove if the user does not want the output box to be refreshed
        self.output_text.insert(ctk.END, message + '\n') 