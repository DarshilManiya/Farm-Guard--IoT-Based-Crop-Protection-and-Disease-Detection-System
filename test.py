import firebase_admin
from firebase_admin import credentials, storage
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

# cred = credentials.Certificate("google.json")
# firebase_admin.initialize_app(cred, {'storageBucket': 'smart-fence-cd01a.appspot.com'})


def build(user_id):
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix=user_id + "_F")
    image_names = [blob.name for blob in blobs]
    image_numbers = [int(name.split('_F')[1].split('.')[0]) for name in image_names]
    sorted_indices = sorted(range(len(image_numbers)), key=lambda k: image_numbers[k], reverse=True)
    last_five_indices = sorted_indices[:5]
    last_five_images = [image_names[i] for i in last_five_indices]

    l1 = []

    l1[0] = f"https://firebasestorage.googleapis.com/v0/b/smart-fence-cd01a.appspot.com/o/{last_five_images[0]}?alt=media"
    l1[1] = f"https://firebasestorage.googleapis.com/v0/b/smart-fence-cd01a.appspot.com/o/{last_five_images[1]}?alt=media"
    l1[2] = f"https://firebasestorage.googleapis.com/v0/b/smart-fence-cd01a.appspot.com/o/{last_five_images[2]}?alt=media"
    l1[3] = f"https://firebasestorage.googleapis.com/v0/b/smart-fence-cd01a.appspot.com/o/{last_five_images[3]}?alt=media"
    l1[4] = f"https://firebasestorage.googleapis.com/v0/b/smart-fence-cd01a.appspot.com/o/{last_five_images[4]}?alt=media"

    return  l1
