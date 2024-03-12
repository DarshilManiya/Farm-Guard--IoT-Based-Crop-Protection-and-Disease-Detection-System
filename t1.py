import kivy
from docutils.parsers.rst.directives import images
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.camera import Camera
import time
from kivy.uix.image import Image
import os
import firebase_admin
from plyer import filechooser
import sys
from firebase_admin import credentials, firestore, initialize_app
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from PIL import Image
import shutil

cnt = 0

class Login(Screen):

    def submit(self):
        if self.ids.nameInput.text != "" and self.ids.emailInput.text != "" and self.ids.addressInput.text != "":
            try:
                # Initialize Firestore
                db = firestore.client()

                # Create a dictionary of data
                data = {
                    'name': self.ids.nameInput.text,
                    'email': self.ids.emailInput.text,
                    'address': self.ids.addressInput.text
                }

                # Add the data to Firestore
                db.collection('users').add(data)

                # Show success message
                self.show_popup("Success", "Data submitted successfully!")

            except Exception as e:
                print(f"Error submitting data: {e}")
        else:
            self.content = Button(text='Close', on_press=self.dismiss_popup)
            self.popup = Popup(title='Enter every detail', content=self.content,
                               size_hint=(None, None), size=(200, 100))
            self.popup.open()

    def show_popup(self, title, message):
        self.content1 = Button(text='Close', on_press=self.dismiss_popup1)
        self.popup1 = Popup(title=title, content=self.content1,
                           size_hint=(None, None), size=(200, 100))
        self.popup1.open()

    def dismiss_popup(self, instance):
        self.popup.dismiss()

    def dismiss_popup1(self, instance):
        self.popup1.dismiss()

    def clear_text_inputs(self):
        self.ids.nameInput.text = ""
        self.ids.emailInput.text = ""
        self.ids.addressInput.text = ""


class Home(Screen):
    pass


class CameraCapture(Screen):
    def capture_image(self, camera_widget):
        camera_texture = camera_widget.texture
        if camera_texture:
            buffer = camera_texture.pixels
            image = Image.frombytes('RGBA', camera_texture.size, buffer)
            self.save_image(image)

    def save_image(self, image):
        global cnt
        captured_images_dir = 'images'
        os.makedirs(captured_images_dir, exist_ok=True)
        if cnt >= 5:
            cnt = 0
        cnt += 1
        captured_image_path = os.path.join(captured_images_dir, '{}.png'.format(cnt))
        image.save(captured_image_path)

    def flip_image(self, camera):
        if camera.index == 0:
            camera.index = 2
        elif camera.index == 2:
            camera.index = 0
        else:
            camera.index = camera.index


class ImageUpload(Screen):
    def choose_image(self, selected_image):
        image_path = filechooser.open_file()
        if image_path:
            new_image_path = image_path[0]
            self.save_uploaded_image(new_image_path)
            selected_image.source = new_image_path

    def save_uploaded_image(self, source_path):
        global cnt
        project_directory = os.path.dirname(os.path.abspath('D:\Code Unnati\Code Unnati App\images'))
        project_directory = project_directory + '\images'
        if cnt >= 5:
            cnt = 0
        cnt += 1
        destination_path = os.path.join(project_directory, '{}.png'.format(cnt))
        shutil.copy(source_path, destination_path)


class History(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class CodeUnnati(App):
    def build(self):
        Window.size = (640, 1136)
        cred = credentials.Certificate("./google.json")
        initialize_app(cred)

        return kv


if __name__ == "__main__":

    for i in os.listdir('images'):
        cnt += 1

    CodeUnnati().run()
