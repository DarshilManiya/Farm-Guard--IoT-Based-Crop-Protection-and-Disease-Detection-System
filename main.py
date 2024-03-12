import webbrowser

import kivy
import requests
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
from kivy.uix.image import Image
import os
import firebase_admin
from plyer import filechooser
from firebase_admin import credentials, firestore, storage
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from PIL import Image
import uuid
import re
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
import model


email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


global_user_id = None
disease_name = None

class Registration(Screen):

    def check_re(self, name, email, address, password):
        if self.ids.nameInput.text != "" and email.text != "" and self.ids.addressInput.text != "":
            if email_regex.match(email.text):
                self.submit()
                return True
            else:
                self.show_popup("Enter valid email")
        else:
            self.show_popup("Enter every details")

    def submit(self):
        global global_user_id
        global flg
        try:
            db = firestore.client()
            user_id = str(uuid.uuid4())
            global_user_id = user_id
            data = {
                'user_id': user_id,
                'name': self.ids.nameInput.text,
                'email': self.ids.emailInput.text,
                'address': self.ids.addressInput.text,
                'password': self.ids.passwordInput.text
            }

            data_cnt = {
                'cnt': 0,
                'counter': 0
            }
            db.collection('cnt').document(global_user_id).set(data_cnt)

            db.collection('users').add(data)
            self.show_popup("Success")
        except Exception as e:
            print(f"Error submitting data: {e}")

    def show_popup(self, title):
        self.content1 = Button(text='Close', on_press=self.dismiss_popup1)
        self.popup1 = Popup(title=title, content=self.content1,
                           size_hint=(None, None), size=(200, 100))
        self.popup1.open()

    def dismiss_popup1(self, instance):
        self.popup1.dismiss()

    def clear_text_inputs(self):
        self.ids.nameInput.text = ""
        self.ids.emailInput.text = ""
        self.ids.addressInput.text = ""
        self.ids.passwordInput.text = ""


class Login(Screen):
    global global_user_id

    def check_login(self, login_emailInput, login_passwordInput):
        global flg

        db = firestore.client()
        email = login_emailInput.text
        password = login_passwordInput.text
        user_ref = db.collection('users').where('email', '==', email).limit(1).get()
        if not user_ref:
            print("User with email {} does not exist.".format(email))
            return False
        user_data = user_ref[0].to_dict()
        stored_password = user_data.get('password', None)
        if stored_password is None:
            print("Password not found for user with email {}".format(email))
            return False
        if password == stored_password:
            print("Login successful!")
            global global_user_id
            global_user_id = user_data.get('user_id')
            App.get_running_app().root.current = 'home'
            return True
        else:
            print("Incorrect password for email {}".format(email))
            return False

    def clear_login_text_inputs(self):
        self.ids.login_emailInput.text = ""
        self.ids.login_passwordInput.text = ""

class Home(Screen):
    pass


class CameraCapture(Screen):
    image = None
    def capture_image(self, camera_widget):
        global global_user_id
        global image
        camera_texture = camera_widget.texture
        if camera_texture:
            buffer = camera_texture.pixels
            image = Image.frombytes('RGBA', camera_texture.size, buffer)

    def save_image(self):
        global global_user_id
        global image
        temp_image_path = "temp_image.png"
        image.save(temp_image_path)
        self.upload_to_firebase_storage(temp_image_path, global_user_id)

    def flip_image(self, camera):
        if camera.index == 0:
            camera.index = 2
        elif camera.index == 2:
            camera.index = 0
        else:
            camera.index = camera.index

    def upload_to_firebase_storage(self, image_path, user_id):
        global global_user_id
        bucket = storage.bucket('smart-fence-cd01a.appspot.com')
        filename = f"{global_user_id}_master.png"
        blob = bucket.blob(filename)
        blob.upload_from_filename(image_path)
        image_url = blob.public_url

        print("Image uploaded to", image_url)


class ImageUpload(Screen):
    def choose_image(self, selected_image):
        global global_user_id
        image_path = filechooser.open_file()
        if image_path:
            self.new_image_path = image_path[0]
            selected_image.source = self.new_image_path

    def save_uploaded_image(self):
        global global_user_id
        global cnt
        if hasattr(self, 'new_image_path') and self.new_image_path:
            filename = f"{global_user_id}_master.png"
            self.upload_to_firebase_storage(self.new_image_path, filename)

    def upload_to_firebase_storage(self, image_path, filename):
        bucket = storage.bucket("smart-fence-cd01a.appspot.com")
        blob = bucket.blob(filename)
        blob.upload_from_filename(image_path)

        print("Image uploaded to Firebase Storage with filename:", filename)


