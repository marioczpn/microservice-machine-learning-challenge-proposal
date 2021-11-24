import pytest

mp = pytest.MonkeyPatch()
mp.setenv('FACE_DETECTION_API_NAME', 'FACE_DETECTION_API_NAME')
mp.setenv('ML_MODEL_PATH', './models/haarcascade_frontalface_default.xml')
                