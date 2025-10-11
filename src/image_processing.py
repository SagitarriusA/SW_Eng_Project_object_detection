import cv2
import os
import numpy as np


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
            self.cap = cv2.VideoCapture(self.cam_device, cv2.CAP_DSHOW)

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

    def process_frame(self, image):
        if image is None:
            print("Error, no image found to process")
            return image, []

        # --- Preprocessing ---
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 220, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        MIN_AREA = 5000
        MAX_AREA = 500000
        detections = []

        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area < MIN_AREA or area > MAX_AREA:
                continue

            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            cv2.drawContours(image, [contour], -1, (0, 0, 0), 2)
            x, y, w, h = cv2.boundingRect(approx)
            x_mid, y_mid = x + w // 2, y + h // 2

            shape_name = {
                3: "Triangle",
                4: "Quadrilateral",
                5: "Pentagon",
                6: "Hexagon"
            }.get(len(approx), "Circle")

            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.drawContours(mask, [contour], -1, 255, -1)
            mean_color = cv2.mean(image, mask=mask)
            color_name = self.closest_color_name((mean_color[0], mean_color[1], mean_color[2]))

            cv2.putText(image, f"{color_name}, {shape_name}",
                        (x_mid - 40, y_mid), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            detections.append((shape_name, color_name))

        return image, detections


    def closest_color_name(self, bgr):
        """
        Detects the closest color using HSV thresholds.
        Returns a basic color name.
        """
        # Convert the RGB (actually OpenCV uses BGR) to HSV
        b, g, r = bgr
        color_bgr = np.uint8([[[b, g, r]]])
        hsv = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV)[0][0]
        h, s, v = hsv

        # Define HSV ranges for basic colors
        # Hue values in OpenCV range from 0 to 179
        color_ranges = {
            "red":       [(0, 70, 50), (10, 255, 255)],
            "red2":      [(170, 70, 50), (180, 255, 255)],
            "orange":    [(11, 70, 50), (20, 255, 255)],
            "yellow":    [(21, 70, 50), (35, 255, 255)],
            "green":     [(36, 70, 50), (85, 255, 255)],
            "cyan":      [(86, 70, 50), (100, 255, 255)],
            "blue":      [(101, 70, 50), (130, 255, 255)],
            "purple":    [(131, 70, 50), (180, 255, 255)],
            "white":     [(0, 0, 200), (180, 40, 255)],
            "gray":      [(0, 0, 40), (180, 40, 200)],
            "black":     [(0, 0, 0), (180, 255, 40)]
        }

        for name, (lower, upper) in color_ranges.items():
            lower_np = np.array(lower, dtype=np.uint8)
            upper_np = np.array(upper, dtype=np.uint8)
            if (lower_np[0] <= h <= upper_np[0] and
                lower_np[1] <= s <= upper_np[1] and
                lower_np[2] <= v <= upper_np[2]):
                # Merge "red" and "red2"
                if name == "red2":
                    name = "red"
                return name

        return "unknown"

    def release(self):
        """Release camera resource if open."""
        if self.cap:
            self.cap.release()
            print("Camera released.")


if __name__ == "__main__":
    processor = ImageProcessor(cam_device=0)

    """script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "../images", "test_image_00.png")
    processor = ImageProcessor(image_path=image_path)"""

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
