import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import threading
import socket

host = '81.7.7.146'
port = 1234

kivy.require("1.9.0")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class MyRoot(BoxLayout):

    def __init__(self):
        super(MyRoot, self).__init__()

    def send_message(self):
        client.send(f"{self.nickname_text.text}: {self.message_text.text}".encode('utf-8'))

    def connect_to_server(self):
        if self.nickname_text != "":
            client.connect((self.ip_text.text, 1234))
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                client.send(self.nickname_text.text.encode('utf-8'))
                self.send_btn.disabled = False
                self.message_text.disabled = False
                self.connect_btn.disabled = True
                self.ip_text.disabled = True

                self.make_invisible(self.connection_grid)
                self.make_invisible(self.connect_btn)

                thread = threading.Thread(target=self.receive)
                thread.start()

    def make_invisible(self, widget):
        widget.visible = False
        widget.size_hint_x = None
        widget.size_hint_y = None
        widget.height = 0
        widget.width = 0
        widget.text = ""
        widget.opacity = 0

    def receive(self):
        stop = False
        while not stop:
            try:
                message = client.recv(1024).decode('utf-8')
                self.chat_text.text += message + "\n"
            except:
                print("ERROR")
                client.close()
                stop = True


class AndroidClient(App):

    def build(self):
        return MyRoot()


AndroidClient = AndroidClient()
AndroidClient.run()
