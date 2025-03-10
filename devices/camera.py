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

    def get_color_matrix(self):
        pipeline = self.rs.pipeline()
        config = self.rs.config()
        context = self.rs.context()
        devices = context.query_devices()
        print(f"identifying {len(devices)} devices")

        # ✅ Reduce resolution to 424x240 and FPS to 6 (USB 2.1 compatibility)
        config.enable_stream(self.rs.stream.color, 424, 240, self.rs.format.bgr8, 6)

        pipeline.start(config)
        print("✅ Color stream started (USB 2.1 mode)")

        try:
            frames = pipeline.wait_for_frames(timeout_ms=10000)

            # for _ in range(5):  # Skip initial frames for better quality
            #     frames = pipeline.wait_for_frames(timeout_ms=10000)

            # frames = pipeline.wait_for_frames(timeout_ms=10000)
            color = frames.get_color_frame()

            if not color:
                print("❌ No color frame received!")
                return None

            print("✅ Color frame received!")
            color_data = color.as_frame().get_data()
            np_image = self.np.asanyarray(color_data)
            return np_image

        except Exception as e:
            print(f"exception: {e}")
            devices[0].hardware_reset()
            print("reset device")


        finally:
            pipeline.stop()

    def get_depth_matrix(self):
        pipeline = self.rs.pipeline()
        config = self.rs.config()

        # ✅ Reduce depth resolution to 424x240 and FPS to 6 (USB 2.1 compatibility)
        config.enable_stream(self.rs.stream.depth, 424, 240, self.rs.format.z16, 6)

        pipeline.start(config)
        print("✅ Depth stream started (USB 2.1 mode)")

        try:
            for _ in range(5):  # Skip initial frames
                frames = pipeline.wait_for_frames(timeout_ms=10000)

            frames = pipeline.wait_for_frames(timeout_ms=10000)
            depth = frames.get_depth_frame()

            if not depth:
                print("❌ No depth frame received!")
                return None

            print("✅ Depth frame received!")
            depth_data = depth.as_frame().get_data()
            np_image = self.np.asanyarray(depth_data)

            # ✅ Apply color mapping for better visualization
            np_image = cv2.applyColorMap(cv2.convertScaleAbs(np_image, alpha=0.03), cv2.COLORMAP_JET)
            return np_image

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

    # print("📏 Capturing depth image...")
    # camera.get_depth_image()

if __name__ == "__main__":
    test()
