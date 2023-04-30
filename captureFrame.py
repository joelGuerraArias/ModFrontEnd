import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


class VideoCapture:
    def __init__(self, video_source):
        self.cap = cv2.VideoCapture(video_source)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.current_frame = 0

    def release(self):
        if self.cap is not None:
            self.cap.release()

    def get_frame(self):
        if self.cap is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
            ret, frame = self.cap.read()
            if ret:
                self.current_frame += self.fps * 30  # Saltar 30 segundos
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                self.release()
                return ret, None
        else:
            return False, None


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Cargar video
        self.video_source = filedialog.askopenfilename()
        self.vid = VideoCapture(self.video_source)

        # Crear directorio de capturas en el escritorio
        self.save_dir = os.path.join(
            os.path.expanduser("~"), "Desktop", "capturas")
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        # Configurar la ventana
        self.canvas = tk.Canvas(window, width=self.vid.cap.get(
            cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.delay = int(1000/self.vid.fps)
        self.update()

        self.window.mainloop()

    def capture(self):
        ret, frame = self.vid.get_frame()
        if ret and frame is not None:
            filename = os.path.join(
                self.save_dir, "fotograma_%d.png" % self.vid.current_frame)
            print("Guardando en", filename)
            cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        self.capture()
        ret, frame = self.vid.get_frame()
        if ret and frame is not None:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)

    def __del__(self):
        self.vid.release()


App(tk.Tk(), "Tkinter Video Capture")
