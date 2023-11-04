import cv2
import time
from kafka import KafkaProducer
import json
import logging
import os
from datetime import datetime

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables for Kafka
KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'video_frames')

# Kafka Producer
producer = KafkaProducer(
  bootstrap_servers=[KAFKA_BROKER_URL],
  value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Replace 'WINDOWS_IP' and 'PORT' with your IP and port
url = "http://test:test@192.168.254.80:8080/video"

def publish_frame(frame, producer, topic):
  """Publishes a single frame to Kafka topic"""
  try:
    # Convert the frame to jpg format for better performance
    ret, buffer = cv2.imencode('.jpg', frame)
    producer.send(topic, buffer.tobytes())
    # Sleeping for a short duration to simulate real-time capture and transmission
    time.sleep(0.02)
  except Exception as e:
    logger.error(f"Failed to publish frame: {e}")

def connect_to_camera(url):
  """Attempts to connect to the camera and retries if it fails"""
  while True:
    cap = cv2.VideoCapture(url)
    if cap.isOpened():
      logger.info("Camera connection established")
      return cap
    else:
      logger.error("Failed to connect to camera, retrying in 5 seconds...")
      time.sleep(5)

def capture_video(producer, topic, url):
  """Captures video from the camera and publishes frames to Kafka"""
  cap = connect_to_camera(url)
  while True:
    ret, frame = cap.read()
    if frame is not None:
      publish_frame(frame, producer, topic)
    else:
      # Handle a disconnection
      logger.error("Frame capture failed, attempting to reconnect")
      cap.release()
      cap = connect_to_camera(url)

if __name__ == "__main__":
  try:
    capture_video(producer, KAFKA_TOPIC, url)
  except KeyboardInterrupt:
    logger.info("Video capture stopped")
  finally:
    producer.close()
