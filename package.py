import struct
import random

class RTPPackage:
    def __init__(self, payload_type=26):
        # O Packetizer só gerencia o Estado do RTP
        self.seq_num = random.randint(1, 10000)
        self.timestamp = random.randint(1, 10000)
        self.ssrc = random.randint(100000, 999999)
        self.payload_type = payload_type 

    def build_rtp_packet(self, payload, marker=1, timestamp_increment=3000):
        """
        Recebe o payload (vídeo), constrói o cabeçalho e avança os contadores.
        """
        version_byte = 0x80
        marker_pt_byte = (marker << 7) | self.payload_type
        
        # Empacota o cabeçalho
        header = struct.pack('!BBHII', 
                             version_byte, 
                             marker_pt_byte, 
                             self.seq_num, 
                             self.timestamp, 
                             self.ssrc)
        
        # O pacote final é o Cabeçalho + Payload
        packet = header + payload
        
        # ATUALIZA O ESTADO para a próxima vez que a função for chamada
        self.seq_num = (self.seq_num + 1) & 0xFFFF
        self.timestamp = (self.timestamp + timestamp_increment) & 0xFFFFFFFF 
        
        return packet