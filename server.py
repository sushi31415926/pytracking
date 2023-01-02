import pickle
import socket
import struct
import select

import cv2

HOST = '172.17.0.1'
PORT = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')
conn, addr = s.accept()

data = b'' ### CHANGED
payload_size = struct.calcsize("L") ### CHANGED

first = True
while True:
    display_name = "frame"
    # Retrieve message size
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED

    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Extract frame
    frame = pickle.loads(frame_data)
    # Display
    cv2.imshow(display_name, frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('r') or first:
        if not first:
            conn.send(b"start")
            while True:
                ready_to_read, _, _ = select.select([conn], [], [], 1)
                if ready_to_read:
                    while len(data) < payload_size:
                        data += conn.recv(4096)

                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED

                    # Retrieve all data based on message size
                    while len(data) < msg_size:
                        data += conn.recv(4096)
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame = pickle.loads(frame_data)

                else:
                    break


       
        cv2.putText(frame, 'Select target ROI and press ENTER', (20, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                   (0, 0, 0), 1)

        cv2.imshow(display_name, frame)
        x, y, w, h = cv2.selectROI(display_name, frame, fromCenter=False)
        bounding_box = f"{x},{y},{w},{h}"
        conn.send(str.encode(bounding_box))
    first = False
