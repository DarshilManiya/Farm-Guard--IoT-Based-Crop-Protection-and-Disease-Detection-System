import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from plyer import filechooser
import shutil
import sys
import time
from kivy.uix.floatlayout import FloatLayout

import os

kivy.require('1.11.1')

class Home(App):
    def build(self):
        Window.size = (640, 1136)
        layout = GridLayout(cols=1, spacing=10, size_hint=(0.8, 0.85),
                                 pos_hint={"center_x": 0.5, "center_y": 0.5})
        n_layout1 = BoxLayout(orientation='horizontal', size_hint=(1, 0.1),
                                  pos_hint={"center_x": 0.5, "center_y": 0.5}, spacing=20)
        n_layout2 = BoxLayout(orientation='horizontal', size_hint=(1, 0.1),
                              pos_hint={"center_x": 0.5, "center_y": 0.5}, spacing=20)

        self.back = Button(text='Back', on_press=self.on_button_pressed, size_hint=(None, None), width=100, height=50,
                             pos_hint={"center_x": 1, "center_y": 1})

        self.msg = Label(text="Add image for disease recognition", font_size=28, color='#61fa7d',
                           pos_hint={"center_x": 0.5, "center_y": 1}, size_hint=(1, None), height=300)


        self.camera = Button(text='Capture from Camera', on_press=self.on_button_pressed, size_hint=(0.3, 0.25),
                                  pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.gallery = Button(text='Upload from Gallery', on_press=self.on_button_pressed, size_hint=(0.3, 0.25),
                                  pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.history = Button(text='History', on_press=self.on_button_pressed, size_hint=(None, None), width=150, height=50,
                              pos_hint={"center_x": 0, "center_y": 0})


        layout.add_widget(self.back)
        layout.add_widget(self.msg)
        layout.add_widget(n_layout1)
        layout.add_widget(n_layout2)
        n_layout1.add_widget(self.camera)
        n_layout1.add_widget(self.gallery)
        n_layout2.add_widget(self.history)

        return layout

    def on_button_pressed(self, instance):
        button_text = instance.text

        if button_text == 'Capture from Camera':
            try:
                self.stop()
                exec(open("camera_capture.py").read())
            except Exception as e:
                print(f"Error running camera_capture.py: {e}")
        elif button_text == 'Upload from Gallery':
            try:
                self.stop()
                exec(open("image_upload.py").read())
            except Exception as e:
                print(f"Error running image_upload.py: {e}")

if __name__ == '__main__':
    Home().run()
