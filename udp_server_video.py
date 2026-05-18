import socket
import cv2

from package import RTPPackage
from Crypto.Cipher import AES

DEST_IP = "127.0.0.1"
DEST_PORT = 5004

MAX_PAYLOAD = 1400

# 32 bytes (AES-256)
SECRET_KEY = b'32323232323232323232323232323232'

# Socket UDP
sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

# DSCP AF41
TOS_VIDEO_VALUE = 0x88
sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, TOS_VIDEO_VALUE)

rtp = RTPPackage(payload_type=26)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir webcam")
    exit()

print("Streaming RTP iniciado...")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Compressão JPEG
    _, buffer = cv2.imencode('.jpg', frame)

    payload = buffer.tobytes()

    chunks = [
        payload[i:i + MAX_PAYLOAD]
        for i in range(0, len(payload), MAX_PAYLOAD)
    ]

    for i, chunk in enumerate(chunks):

        # Último pacote do frame?
        marker = 1 if i == len(chunks) - 1 else 0

        cipher = AES.new(SECRET_KEY, AES.MODE_CTR)
        nonce = cipher.nonce
        encrypted_chunk = cipher.encrypt(chunk)

        secure_payload = nonce + encrypted_chunk

        packet = rtp.build_rtp_packet(
            secure_payload,
            marker=marker
        )
    
        sock.sendto(
            packet,
            (DEST_IP, DEST_PORT)
        )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()