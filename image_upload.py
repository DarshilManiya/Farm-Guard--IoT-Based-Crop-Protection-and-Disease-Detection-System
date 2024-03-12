import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.image import Image
from plyer import filechooser
from kivy.uix.scrollview import ScrollView
import os
import shutil
import time
import sys

kivy.require('1.11.1')

class ImageUpload(App):

    def build(self):
        Window.size = (640, 1136)
        layout = GridLayout(cols=1, spacing=10, size_hint=(0.8, 0.85),
                                 pos_hint={"center_x": 0.5, "center_y": 0.5})
        n_layout1 = BoxLayout(orientation='horizontal', size_hint=(1, 0.5),
                              pos_hint={"center_x": 0.8, "center_y": 0.5}, spacing=20)

        self.back = Button(text='Back', on_press=self.previous, size_hint=(None, None), width=100, height=50,
                           pos_hint={"center_x": 1, "center_y": 1})

        self.msg = Label(text='Select Image from the Device: ', font_size=28, color='#61fa7d',
                           pos_hint={"center_x": 0.5, "center_y": 0.85}, size_hint=(1, 0.2))

        self.selected_image_label = Label(text='Selected File: ', font_size=20, color='#61fa7d',
                           pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(0.3, 1))
        self.selected_image = Image(source='img.png', pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(0.7, 0.5))
        choose_image_button = Button(text='Choose Image', on_press=self.choose_image, size_hint=(None, None),
                                     width=150, height=50, background_color="#61fa7d",
                                pos_hint={"center_x": 0.5, "center_y": 0.05}, bold=True)


        layout.add_widget(self.back)
        layout.add_widget(self.msg)
        layout.add_widget(n_layout1)
        n_layout1.add_widget(self.selected_image_label)
        n_layout1.add_widget(self.selected_image)
        layout.add_widget(choose_image_button)

        return layout

    def choose_image(self, instance):
        image_path = filechooser.open_file()
        if image_path:
            new_image_path = image_path[0]
            self.save_uploaded_image(new_image_path)
            self.selected_image.source = new_image_path

    def save_uploaded_image(self, source_path):
        # Set the destination path in your project directory
        timenow = time.strftime("%Y%m%d_%H%M%S")
        project_directory = os.path.dirname(os.path.abspath('D:\Code Unnati\Code Unnati App\images'))
        project_directory = project_directory + '\images'
        destination_path = os.path.join(project_directory, 'img_{}.png'.format(timenow))

        # Copy the file to the project directory
        shutil.copy(source_path, destination_path)
        print(f"Image saved to: {destination_path}")

    def previous(self, instance):
        try:
            print("XD")
            self.stop()
            exec(open("home.py").read())
        except Exception as e:
            print("LOL")
            print(f"Error running home.py: {e}")

if __name__ == '__main__':
    ImageUpload().run()
