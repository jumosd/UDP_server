import gi
import cv2
gi.require_version('Gst', '1.0')
from gi.repository import Gst

# GStreamer 초기화
Gst.init(None)

# 송신 파이프라인 설정 (예: 192.168.1.84 IP 주소로 전송)
pipeline = Gst.parse_launch(
    "avfvideosrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast "
    "! rtph264pay config-interval=1 pt=96 ! udpsink host=192.168.1.84 port=5600"
)

# 파이프라인 실행
pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        pass
except KeyboardInterrupt:
    print("종료 중...")
finally:
    pipeline.set_state(Gst.State.NULL)
