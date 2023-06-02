from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle,RoundedRectangle
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from kivy.uix.filechooser import FileChooserIconView,FileChooser
from shutil import copyfile


import pyaudio
import wave
import speech_recognition as sr
import csv
import os
import pandas as pd



def show_popup(message, title):
    label = Label(text=message)
    popup = Popup(title=title, content=label, size_hint=(None, None), size=(400, 200))
    popup.open()


def recorder(x):
    chunk = 1024  
    sample_format = pyaudio.paInt16 
    channels = 1
    fs = 44100  
    seconds = 5
    p = pyaudio.PyAudio()
    print('Recording...')
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()  
    print('Finished recording.')
    wf = wave.open(f"voice/{x}.wav", 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    return voice_to_text(f"voice/{x}.wav")

def voice_to_text(x):
    r = sr.Recognizer()
    audio_path = x
    print(x)
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        return text
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return "error1"
    except sr.RequestError as e:
        print(f"Error: {e}")
        return "error1"

class Header(BoxLayout):
    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.size_hint_y = 0.08
        self.bind(pos=self.update_header_background, size=self.update_header_background)
        # Set background color
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Black color
            self.header_background = Rectangle(pos=self.pos, size=self.size)



        logo_image = Image(source='logo_sr.jpg', size_hint=(None, None), size=(200, 300))
        self.add_widget(logo_image)  # Add the image widget directly

        self.add_widget(Label(text='SRSS', color=(1, 1, 1, 1), bold=True))  # White color and bold text

        # Add buttons with custom style
        button_style = {
            'background_normal': '',
            'background_color': (0, 0, 0, 1),  # Black color
            'color': (1, 1, 1, 1),  # White color
            'underline': True,
            'font_size': '14sp',  # Adjust the font size as desired
        }

        self.home_button = Button(text='Home', **button_style)
        self.home_button.bind(on_press=self.home)
        self.add_widget(self.home_button)

        self.about_button = Button(text='About', **button_style)
        self.about_button.bind(on_press=self.about)
        self.add_widget(self.about_button)

        self.contact_button = Button(text='Contact Us', **button_style)
        self.contact_button.bind(on_press=self.contact)
        self.add_widget(self.contact_button)
    
    def home(self,instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(Header(size_hint_y=.1))
        app.root.add_widget(SignInPage(size_hint_y=.5))
        app.root.add_widget(extra(size_hint_y=.3))
        app.root.add_widget(Footer(size_hint_y=0.1))

    def about(self,instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(Header(size_hint_y=.1))
        app.root.add_widget(about(size_hint_y=.5))
        app.root.add_widget(extra(size_hint_y=.3))
        app.root.add_widget(Footer(size_hint_y=0.1))   

    def contact(self,instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(Header(size_hint_y=.1))
        app.root.add_widget(contact(size_hint_y=.5))
        app.root.add_widget(extra(size_hint_y=.3))
        app.root.add_widget(Footer(size_hint_y=0.1))      

    def update_header_background(self, *args):
        self.header_background.pos = self.pos
        self.header_background.size = self.size



           
class about(BoxLayout):
    def __init__(self, **kwargs):
        super(about, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 15
        self.padding=[10,10,10,10]
        self.add_widget(Label(text='Our app is based on security system, you can secure any', size_hint_y=0.057, bold=True, font_size='24sp',color=(0,0,0,1))) 
        self.add_widget(Label(text='  images file PDF with our application. The most important thing', size_hint_y=0.057, bold=True, font_size='24sp',color=(0,0,0,1)))
        self.add_widget(Label(text='about our app is that we are using voice authentication as a ', size_hint_y=0.057, bold=True, font_size='24sp',color=(0,0,0,1)))
        self.add_widget(Label(text='password and our service is available on both website and application.', size_hint_y=0.057, bold=True, font_size='24sp',color=(0,0,0,1))) 
        self.add_widget(Label(text='To use our app you simply have to register and after registration you ', size_hint_y=0.057, bold=True, font_size='24sp',color=(0,0,0,1)))
        self.add_widget(Label(text='simply login and store your voice and after that you will reach our ', size_hint_y=0.057, bold=True, font_size='24sp',color=(0,0,0,1)))
        self.add_widget(Label(text='dashboard and after that you can store any of your images file', size_hint_y=0.057, bold=True, font_size='24sp',color=(0,0,0,1)))
        self.add_widget(Label(text=' pdf there.', size_hint_y=0.057, bold=True, font_size='24sp',color=(0,0,0,1)))  
        self.add_widget(Label(text=' ', size_hint_y=0.1, bold=True, font_size='50sp',color=(0,0,0,1)))   
        self.add_widget(Label(text="Developer name",size_hint_y=0.06667, bold=True, font_size='32sp',color=(0,0,0,1)))
        self.add_widget(Label(text="1 Anurag shukla (Assistant Prof.)",size_hint_y=0.0667, bold=True, font_size='32sp',color=(0,0,0,1)))
        self.add_widget(Label(text="2 Deepshikha Tiwari",size_hint_y=0.0667, bold=True, font_size='32sp',color=(0,0,0,1)))
        self.add_widget(Label(text="3 Swarnakala Singh",size_hint_y=0.0667, bold=True, font_size='32sp',color=(0,0,0,1)))
        self.add_widget(Label(text="4 Prabhat Verma",size_hint_y=0.0667, bold=True, font_size='32',color=(0,0,0,1)))
        self.add_widget(Label(text="5 Anshika Tiwari",size_hint_y=0.0667, bold=True, font_size='32',color=(0,0,0,1)))


class contact(BoxLayout):
    def __init__(self, **kwargs):
        super(contact, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding=[10,10,10,10]

        self.add_widget(Label(text='Contact Details',size_hint_y=0.3, bold=True, font_size='24sp',color=(0,0,0,1)))
        self.add_widget(Label(text='Email Id = prabhatv93540@gmail.com',size_hint_y=0.3, bold=True, font_size='24sp',color=(0,0,0,1)))
        self.add_widget(Label(text='Contact No = 9354090635',size_hint_y=0.3, bold=True, font_size='24sp',color=(0,0,0,1)))


class extra(BoxLayout):
    def __init__(self, **kwargs):
        super(extra, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.add_widget(Label(text='', size_hint_y=0.2, bold=True, font_size='24sp'))  # About section label

class welcome(BoxLayout):
    def __init__(self,name='', **kwargs):
        super(welcome, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.size_hint_y = 0.1
        self.padding=[10,10,10,20]

        self.add_widget(Label(text=f'WELCOME,{name}', size_hint_y=0.2, bold=True, font_size='36sp',color=(0, 0, 0, 1)))  # About section label


class SignInPage(ScrollView):
    def __init__(self, **kwargs):
        super(SignInPage, self).__init__(**kwargs)
        
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[140, 40, 140, 20])
        self.username = ''
        self.password = ''

        # Set background color
        # self.background_color = (1, 1, 1, 1)  # White color

        with self.layout.canvas.before:
            # Load the background image
            self.bg_image = RoundedRectangle(source='login1.jpg', pos=self.pos, size=self.size,radius=[20])

        self.layout.bind(pos=self.update_background, size=self.update_background)

        self.layout.add_widget(Label(text='Sign In', size_hint_y=0.2, bold=True, font_size='36sp', color=(0, 0, 0, 1)))  # Sign-in heading

        self.username_input = TextInput(hint_text='Username', size_hint_y=0.3)  # Black color for the input background
        self.layout.add_widget(self.username_input)

        self.password_button = Button(text='Voice Recording for Password', background_color=(0.5, 0.5, 0.5, 1), size_hint_y=0.3)  # Gray color for the button
        self.password_button.bind(on_press=self.password1)
        self.layout.add_widget(self.password_button)

        self.submit_button = Button(text='Submit', background_color=(0, 1, 0, 1), color=(1, 1, 1, 1), size_hint_y=0.3)  # Green color for the button
        self.submit_button.bind(on_press=self.match)
        self.layout.add_widget(self.submit_button)

        self.signup_label = Label(text="Don't have an account? Sign up", bold=True, color=(0, 0, 0, 1), size_hint_y=0.3)  # Black color and bold text
        self.signup_label.bind(on_touch_down=self.switch_to_signup)
        self.layout.add_widget(self.signup_label)

        self.add_widget(self.layout)

    def switch_to_signup(self, instance, touch):
        if self.signup_label.collide_point(*touch.pos):
            app = App.get_running_app()
            app.root.clear_widgets()
            app.root.add_widget(Header(size_hint_y=.1))
            app.root.add_widget(SignUpPage(size_hint_y=.6))
            app.root.add_widget(extra(size_hint_y=.2))
            app.root.add_widget(Footer(size_hint_y=0.1))

    def password1(self, instance):
        self.username = self.username_input.text
        self.password = recorder(self.username)
        print(self.password)
        if self.password == "error1":
            message = "Please record your voice again"
        else:
            message = "Voice recorded successfully"
        show_popup(message, "voice")

    def match(self, instance):
        register_data = pd.read_csv("register.csv")
        if self.username not in register_data['username'].values:
            message = "Username is not correct"
            show_popup(message, "username")
        else:
            register_data = register_data.values
            for i in register_data:
                if i[2] == self.username and i[3] == self.password:
                    print("login")
                    app = App.get_running_app()
                    app.root.clear_widgets()
                    app.root.add_widget(welcome(name=i[0],size_hint_y=0.1))
                    app.root.add_widget(data(username=self.username,size_hint_y=0.4))
                    app.root.add_widget(displayfiles(username=self.username,size_hint_y=0.27)) 
                    app.root.add_widget(extra(size_hint_y=0.23))
                    # Add the appropriate widget here for the successful sign-in state

    def update_background(self, *args):
        content_x = self.layout.x + self.layout.padding[0] - 20
        content_y = self.layout.y + self.layout.padding[1] - 20
        content_width = self.layout.width - sum(self.layout.padding[::2]) + 50
        content_height = self.layout.height - sum(self.layout.padding[1::2]) + 20

        # Update the position and size of the background image
        self.bg_image.pos = content_x, content_y
        self.bg_image.size = content_width, content_height
        self.bg_image.radius=[20]


class data(ScrollView):
    def __init__(self,username="", **kwargs):
        super(data, self).__init__(**kwargs)
        
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[170, 40, 170, 20])

        # Set background color
        # self.background_color = (1, 1, 1, 1)  # White color
        self.username=username
        with self.layout.canvas.before:
            # Load the background image
            self.bg_image = RoundedRectangle(source='login1.jpg', pos=self.pos, size=self.size,radius=[20])

        self.layout.bind(pos=self.update_background, size=self.update_background)

        self.layout.add_widget(Label(text=f'UPLOAD FILES ', size_hint_y=0.2, bold=True, font_size='36sp', color=(0, 0, 0, 1)))  # Sign-in heading

        self.password_button = Button(text='Select File', background_color=(0.5, 0.5, 0.5, 1), size_hint_y=0.3)  # Gray color for the button
        self.password_button.bind(on_press=self.select_file)
        self.layout.add_widget(self.password_button)

        self.submit_button = Button(text='Submit', background_color=(0, 1, 0, 1), color=(1, 1, 1, 1), size_hint_y=0.3)  # Green color for the button
        self.submit_button.bind(on_press=self.upload_file)
        self.layout.add_widget(self.submit_button)

        self.signup_label = Label(text="Go to Home", bold=True, color=(0, 0, 0, 1), size_hint_y=0.3)  # Black color and bold text
        self.signup_label.bind(on_touch_down=self.switch_to_signup)
        self.layout.add_widget(self.signup_label)

        self.add_widget(self.layout)
    def select_file(self, button):
        file_chooser = FileChooserIconView()
        file_chooser.bind(on_submit=self.select_file_name, on_cancel=self.cancel_selection)

        # OK button for file selection
        ok_button = Button(text='OK', size_hint=(None, None), size=(150, 50))
        ok_button.bind(on_release=lambda btn: self.select_file_name(file_chooser))

        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup_content.add_widget(file_chooser)
        popup_content.add_widget(ok_button)

        self.popup = Popup(title='Select a File', content=popup_content, size_hint=(0.7, 0.7))
        self.popup.open()

    def select_file_name(self, file_chooser):
        self.selected_file = file_chooser.selection[0]
        print(f"Selected file: {self.selected_file}")

        self.popup.dismiss()

    def upload_file(self, button):
        if self.selected_file:
            current_dir = os.getcwd()
            file_name = os.path.basename(self.selected_file)
            destination_file = f"data/{self.username}/{file_name}"

            copyfile(self.selected_file, destination_file)
            print(f"File saved to: {destination_file}")

    def cancel_selection(self, file_chooser):
        self.popup.dismiss()    

    def switch_to_signup(self, instance, touch):
        if self.signup_label.collide_point(*touch.pos):
            app = App.get_running_app()
            app.root.clear_widgets()
            app.root.add_widget(Header(size_hint_y=.1))
            app.root.add_widget(SignInPage(size_hint_y=.5))
            app.root.add_widget(extra(size_hint_y=.3))
            app.root.add_widget(Footer(size_hint_y=0.1))


    def update_background(self, *args):
        content_x = self.layout.x + self.layout.padding[0] - 20
        content_y = self.layout.y + self.layout.padding[1] - 20
        content_width = self.layout.width - sum(self.layout.padding[::2]) + 50
        content_height = self.layout.height - sum(self.layout.padding[1::2]) + 20

        # Update the position and size of the background image
        self.bg_image.pos = content_x, content_y
        self.bg_image.size = content_width, content_height
        self.bg_image.radius=[20]



class SignUpPage(ScrollView):
    def __init__(self, **kwargs):
        super(SignUpPage, self).__init__(**kwargs)
        
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[130, 40, 140, 20])
        self.register_data = pd.read_csv("register.csv")
        self.username = ''
        self.password = ''
        self.name = ''
        self.email = ''

        # Set background color
        # self.background_color = (1, 1, 1, 1)  # White color
        with self.layout.canvas.before:
            # Load the background image
            self.bg_image = RoundedRectangle(source='login1.jpg', pos=self.pos, size=self.size,radius=[20])

        self.layout.bind(pos=self.update_background, size=self.update_background)

        self.layout.add_widget(Label(text='Sign Up', size_hint_y=0.2, bold=True, font_size='36sp',color=(0, 0, 0, 1)))  # Sign-up heading

        self.name_input = TextInput(hint_text='Name',  size_hint_y=0.3)  # Black color for the input background
        self.layout.add_widget(self.name_input)

        self.email_input = TextInput(hint_text='Email',  size_hint_y=0.3)  # Black color for the input background
        self.layout.add_widget(self.email_input)

        self.username_input = TextInput(hint_text='Username', size_hint_y=0.3)  # Black color for the input background
        self.layout.add_widget(self.username_input)

        self.password_button = Button(text='Voice Recording for Password', background_color=(0.5, 0.5, 0.5, 1), size_hint_y=0.3)  # Gray color for the button
        self.password_button.bind(on_press=self.password2)
        self.layout.add_widget(self.password_button)

        self.submit_button = Button(text='Submit', background_color=(0, 0.6, 0, 1), size_hint_y=0.3)  # Green color for the button
        self.submit_button.bind(on_press=self.match)
        self.layout.add_widget(self.submit_button)

        self.signup_label = Label(text="Already an account? Sign in", bold=True, color=(0, 0, 0, 1), size_hint_y=0.3)  # Black color and bold text
        self.signup_label.bind(on_touch_down=self.switch_to_signin)
        self.layout.add_widget(self.signup_label)

        self.add_widget(self.layout)

    def password2(self, instance):
        self.password = recorder(self.username)
        print(self.password)
        if self.password == "error1":
            message = "Please record your voice again"
        else:
            message = "Voice recorded successfully"
        show_popup(message, "voice")

    def match(self, instance):
        self.name = self.name_input.text
        self.email = self.email_input.text
        self.username = self.username_input.text        
        if self.username in self.register_data['username'].values:
            message = "Username already exists"
            show_popup(message, "username")
        else:    
            with open('register.csv', 'a', newline="") as file:
                writer = csv.writer(file)
                writer.writerow([self.name, self.email, self.username, self.password])
            os.makedirs(f"data/{self.username}")    
            show_popup("Account Created Successfully", 'Account')
            self.name_input.text=''
            self.email_input.text=""
            self.username_input.text=''

    def update_background(self, *args):
        content_x = self.layout.x + self.layout.padding[0] - 20
        content_y = self.layout.y + self.layout.padding[1] - 20
        content_width = self.layout.width - sum(self.layout.padding[::2]) + 50
        content_height = self.layout.height - sum(self.layout.padding[1::2]) + 20

        # Update the position and size of the background image
        self.bg_image.pos = content_x, content_y
        self.bg_image.size = content_width, content_height
        self.bg_image.radius = [20]
        
    def switch_to_signin(self, instance, touch):
        if self.signup_label.collide_point(*touch.pos):
            app = App.get_running_app()
            app.root.clear_widgets()
            app.root.add_widget(Header(size_hint_y=.1))
            app.root.add_widget(SignInPage(size_hint_y=.5))
            app.root.add_widget(extra(size_hint_y=.3))
            app.root.add_widget(Footer(size_hint_y=0.1))    

         
class Footer(BoxLayout):
    def __init__(self, **kwargs):
        super(Footer, self).__init__(**kwargs)
        button_style = {
            'color': (1, 1, 1, 1),  # White color
            'underline': True,
            'font_size': '14sp',  # Adjust the font size as desired
        }
        self.orientation = 'horizontal'
        self.spacing = 10
        self.size_hint_y = 0.07

        with self.canvas.before:
            Color(0, 0, 0, 1)  # Black color
            self.background = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_background, size=self.update_background)

        self.add_widget(Label(text='© 2023 SRSS', **button_style))

    def update_background(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size


class displayfiles(BoxLayout):
    def __init__(self, username="",**kwargs):
        super(displayfiles, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[190, 10, 190, 40])
        self.path=f"data/{username}"

        self.password_button = Button(text='VIEW ALL UPLOADED FILES', background_color=(0.5, 0.5, 0.5, 1), size_hint_y=0.3)  # Gray color for the button
        self.password_button.bind(on_press=self.select_file)
        self.layout.add_widget(self.password_button)

        self.submit_button = Button(text='SHOW FILE', background_color=(0, 1, 0, 1), color=(1, 1, 1, 1), size_hint_y=0.3)  # Green color for the button
        self.submit_button.bind(on_press=self.display_file)
        self.layout.add_widget(self.submit_button)

        self.add_widget(self.layout)

    def select_file(self, button):
        file_chooser = FileChooserIconView(path=self.path)
        file_chooser.bind(on_submit=self.select_file_name, on_cancel=self.cancel_selection)

        # OK button for file selection
        ok_button = Button(text='OK', size_hint=(None, None), size=(150, 50))
        ok_button.bind(on_release=lambda btn: self.select_file_name(file_chooser))

        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup_content.add_widget(file_chooser)
        popup_content.add_widget(ok_button)

        self.popup = Popup(title='ALL FILES', content=popup_content, size_hint=(0.9, 0.9))
        self.popup.open()

    def select_file_name(self, file_chooser):
        self.selected_file = file_chooser.selection[0]
        print(self.selected_file)

        self.popup.dismiss()

    def display_file(self, button):
        pop = Popup(title='test', content=Image(source=self.selected_file),
                    size_hint=(None, None), size=(400, 400))
        pop.open()

    def cancel_selection(self, file_chooser):
        self.popup.dismiss()


class MyApp(App):
    def build(self):
        main_layout = GridLayout(cols=1)

        header = Header(size_hint_y=.1)
        main_layout.add_widget(header)

        main_layout.add_widget(SignInPage(size_hint_y=.5))
        main_layout.add_widget(extra(size_hint_y=.3))

        footer = Footer(size_hint_y=.1)
        main_layout.add_widget(footer)

        Window.clearcolor = (0, 255, 255, 1) 

        return main_layout


if __name__ == '__main__':
    MyApp().run()
