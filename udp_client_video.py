import socket
import struct

import cv2
import numpy as np

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 5004

# UDP
sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.bind((LISTEN_IP, LISTEN_PORT))

print("Cliente RTP ouvindo...")

frame_buffer = b""

while True:

    packet, addr = sock.recvfrom(65535)

    header = packet[:12]

    payload = packet[12:]

    v_p_x_cc, m_pt, seq, timestamp, ssrc = struct.unpack(
        '!BBHII',
        header
    )

    # Marker bit
    marker = m_pt >> 7

    # Junta chunks
    frame_buffer += payload

    # Último pacote?
    if marker == 1:

        # Reconstrói JPEG
        np_data = np.frombuffer(
            frame_buffer,
            dtype=np.uint8
        )

        frame = cv2.imdecode(
            np_data,
            cv2.IMREAD_COLOR
        )

        if frame is not None:

            cv2.imshow(
                "Cliente RTP",
                frame
            )

        # Limpa buffer
        frame_buffer = b""

        # ESC fecha
        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()