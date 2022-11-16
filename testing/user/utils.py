import base64
from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np
import requests

url = 'http://localhost:8080/user'
