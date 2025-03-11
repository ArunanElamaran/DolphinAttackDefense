import numpy as np  # importing inside the init function does not work for some reason
import pyrealsense2 as rs
import cv2
from PIL import Image

class LidarCamera:
    def __init__(self, environ_image, depth_image):
        self.np = np
        self.rs = rs
        self.Image = Image
        self.depth_image_path = environ_image
        self.color_image_path = depth_image

    def get_depth_matrix(self):
        # Create a context object. This object owns the handles to all connected realsense devices
        pipeline = self.rs.pipeline()
        pipeline.start()

        try:
            while True:
            # Create a pipeline object. This object configures the streaming camera and owns it's handle
                for i in range(3):
                	frames = pipeline.wait_for_frames()
                frames = pipeline.wait_for_frames()
                depth = frames.get_depth_frame()
                if not depth: 
                    continue
                depth_data = depth.as_frame().get_data()
                np_image = self.np.asanyarray(depth_data)
                np_image = cv2.applyColorMap(cv2.convertScaleAbs(np_image, alpha=0.03), cv2.COLORMAP_JET) #added color overlay
                return np_image
                break
        finally:
            pipeline.stop()

    def get_color_matrix(self):
        pipeline =self.rs.pipeline()
        pipeline.start()

        try:
            while True:
            # Create a pipeline object. This object configures the streaming camera and owns it's handle
                for i in range(3):
                	frames = pipeline.wait_for_frames()
                frames = pipeline.wait_for_frames()
                color = frames.get_color_frame()
                if not color:
                    continue
                color_data = color.as_frame().get_data()
                np_image = self.np.asanyarray(color_data)
                return np_image
                break
        finally:
            pipeline.stop()


    def get_depth_image(self):
        matrix = self.get_depth_matrix()
        if matrix is not None:
            image = self.Image.fromarray(matrix)
            image.save(self.depth_image_path)

    def get_color_image(self):
        matrix = self.get_color_matrix()
        if matrix is not None:
            image = self.Image.fromarray(matrix)
            image.save(self.color_image_path)


# Example Usage
def test():
    import os
    path = os.getcwd()
    camera = LidarCamera(path + "/../environmentImage.jpg", path + "/../depthImage.jpg")

    print("📷 Capturing color image...")
    camera.get_color_image()

    print("📏 Capturing depth image...")
    camera.get_depth_image()

if __name__ == "__main__":
    test()
