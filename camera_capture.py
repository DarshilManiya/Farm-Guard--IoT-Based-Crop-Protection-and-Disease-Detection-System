import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.uix.image import Image
from plyer import filechooser
import shutil
import sys
import time
import os

kivy.require('1.11.1')

class CameraCapture(App):

    def build(self):
        Window.size = (640, 1136)
        layout = GridLayout(cols=1, spacing=10, size_hint=(0.8, 0.85),
                                 pos_hint={"center_x": 0.5, "center_y": 0.5})
        n_layout1 = BoxLayout(orientation='horizontal', size_hint=(1, 0.1),
                              pos_hint={"center_x": 0.8, "center_y": 0.5}, spacing=20)

        self.back = Button(text='Back', on_press=self.previous, size_hint=(None, None), width=100, height=50,
                           pos_hint={"center_x": 1, "center_y": 1})

        self.msg = Label(text="Capture image of crop disease", font_size=28, color='#61fa7d',
                           pos_hint={"center_x": 0.5, "center_y": 0.85}, size_hint=(1, 0.2))

        self.camera = Camera(resolution=(600, 600), play=True,
                                 pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(1, 1))


        capture_button = Button(text='Capture', size_hint=(None, None), width=150, height=50, background_color="#61fa7d",
                                pos_hint={"center_x": 0.5, "center_y": 0.05}, bold=True, on_press=self.capture_image)
        flip_button = Button(text='Flip Camera', size_hint=(None, None), width=150, height=50, bold=True,
                                pos_hint={"center_x": 0.5, "center_y": 0.05}, on_press=self.flip_image)


        layout.add_widget(self.back)
        layout.add_widget(self.msg)
        layout.add_widget(self.camera)
        layout.add_widget(n_layout1)
        n_layout1.add_widget(capture_button)
        n_layout1.add_widget(flip_button)

        return layout

    def capture_image(self, instance):
        self.captured_image_path = None
        self.captured_images_dir = 'images'
        os.makedirs(self.captured_images_dir, exist_ok=True)
        # Capture the images from the camera and display it
        timenow = time.strftime("%Y%m%d_%H%M%S")
        self.captured_image_path = os.path.join(self.captured_images_dir, 'img_{}.png'.format(timenow))
        self.camera.export_to_png(self.captured_image_path)

    def flip_image(self, instance):
        if self.camera.index == 0:
            self.camera.index = 2
        elif self.camera.index == 2:
            self.camera.index = 0
        else:
            self.camera.index = self.camera.index

    def previous(self, instance):
        try:
            self.stop()
            exec(open("home.py").read())
        except Exception as e:
            print(f"Error running home.py: {e}")

if __name__ == '__main__':
    CameraCapture().run()
