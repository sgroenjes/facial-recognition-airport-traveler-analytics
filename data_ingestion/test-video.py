import cv2
import logging
import time

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Camera URL
url = "http://test:test@192.168.254.80:8080/video"

def test_camera_connection(url, num_frames=10):
  """Test the camera connection by capturing and displaying a few frames"""
  cap = cv2.VideoCapture(url)

  if not cap.isOpened():
    logger.error("Failed to connect to camera.")
    return

  try:
    for _ in range(num_frames):
      ret, frame = cap.read()
      if not ret:
        logger.error("Failed to capture frame.")
        break

      # Display the frame
      cv2.imshow('Camera Frame', frame)

      # Wait for 1ms and exit the loop if 'q' is pressed
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

      # Let's also print the frame to see if it's captured correctly
      # We'll print the shape of the frame array
      print(f"Frame dimensions: {frame.shape}")
      time.sleep(0.5)  # Wait for half a second between frames

  finally:
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
  test_camera_connection(url)
