import socket
import struct

import cv2
import numpy as np

from Crypto.Cipher import AES

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 5004

SECRET_KEY = b'32323232323232323232323232323232'

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

    secure_payload = packet[12:]

    v_p_x_cc, m_pt, seq, timestamp, ssrc = struct.unpack(
        '!BBHII',
        header
    )

    # Marker bit
    marker = m_pt >> 7

    nonce = secure_payload[:8]
    encrypted_chunk = secure_payload[8:] 

    cipher = AES.new(SECRET_KEY, AES.MODE_CTR, nonce=nonce)
    decrypted_chunk = cipher.decrypt(encrypted_chunk)


    # Junta chunks
    frame_buffer += decrypted_chunk

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