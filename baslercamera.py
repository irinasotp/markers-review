from pypylon import pylon
import cv2
import time


class BaslerVideoCapture:
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    converter = pylon.ImageFormatConverter()

    # The parameter MaxNumBuffer can be used to control the count of buffers
    # allocated for grabbing. The default value of this parameter is 10.
    #camera.MaxNumBuffer = 1

    camera.ExposureAuto.SetValue('Off')
    camera.ExposureTime.SetValue(3000)
    camera.GainAuto.SetValue('Off')
    camera.Gain.SetValue(0)

    # converting to opencv bgr format
    # converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputPixelFormat = pylon.PixelType_Mono8
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    
    def set_gain_exp_time(self,exp_time, gain):
        self.camera.ExposureAuto.SetValue('Off')
        self.camera.ExposureTime.SetValue(exp_time)
        self.camera.GainAuto.SetValue('Off')
        self.camera.Gain.SetValue(gain)

    def read(self):
        while True:
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                image = self.converter.Convert(grabResult)
                img = image.GetArray()
                #img = cv2.GaussianBlur(img, (3,3), 0)
                grabResult.Release()
                return img
