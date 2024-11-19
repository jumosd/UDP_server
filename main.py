import gi
import cv2
import socket
import numpy as np
import time
# GStreamer 초기화
gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init(None)

# 송신할 서버 IP와 포트 설정
SERVER_IP = "192.168.1.84"  # 수신할 QGC가 있는 컴퓨터의 IP 주소
SERVER_PORT = 5600          # QGC가 비디오를 수신할 포트

# GStreamer 송신 파이프라인 설정
pipeline = Gst.parse_launch(
    f"avfvideosrc device-index=1 ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast "
    f"! rtph264pay config-interval=1 pt=96 ! udpsink host={SERVER_IP} port={SERVER_PORT}"
)

# 파이프라인 실행
pipeline.set_state(Gst.State.PLAYING)

try:
    print("QGC로 비디오 스트리밍을 시작합니다. 종료하려면 Ctrl+C를 누르세요.")
    while True:
        success, position = pipeline.query_position(Gst.Format.TIME)
        if success:
            print(f"현재 위치: {position / Gst.SECOND} 초")
            time.sleep(1)  # 1초 간격으로 확인
        pass  # 파이프라인이 계속 실행되도록 유지
    
except KeyboardInterrupt:
    print("종료 중...")

finally:
    # 파이프라인 정지 및 종료
    pipeline.set_state(Gst.State.NULL)
    print("스트리밍이 종료되었습니다.")
