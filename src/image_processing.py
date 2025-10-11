import cv2
import os


class ImageProcessor:
    def __init__(self, cam_device=None, image_path=None):
        self.cam_device = cam_device
        self.image_path = image_path
        self.cap = None
        self.image = None
        self.is_camera = False

        self._init_source()

    def _init_source(self):
        """Initialize either a camera or image input."""
        if self.cam_device is not None:
            print(f"Initializing camera device {self.cam_device}")
            self.cap = cv2.VideoCapture(self.cam_device)

            if not self.cap.isOpened():
                raise RuntimeError(f"Could not open camera device {self.cam_device}")

            self.is_camera = True
            print("Camera initialized successfully.")

        elif self.image_path is not None:
            print(f"Loading image from {self.image_path}")

            if not os.path.exists(self.image_path):
                raise FileNotFoundError(f"Image not found: {self.image_path}")

            self.image = cv2.imread(self.image_path)
            if self.image is None:
                raise ValueError(f"Failed to read image: {self.image_path}")

            self.is_camera = False
            print("Image loaded successfully.")

        else:
            raise ValueError("No input source provided (camera or image).")

    def get_frame(self):
        """Get a single frame from camera or the loaded image."""
        if self.is_camera:
            ret, frame = self.cap.read()
            if not ret:
                raise RuntimeError("Failed to capture frame from camera.")
            return frame
        else:
            return self.image

    def process_frame(self, frame):
        # Convert to grayscale as a simple example
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Draw a text overlay just to visualize processing
        processed = cv2.putText(gray.copy(), "Processed Frame", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return processed

    def release(self):
        """Release camera resource if open."""
        if self.cap:
            self.cap.release()
            print("Camera released.")


if __name__ == "__main__":
    # processor = ImageProcessor(cam_device=0)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "../images", "test_image_00.png")
    processor = ImageProcessor(image_path=image_path)

    if processor.is_camera:
        print("Running real-time camera processing (press 'q' to quit)")
        while True:
            frame = processor.get_frame()
            processed = processor.process_frame(frame)

            cv2.imshow("Processed Frame", processed)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        processor.release()
        cv2.destroyAllWindows()

    else:
        print("Processing static image (press any key to close)")
        frame = processor.get_frame()
        processed = processor.process_frame(frame)

        cv2.imshow("Processed Image", processed)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