h_submitted_image = None


def download_image(url, filename):
    global global_user_id
    global h_submitted_image
    response = requests.get(url)
    db = firestore.client()
    compare_doc = db.collection('cnt').document(global_user_id).get()
    cnt = compare_doc.to_dict().get('cnt')
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        cnt += 1
        filename = '{}_{}.png'.format(global_user_id, cnt)
        upload_to_firebase_storage2("image.png", filename)
        db.collection('cnt').document(global_user_id).update({'cnt': cnt})
        h_submitted_image = f"https://firebasestorage.googleapis.com/v0/b/smart-fence-cd01a.appspot.com/o/{global_user_id}_{cnt}.png?alt=media"
    else:
        print("Failed to download image")

def upload_to_firebase_storage2(image_path, filename):
    bucket = storage.bucket("smart-fence-cd01a.appspot.com")
    blob = bucket.blob(filename)
    blob.upload_from_filename(image_path)

    print("Image uploaded to Firebase Storage with filename:", filename)


class Prediction(Screen):
    disease_name = None
    disease_cure = None

    def disease_pred(self, image_widget, label_widget):
        global global_user_id
        global disease
        global h_submitted_image
        global disease_cure
        db = firestore.client()
        compare_doc = db.collection('cnt').document(global_user_id).get()
        counter = compare_doc.to_dict().get('counter')
        image_url = f"https://firebasestorage.googleapis.com/v0/b/smart-fence-cd01a.appspot.com/o/{global_user_id}_master.png?alt=media&token=d5d07d17-465d-4b21-acf3-4b628500c7b7"
        Clock.schedule_once(lambda dt: self.update_image_source(image_widget, image_url), 0)
        # image_widget.source = image_url
        print(image_url)
        image_filename = "image.png"
        download_image(image_url, image_filename)
        disease_name = model.predict_disease("image.png")
        disease_cure = f"https://www.google.com/search?q=how+to+cure+{disease_name}+disese&rlz=1C1ONGR_enIN981IN981&oq=how+to+cure+{disease_name}+disese++&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCTQ3MDE2ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8"
        label_widget.text = disease_name
        data = {
            'user_id': global_user_id,
            'photo': h_submitted_image,
            'disease_name': disease_name,
            'cure_discription': disease_cure
        }
        counter += 1
        xyz = f"{global_user_id}_{counter}"
        db.collection('data').document(xyz).set(data)
        db.collection('cnt').document(global_user_id).update({'counter': counter})

    def update_image_source(self, image_widget, image_url):
        image_widget.source = image_url


    def on_link_click(self, label_widget, instance, touch, *args):
        global disease_cure
        if instance.collide_point(*touch.pos):
            webbrowser.open(disease_cure)


