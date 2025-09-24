from io import BytesIO
from typing import Tuple
import numpy as np
import cv2
from PIL import Image


# Load image from bytes into OpenCV BGR format
def load_image_bytes(data: bytes) -> np.ndarray:
arr = np.frombuffer(data, np.uint8)
img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
if img is None:
raise ValueError('Could not decode image')
return img


# Convert back to bytes (JPEG)
def image_to_bytes(img: np.ndarray, ext='.jpg', quality=90) -> bytes:
ok, buf = cv2.imencode(ext, img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
if not ok:
raise ValueError('Encoding failed')
return buf.tobytes()


# Filters
def to_grayscale(img: np.ndarray) -> np.ndarray:
return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def blur(img: np.ndarray, ksize: int = 5) -> np.ndarray:
k = max(1, (ksize // 2) * 2 + 1)
return cv2.GaussianBlur(img, (k, k), 0)


# Flip: 0 vertical, 1 horizontal, -1 both
def flip(img: np.ndarray, mode: int = 1) -> np.ndarray:
return cv2.flip(img, mode)


# Crop: (x,y,w,h)
def crop(img: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
h_img, w_img = img.shape[:2]
x0 = max(0, x)
y0 = max(0, y)
x1 = min(w_img, x + w)
y1 = min(h_img, y + h)
return img[y0:y1, x0:x1]


# Composite processing function


def process_image(data: bytes, ops: dict) -> Tuple[bytes, str]:
"""ops example:
{
"filter": "grayscale" | "blur",
"blur_ksize": 7,
"flip": 1,
"crop": [x,y,w,h]
}
Returns: (bytes, mime)
"""
img = load_image_bytes(data)


# Crop first (if provided)
if 'crop' in ops and isinstance(ops['crop'], (list, tuple)) and len(ops['crop']) == 4:
x, y, w, h = ops['crop']
img = crop(img, int(x), int(y), int(w), int(h))


# Flip
if 'flip' in ops:
try:
mode = int(ops['flip'])
img = flip(img, mode)
except Exception:
pass
return out_bytes, 'image/jpeg'