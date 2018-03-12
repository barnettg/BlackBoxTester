from tkinter import *
from tkinter import Label
from tkinter import Button
import time
import socket

class TrafficGUI:
    def __init__(self, master):
        self.master = master
        master.title("Traffic Lights GUI")

        self.id_ns_top = None
        self.id_ns_mid = None
        self.id_ns_bot = None
        self.signal_ns = None
        self.signal_ew = None

        self.train_coming_flag = False
        self.light_error_flag = False
        self.car_waiting_ew_flag = False
        self.car_waiting_ns_flag = False

        self.cv = Canvas(self.master, width = 850, height = 400)
        self.cv.pack()

        self.label_train = self.cv.create_text((200, 50), text="")
        self.label_Car_Waiting_NS = self.cv.create_text((200, 70), text="")
        self.label_Car_Waiting_EW = self.cv.create_text((200, 90), text="")
        self.label_error = self.cv.create_text((200, 110), text="")

        self.frame_buttons = Frame(root)
        self.frame_buttons.pack( side = BOTTOM)

        self.label = Label(self.frame_buttons, text=("IP: " + socket.gethostbyname(socket.gethostname())) )
        self.label.pack(side = LEFT, padx=5, pady=5 )

        self.change_button = Button(self.frame_buttons, text="Change", command=self.change)
        self.change_button.pack(side = LEFT, padx=5, pady=5  )

        self.train_button = Button(self.frame_buttons, text="Train", command=self.train)
        self.train_button.pack(side = LEFT, padx=5, pady=5  )

        self.error_button = Button(self.frame_buttons, text="Error", command=self.light_error)
        self.error_button.pack(side = LEFT, padx=5, pady=5 )

        self.carEW_button = Button(self.frame_buttons, text="Car EW", command=self.car_ew)
        self.carEW_button.pack(side = LEFT, padx=5, pady=5  )

        self.carNS_button = Button(self.frame_buttons, text="Car NS", command=self.car_ns)
        self.carNS_button.pack(side = LEFT, padx=5, pady=5  )

        self.create_street()

        #self.close_button = Button(master, text="Close", command=master.quit)
        #self.close_button.pack()

    def change(self):
        print("change!")
        self.set_lights("red", "red")

    def train(self):
        print("train!")
        if self.train_coming_flag is False:
            self.cv.itemconfig(self.label_train, text="Train coming!")
            self.train_coming_flag = True
        else:
            self.cv.itemconfig(self.label_train, text="")
            self.train_coming_flag = False

    def light_error(self):
        print("error!")
        if self.light_error_flag is False:
            self.cv.itemconfig(self.label_error, text="Error!")
            self.light_error_flag = True
        else:
            self.cv.itemconfig(self.label_error, text="")
            self.light_error_flag = False

    def car_ew(self):
        print("car_ew!")
        if self.car_waiting_ew_flag is False:
            self.cv.itemconfig(self.label_Car_Waiting_EW, text="Car Waiting EW")
            self.car_waiting_ew_flag = True
        else:
            self.cv.itemconfig(self.label_Car_Waiting_EW, text="")
            self.car_waiting_ew_flag = False

    def car_ns(self):
        print("car_ns!")
        if self.car_waiting_ns_flag is False:
            self.cv.itemconfig(self.label_Car_Waiting_NS, text="Car Waiting NS")
            self.car_waiting_ns_flag = True
        else:
            self.cv.itemconfig(self.label_Car_Waiting_NS, text="")
            self.car_waiting_ns_flag = False

    def set_lights(self, ns, ew):
        # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/colors.html
        if ns is "red":
            self.cv.itemconfig(self.id_ns_top, fill="red")  # change color


    def create_street(self):
        # ns signal
        self.make_signal_ns(480, 10)
        self.cv.create_text((450, 100), text="NS")
        self.cv.create_line(430, 50, 430, 100)
        self.cv.create_line(430, 50, 420, 70)
        self.cv.create_line(430, 50, 440, 70)
        self.cv.create_line(430, 100, 420, 80)
        self.cv.create_line(430, 100, 440, 80)

        # ew signal
        self.make_signal_ew(200, 220)
        self.cv.create_text((260, 250), text="EW")
        self.cv.create_line(250, 280, 300, 280)
        self.cv.create_line(250, 280, 270, 270)
        self.cv.create_line(250, 280, 270, 290)
        self.cv.create_line(300, 280, 280, 270)
        self.cv.create_line(300, 280, 280, 290)

        # street
        self.cv.create_line(100, 150, 350, 150)
        self.cv.create_line(100, 200, 350, 200)
        self.cv.create_line(400, 150, 650, 150)
        self.cv.create_line(400, 200, 650, 200)
        self.cv.create_line(350, 0, 350, 150)
        self.cv.create_line(400, 0, 400, 150)
        self.cv.create_line(350, 200, 350, 350)
        self.cv.create_line(400, 200, 400, 350)

    def make_signal_ns(self, location_x, location_y):
        self.signal_ns = Signal(self.cv)
        self.signal_ns.make(0,0)
        self.signal_ns.set_red(True)
        #self.signal_ns.set_yellow(True)
        self.signal_ns.move(location_x,location_y)
        return 0

    def make_signal_ew(self, location_x, location_y):
        self.signal_ew = Signal(self.cv)
        self.signal_ew.make(0,0)
        self.signal_ew.set_red(True)
        self.signal_ew.move(location_x,location_y)
        return 0

    def move_signal(self, signal):
        pass