class History(Screen):
    cure_description1 = ""
    cure_description2 = ""
    cure_description3 = ""
    cure_description4 = ""
    cure_description5 = ""
    def load_images(self, h_img1, h_img2, h_img3, h_img4, h_img5, ind1, ind2, ind3, ind4, ind5):

        global global_user_id
        global cure_description1
        global cure_description2
        global cure_description3
        global cure_description4
        global cure_description5
        db = firestore.client()

        compare_doc = db.collection('cnt').document(global_user_id).get()
        counter = compare_doc.to_dict().get('counter')

        # 1
        document_name1 = f"{global_user_id}_{counter}"
        doc_ref1 = db.collection('data').document(document_name1)
        doc1 = doc_ref1.get()
        data1 = doc1.to_dict()
        cure_description1 = data1.get('cure_discription')
        disease_name1 = data1.get('disease_name')
        photo1 = data1.get('photo')
        h_img1.source = photo1
        ind1.text = "1. " + disease_name1
        print(cure_description1)
        print(disease_name1)
        print(photo1)

        # 2
        counter = counter - 1
        document_name2 = f"{global_user_id}_{counter}"
        doc_ref2 = db.collection('data').document(document_name2)
        doc2 = doc_ref2.get()
        data2 = doc2.to_dict()
        cure_description2 = data2.get('cure_discription')
        disease_name2 = data2.get('disease_name')
        photo2 = data2.get('photo')
        h_img2.source = photo2
        ind2.text = "2. " + disease_name2
        print(cure_description2)
        print(disease_name2)
        print(photo2)

        # 3
        counter = counter - 1
        document_name3 = f"{global_user_id}_{counter}"
        doc_ref3 = db.collection('data').document(document_name3)
        doc3 = doc_ref3.get()
        data3 = doc3.to_dict()
        cure_description3 = data3.get('cure_discription')
        disease_name3 = data3.get('disease_name')
        photo3 = data3.get('photo')
        h_img3.source = photo3
        ind3.text = "3. " + disease_name3
        print(cure_description3)
        print(disease_name3)
        print(photo3)

        # 4
        counter = counter - 1
        document_name4 = f"{global_user_id}_{counter}"
        doc_ref4 = db.collection('data').document(document_name4)
        doc4 = doc_ref4.get()
        data4 = doc4.to_dict()
        cure_description4 = data4.get('cure_discription')
        disease_name4 = data4.get('disease_name')
        photo4 = data4.get('photo')
        h_img4.source = photo4
        ind4.text = "4. " + disease_name4
        print(cure_description4)
        print(disease_name4)
        print(photo4)

        # 5
        counter = counter - 1
        document_name5 = f"{global_user_id}_{counter}"
        doc_ref5 = db.collection('data').document(document_name5)
        doc5 = doc_ref5.get()
        data5 = doc5.to_dict()
        cure_description5 = data5.get('cure_discription')
        disease_name5 = data5.get('disease_name')
        photo5 = data5.get('photo')
        h_img5.source = photo5
        ind5.text = "5. " + disease_name5
        print(cure_description5)
        print(disease_name5)
        print(photo5)


    def on_link_click1(self, instance, touch, *args):
        global cure_description1
        if instance.collide_point(*touch.pos):
            webbrowser.open(cure_description1)


    def on_link_click2(self, instance, touch, *args):
        global cure_description2
        if instance.collide_point(*touch.pos):
            webbrowser.open(cure_description2)

    def on_link_click3(self, instance, touch, *args):
        global cure_description3
        if instance.collide_point(*touch.pos):
            webbrowser.open(cure_description3)

    def on_link_click4(self, instance, touch, *args):
        global cure_description4
        if instance.collide_point(*touch.pos):
            webbrowser.open(cure_description4)

    def on_link_click5(self, instance, touch, *args):
        global cure_description5
        if instance.collide_point(*touch.pos):
            webbrowser.open(cure_description5)


class FarmImages(Screen):
    def load_farmImages(self, f_img1, f_img2, f_img3, f_img4, f_img5):
        global global_user_id
        user_id = "56d5b593-b18d-40ff-b0f2-f2528a253a23"
        bucket = storage.bucket()
        blobs = bucket.list_blobs(prefix=user_id + "_F")
        print(blobs)
        image_names = [blob.name for blob in blobs]
        image_numbers = [int(name.split('_F')[1].split('.')[0]) for name in image_names]
        sorted_indices = sorted(range(len(image_numbers)), key=lambda k: image_numbers[k], reverse=True)
        last_five_indices = sorted_indices[:5]
        last_five_images = [image_names[i] for i in last_five_indices]

        image_url0 = f"https://firebasestorage.googleapis.com/v0/b/smart-fence-cd01a.appspot.com/o/{last_five_images[0]}?alt=media"
        image_url1 = f"https://firebasestorage.googleapis.com/v0/b/smart-fence-cd01a.appspot.com/o/{last_five_images[1]}?alt=media"
        image_url2 = f"https://firebasestorage.googleapis.com/v0/b/smart-fence-cd01a.appspot.com/o/{last_five_images[2]}?alt=media"
        image_url3 = f"https://firebasestorage.googleapis.com/v0/b/smart-fence-cd01a.appspot.com/o/{last_five_images[3]}?alt=media"
        image_url4 = f"https://firebasestorage.googleapis.com/v0/b/smart-fence-cd01a.appspot.com/o/{last_five_images[4]}?alt=media"

        print(image_url0, image_url1, image_url2, image_url3, image_url4)

        f_img1.source = image_url0
        f_img2.source = image_url1
        f_img3.source = image_url2
        f_img4.source = image_url3
        f_img5.source = image_url4

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class CodeUnnati(App):
    def build(self):
        Window.size = (640, 1136)
        cred = credentials.Certificate("./google.json")
        firebase_admin.initialize_app(cred, {'storageBucket': 'smart-fence-cd01a.appspot.com'})
        return kv


if __name__ == "__main__":
    CodeUnnati().run()