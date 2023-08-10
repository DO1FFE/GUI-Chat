import threading
import socket
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

host = '81.7.7.146'
port = 1234

class ChatApp(App):

    def build(self):
        self.client = Client(host, port, self.display_message)
        self.layout = BoxLayout(orientation='vertical')

        # Chat display
        self.chat_label = Label(size_hint_y=None, height=44, text="Chat:")
        self.messages = ScrollView()
        self.chat_history = Label(size_hint_y=None)
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        self.messages.add_widget(self.chat_history)
        self.layout.add_widget(self.chat_label)
        self.layout.add_widget(self.messages)

        # Input and send button
        self.message_input = TextInput(hint_text="Nachricht:")
        self.send_button = Button(text="Senden", on_press=self.send_message)
        input_layout = BoxLayout(orientation='horizontal')
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(self.send_button)
        self.layout.add_widget(input_layout)

        return self.layout

    def send_message(self, instance):
        message = self.message_input.text
        self.client.write(message)
        self.message_input.text = ''

    def display_message(self, message):
        self.chat_history.text += '\n' + message


class Client:

    def __init__(self, host, port, message_callback):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.nickname = input("Bitte Nicknamen wählen: ")
        self.message_callback = message_callback
        self.running = True
        threading.Thread(target=self.receive).start()

    def write(self, message):
        full_message = f"{self.nickname}: {message}"
        self.sock.send(full_message.encode('utf-8'))

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    self.message_callback(message)
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break


if __name__ == "__main__":
    ChatApp().run()
