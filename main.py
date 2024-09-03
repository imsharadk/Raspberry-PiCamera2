from tkinter import *
import os
from picamera2 import Picamera2, Preview
from time import sleep
from datetime import datetime, date
from PIL import ImageTk, Image
from threading import Thread
import sys
from multiprocessing import Process

camera = Picamera2()
camera.preview_configuration.size = (3000, 2250)
#camera_config = camera.create_preview_configuration()
#camera.configure(camera_config)
camera.start_preview(True, x=1, y=1, width=800, height=600)
camera.start()

def cam_start():
    camera.start_preview(True, x=1, y=1, width=800, height=600)
    camera.start()

def cam_stop():
    camera.stop_preview()

def Recording_start():
    dir = str(datetime.now())
    parent_directory = "/home/pi5/Desktop/CamPic/"
    path = os.path.join(parent_directory, dir)
    os.mkdir(path)
    print("Camera recording start")
    camera.start_and_record_video(path + '/' + "vid" + '.h264')
    message.config(bg="green", text="Video Recording is started")

def Recording_stop():
    print("Camera recording stop")
    camera.stop_recording()
    message.config(bg="red", text="Video Recording is stopped")

def Capture():
    dir = str(datetime.now())
    parent_directory = "/home/pi5/Desktop/CamPic/Image/"
    camera.capture_file(parent_directory + "Image" + dir + '.jpg')
    print("Image Captured")
    message.config(bg="yellow", text=("Image Captured with name " + "Image"+dir+".jpg"))

def phase_view():
    from matplotlib import pyplot as plt
    phase_value = phase_map()
    
    figsize = plt.get_current_fig_manager()
    figsize.resize(*figsize.window.maxsize())

    plt.title("Phase Map View")
    plt.imshow(phase_value)
    plt.colorbar()
    plt.show()
    
def phase_map():
    camera.capture_file("image_phase.jpg")
    sleep(1)
    import numpy as np
    from numpy.fft import fftshift, ifftshift, fft2, ifft2
    import cv2 as cv
    from skimage.restoration import unwrap_phase
    
    mask = np.zeros((2000, 3000), dtype=complex)
    mask[960:1050,1850:1920]  = fftshift(fft2(cv.cvtColor(cv.imread('image_phase.jpg'),cv.COLOR_BGR2GRAY)))[960:1050,1850:1920]
    mask_central = np.zeros_like(mask)
    mask_central[985:1015,1475:1525]  = mask[968:998,1864:1914]
    return unwrap_phase(np.angle(ifft2(ifftshift(mask_central))))
    
