import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from rclpy.service import Service

class TurtuleBot3(Node):
    def __init__(self) -> None:
        # Create the note with name "turtlebot_teleop_2/"
        super().__init__("webcam_publisher")
        
        # Create the topic publisher on the topic "/video_transfer/"
        self.publisher = self.create_publisher(
            msg_type=CompressedImage,   # Defines the topic mensage type
            qos_profile=40,             
            topic="/video_frames"
        )

        # Create the publisher call timer
        self.timer = self.create_timer(
            0.001,  # With 10Hz of refreshe
            self.timer_callback
        )

        self.cap = cv2.VideoCapture(0)

    def timer_callback(self):
        # Capture the video frame
        ret, frame = self.cap.read()
        if ret:
            # Saves the image on a temporarily saves the image on a buffer
            _, buffer = cv2.imencode('.jpeg', frame)

            # Defines the messge type to be published, as bytes
            image_message = CompressedImage()
            image_message.format = "jpeg"
            image_message.data= buffer.tobytes()
            
            # Publish the image on the topic
            self.publisher.publish(image_message)


def main(args=None):
    
    rclpy.init(args=args)
    video_publisher = TurtuleBot3()
    rclpy.spin(video_publisher)
    video_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()