class Signal:
    def __init__(self, canvas_id):
        self.canvas = canvas_id
        self.circle_size = 30
        self.box_width = 40
        self.box_height = 123
        self.cir1_y = 10
        self.cir2_y = 48
        self.cir3_y = 85
        self.location_x = 10
        self.location_y = 10

    def make(self, location_x, location_y):
        self.id_box = self.canvas.create_rectangle(location_x, location_y,
                                          location_x + self.box_width,
                                          location_y + self.box_height,
                                          fill = 'black')

        self.id_top = self.canvas.create_oval(location_x + 5,
                                     location_y + self.cir1_y,
                                     location_x + 5 + self.circle_size,
                                     location_y + self.cir1_y + self.circle_size,
                                     fill = 'red')

        self.id_mid = self.canvas.create_oval(location_x + 5,
                                     location_y + self.cir2_y,
                                     location_x + 5 + self.circle_size,
                                     location_y + self.cir2_y + self.circle_size,
                                     fill = 'yellow')

        self.id_bot = self.canvas.create_oval(location_x + 5,
                                     location_y + self.cir3_y,
                                     location_x + 5 + self.circle_size,
                                     location_y + self.cir3_y + self.circle_size,
                                     fill = 'green')

    def move(self, offset_x, offset_y):
        self.canvas.move(self.id_box, offset_x, offset_y)
        self.canvas.move(self.id_top, offset_x, offset_y)
        self.canvas.move(self.id_mid, offset_x, offset_y)
        self.canvas.move(self.id_bot, offset_x, offset_y)

    def set_red(self, on):
        if on:
            self.canvas.itemconfig(self.id_top, fill="firebrick1")
            self.canvas.itemconfig(self.id_mid, fill="gray84")
            self.canvas.itemconfig(self.id_bot, fill="gray84")
        else:
            self.canvas.itemconfig(self.id_top, fill="gray84")


    def set_yellow(self, on):
        if on:
            self.canvas.itemconfig(self.id_top, fill="gray84")
            self.canvas.itemconfig(self.id_mid, fill="yellow")
            self.canvas.itemconfig(self.id_bot, fill="gray84")
        else:
            self.canvas.itemconfig(self.id_mid, fill="gray84")


    def set_green(self, on):
        if on:
            self.canvas.itemconfig(self.id_top, fill="gray84")
            self.canvas.itemconfig(self.id_mid, fill="gray84")
            self.canvas.itemconfig(self.id_bot, fill="green")
        else:
            self.canvas.itemconfig(self.id_bot, fill="gray84")


if __name__ == '__main__':
    root = Tk()
    my_gui = TrafficGUI(root)
    root.mainloop()