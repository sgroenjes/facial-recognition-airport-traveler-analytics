# For handling video capture

import cv2

# Replace 'WINDOWS_IP' and 'PORT' with your IP and port
url = "http://WINDOWS_IP:PORT/video"
cap = cv2.VideoCapture(url)

while(True):
  ret, frame = cap.read()
  if frame is not None:
    cv2.imshow('IP WebCam', frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
