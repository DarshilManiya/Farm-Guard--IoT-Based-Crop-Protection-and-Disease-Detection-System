import kivy
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
import sys
from firebase_admin import credentials, firestore, initialize_app
from kivy.uix.floatlayout import FloatLayout


kivy.require('1.9.0')


class CodeUnnati(App):

    def build(self):
        Window.size = (640, 1136)
        cred = credentials.Certificate("./google.json")
        initialize_app(cred)

        self.window = GridLayout(cols=1, spacing=30, size_hint=(0.8, 0.7),
                                 pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.n_layout1 = BoxLayout(orientation='horizontal', size_hint=(1, 0.1),
                                  pos_hint={"center_x": 0.5, "center_y": 0.5}, spacing=5)
        self.n_layout2 = BoxLayout(orientation='horizontal', size_hint=(1, 0.1),
                                   pos_hint={"center_x": 0.5, "center_y": 0.5}, spacing=5)
        self.n_layout3 = BoxLayout(orientation='horizontal', size_hint=(1, 0.1),
                                   pos_hint={"center_x": 0.5, "center_y": 0.5}, spacing=5)
        self.n_layout4 = BoxLayout(orientation='horizontal', size_hint=(1, 0.1),
                                   pos_hint={"center_x": 0.5, "center_y": 0.5}, spacing=5)


        self.greet = Label(text="Welcome!", font_size=44, color='#61fa7d',
                           pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(1, 0.65))
        self.spacer = Label(text="", size_hint=(1, 0.3))
        self.spacer2 = Label(text="", size_hint=(1, 0.1))

        self.nameLabel = Label(text="Enter your name: ", font_size=20, color='white',
                               size_hint=(0.3, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.nameInput = TextInput(background_color="#202124", foreground_color="#61fa7d",
                                   multiline=False, padding_y=(9, 9), font_size=18,
                                   size_hint=(0.7, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.emailLabel = Label(text="Enter your email ID: ", font_size=20, color='white',
                                size_hint=(0.3, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.emailInput = TextInput(background_color="#202124", foreground_color="#61fa7d",
                                   multiline=False, padding_y=(9, 9), font_size=18, size_hint=(0.6, 1),
                                   pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.addressLabel = Label(text="Enter your District, State: ", font_size=20, color='white',
                                  size_hint=(0.3, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.addressInput = TextInput(background_color="#202124", foreground_color="#61fa7d",
                                   multiline=False, padding_y=(9, 9), font_size=18, size_hint=(0.4, 1),
                                   pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.submit = Button(text="Submit", size_hint=(0.5, 0.1), bold=True, background_color='#61fa7d',
                             pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.submit.bind(on_press=self.on_button_press)
        self.clear = Button(text="Clear", size_hint=(0.5, 0.1), bold=True,
                             pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.clear.bind(on_press=self.on_button_press)


        self.window.add_widget(self.greet)
        self.window.add_widget(self.spacer2)
        self.window.add_widget(self.n_layout1)
        self.window.add_widget(self.n_layout2)
        self.window.add_widget(self.n_layout3)
        self.window.add_widget(self.spacer)
        self.window.add_widget(self.n_layout4)
        self.n_layout1.add_widget(self.nameLabel)
        self.n_layout1.add_widget(self.nameInput)
        self.n_layout2.add_widget(self.emailLabel)
        self.n_layout2.add_widget(self.emailInput)
        self.n_layout3.add_widget(self.addressLabel)
        self.n_layout3.add_widget(self.addressInput)
        self.n_layout4.add_widget(self.submit)
        self.n_layout4.add_widget(self.clear)

        return self.window

    def on_button_press(self, instance):
        button_text = instance.text

        if button_text == 'Submit':
            if self.nameInput.text != "" and self.emailInput.text != "" and self.addressInput.text != "":
                try:
                    # Initialize Firestore
                    db = firestore.client()

                    # Create a dictionary of data
                    data = {
                        'name': self.nameInput.text,
                        'email': self.emailInput.text,
                        'address': self.addressInput.text
                    }

                    # Add the data to Firestore
                    db.collection('users').add(data)

                    # Show success message
                    self.show_popup("Success", "Data submitted successfully!")

                    try:
                        self.stop()
                        exec(open("home.py").read())
                    except Exception as e:
                        print(f"Error running home.py: {e}")
                except Exception as e:
                    print(f"Error submitting data: {e}")
            else:
                self.content = Button(text='Close', on_press=self.dismiss_popup)
                self.popup = Popup(title='Enter every detail', content=self.content,
                                   size_hint=(None, None), size=(200, 100))
                self.popup.open()
        if button_text == 'Clear':
            self.nameInput.text = ""
            self.emailInput.text = ""
            self.addressInput.text = ""

    def show_popup(self, title, message):
        self.content1 = Button(text='Close', on_press=self.dismiss_popup1)
        self.popup1 = Popup(title=title, content=self.content1,
                           size_hint=(None, None), size=(200, 100))
        self.popup1.open()
    def dismiss_popup(self, instance):
        self.popup.dismiss()

    def dismiss_popup1(self, insatance):
        self.popup1.dismiss()



if __name__ == '__main__':
    CodeUnnati().run()