def fourier_view():
    import matplotlib.pyplot as plt
    from matplotlib import animation
    import numpy as np
    import cv2 as cv

    figpos = plt.get_current_fig_manager()
    figpos.resize(*figpos.window.maxsize())

    camera.capture_file('image_fourier.jpg')
    sleep(0.1)
    img = cv.imread('image_fourier.jpg',0)
    dft = cv.dft(np.float32(img), flags = cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum = 20*np.log(cv.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
    plt.imshow(magnitude_spectrum, cmap='viridis')
    plt.colorbar()
    plt.title('Fourier View')
    plt.xticks([]) 
    plt.yticks([])
    plt.show()

def opencv_view():
    camera.capture_file('image_opencv.jpg')
    sleep(0.1)

    import cv2 as cv
    import matplotlib.pyplot as plt

    figpos = plt.get_current_fig_manager()
    figpos.resize(*figpos.window.maxsize())
    opencv_img = cv.imread('image_opencv.jpg')
    plt.title("OpenCV View")
    plt.imshow(opencv_img)
    plt.colorbar()
    plt.show()

def Setting():
    print("You are into camera setting")
    setting = Tk()
    setting.title("Camera Setting")
    setting.geometry('%dx%d+%d+%d'%(400, 400, 800, 10))
    scale_length = 300
    scale_width = 15

    exposure = Label(setting, 
                     bg='white', 
                     text='Exposure', 
                     height=2, 
                     width=10)
    exposure.grid(row=0, column=0)

    exposure_scale = Scale(setting,  
                           from_=-8.0, 
                           to=8.0, 
                           resolution=0.1,
                           orient=HORIZONTAL,
                           width=scale_width,
                           length=scale_length,
                           command=exposure_setting)
    exposure_scale.grid(row=0, column=1)

    gain = Label(setting, 
                 bg='white', 
                 text='Gain', 
                 height=2, 
                 width=10)
    gain.grid(row=1, column=0)
    gain_scale = Scale(setting,  
                       from_=1.0, 
                       to=251.0,
                       resolution=1.0, 
                       orient=HORIZONTAL,
                       width=scale_width,
                       length=scale_length,
                       command=gain_setting)
    gain_scale.grid(row=1, column=1)

    brightness = Label(setting, 
                 bg='white', 
                 text='Brightness', 
                 height=2, 
                 width=10)
    brightness.grid(row=2, column=0)
    brightness_scale = Scale(setting,  
                       from_=-1, 
                       to=1,
                       resolution=0.01,
                       orient=HORIZONTAL,
                       width=scale_width,
                       length=scale_length,
                       command=brightness_setting)
    brightness_scale.grid(row=2, column=1)

    sharpness = Label(setting, 
                     bg='white', 
                     text='Sharpness', 
                     height=2, 
                     width=10)
    sharpness.grid(row=3, column=0)

    sharpness_scale = Scale(setting,  
                           from_=0, 
                           to=16.0, 
                           resolution=0.1,
                           orient=HORIZONTAL,
                           width=scale_width,
                           length=scale_length,
                           command=sharpness_setting)
    sharpness_scale.grid(row=3, column=1)

    contrast = Label(setting, 
                 bg='white', 
                 text='Contrast', 
                 height=2, 
                 width=10)
    contrast.grid(row=4, column=0)
    contrast_scale = Scale(setting,  
                       from_=0, 
                       to=32,
                       resolution=0.1, 
                       orient=HORIZONTAL,
                       width=scale_width,
                       length=scale_length,
                       command=contrast_setting)
    contrast_scale.grid(row=4, column=1)

    saturation = Label(setting, 
                 bg='white', 
                 text='Saturation', 
                 height=2, 
                 width=10)
    saturation.grid(row=5, column=0)
    saturation_scale = Scale(setting,  
                       from_=0, 
                       to=32,
                       resolution=0.01,
                       orient=HORIZONTAL,
                       width=scale_width,
                       length=scale_length,
                       command=saturation_setting)
    saturation_scale.grid(row=5, column=1)

    colourgain = Label(setting, 
                 bg='white', 
                 text='ColourGains', 
                 height=2, 
                 width=10)
    colourgain.grid(row=6, column=0)
    colourgain_scale = Scale(setting,  
                       from_=0, 
                       to=32,
                       resolution=0.01,
                       orient=HORIZONTAL,
                       width=scale_width,
                       length=scale_length,
                       command=colourgain_setting)
    colourgain_scale.grid(row=6, column=1)

    flickerperiod = Label(setting, 
                 bg='white', 
                 text='Frame Rate', 
                 height=2, 
                 width=10)
    flickerperiod.grid(row=7, column=0)
    flickerperiod_scale = Scale(setting,  
                       from_=1, 
                       to=100,
                       resolution=1,
                       orient=HORIZONTAL,
                       width=scale_width,
                       length=scale_length,
                       command=flickerperiod_setting)
    flickerperiod_scale.grid(row=7, column=1)

def setting_list():
    print(camera.camera_controls)
    print(camera.camera_properties)

def exposure_setting(value):
    set_exposure_value = float(value)
    camera.set_controls({"ExposureValue": set_exposure_value})
    print("Camera exposure value set to " + str(set_exposure_value))

def gain_setting(value):
    set_gain_value = float(value)
    camera.set_controls({"AnalogueGain": set_gain_value})
    print("Camera Gain set to " + str(set_gain_value))

def brightness_setting(value):
    set_brightness_value = float(value)
    camera.set_controls({"Brightness": set_brightness_value})
    print("Camera brightness set to " + str(set_brightness_value))

def sharpness_setting(value):
    set_sharpness_value = float(value)
    camera.set_controls({"Sharpness": set_sharpness_value})
    print("Camera exposure value set to " + str(set_sharpness_value))

def contrast_setting(value):
    set_contrast_value = float(value)
    camera.set_controls({"Contrast": set_contrast_value})
    print("Camera exposure value set to " + str(set_contrast_value))

def saturation_setting(value):
    set_saturation_value = float(value)
    camera.set_controls({"Saturation": set_saturation_value})
    print("Camera exposure value set to " + str(set_saturation_value))

def colourgain_setting(value):
    set_colourgain_value = float(value)
    camera.set_controls({"ExposureValue": set_colourgain_value})
    print("Camera exposure value set to " + str(set_colourgain_value))

def flickerperiod_setting(value):
    set_flickerperiod_value = int((1000000/int(value)))
    camera.set_controls({"AeFlickerPeriod": set_flickerperiod_value})
    print("Camera framerate is set to " + value)

def reset_setting():
    camera.set_controls({"ExposureValue": 0.0})
    camera.set_controls({"AnalogueGain": 1.0})
    camera.set_controls({"Brightness": 0.0})
    camera.set_controls({"Sharpness": 1.0})
    camera.set_controls({"Contrast": 1.0})
    camera.set_controls({"Saturation": 1.0})
    camera.set_controls({"ExposureValue": 0.0})
    
    print("Camera setting reset")

root = Tk()
root.title("Pi Camera")
root.geometry('%dx%d+%d+%d'%(450, 567, 801, 1))
root.configure(bg='gray19')

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
helpmenu = Menu(menu)
settingmenu = Menu(menu)

menu.add_cascade(label="File", menu=filemenu)
filemenu.add_cascade(label="New")
filemenu.add_command(label="Setting",command=Setting)

menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_cascade(label="About")
helpmenu.add_cascade(label="Info")
helpmenu.add_command(label="Exit", command=root.quit)

camstart_button = Button(root, bg='white', text='Camera Start', height=2, width=25, command=cam_start)
camstart_button.grid(row=0, column=0)

camstop_button = Button(root, bg='white', text='Camera Close', height=2, width=25, command=cam_stop)
camstop_button.grid(row=0, column=1)

rec_start_button = Button(root, bg='white', text='Video Recording ON', height=2, width=25, command=Recording_start)
rec_start_button.grid(row=1, column=0)

rec_stop_button = Button(root, bg='white', text='Video Recording OFF', height=2, width=25, command=Recording_stop)
rec_stop_button.grid(row=1, column=1)

capture_button = Button(root, bg='white', text='Image Capture', height=2, width=25, command=Capture)
capture_button.grid(row=2, column=0)

setting_button = Button(root, bg='white', text='Setting', height=2, width=25, command=Setting)
setting_button.grid(row=2, column=1)

reset_setting_button = Button(root, bg='white', text='Reset Setting', height=2, width=25, command=reset_setting)
reset_setting_button.grid(row=3, column=0)

fourier_view__button = Button(root, bg='white', text='Fourier View', height=2, width=25, command=fourier_view)
fourier_view__button.grid(row=3, column=1)

phase_view_button = Button(root, bg='white', text='Phase View', height=2, width=25, command=phase_view)
phase_view_button.grid(row=4, column=0)

cv_view__button = Button(root, bg='white', text='OpenCV View', height=2, width=25, command=opencv_view)
cv_view__button.grid(row=4, column=1)

quit_button = Button(root, bg='white', text='Quit', height=2, width=25, command=root.quit)
quit_button.grid(row=9, column=0)

message = Label(root, bg='white', text='', height=1, width=58)
message.place(x=0, y= 543)

root.mainloop()
