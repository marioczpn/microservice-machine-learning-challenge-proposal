import numpy as np
import cv2
import base64
import time
import os

class MockSDK:
    
    def __init__(self) -> None:
        # You will have to adjust the path to the model if this file is not in the same directory as the "models" directory
        model_path = os.environ['ML_MODEL_PATH']
        self.faceCascade = cv2.CascadeClassifier(model_path)

    
    def get_face_location(self, b64EncodedImg: bytes) -> list:
        """Receives a Base64 encoded bytes-like object (image file)
        and returns face locations

        You can get the correct format using this:

        `base64.b64encode(<bytes>)`

        If you need it to be `utf-8` for some messaging/caching system, then you can use:

        `base64.b64encode(<bytes>).decode('utf-8')`

        But do not forget to use `.encode('utf-8')` on the `str`
        (after retrieving the message) before passing it to this method.

        Parameters
        ----------
        b64EncodedImg : `bytes`
            Image file encoded as a Base64 encoded bytes-like object

        Returns
        -------
        `list`
            A list of lists where each list represents the
            location of a detected face within the image.

            Each list returned has 4 `int` values: `[<x>,<y>,<width>,<height>]`

            `x` and `y` are the coordinates for the
            top left corner of the face bounding box (ROI).
        """
        photo = base64.b64decode(b64EncodedImg)
        photo = cv2.equalizeHist(cv2.imdecode(np.fromstring(photo, np.uint8), cv2.IMREAD_GRAYSCALE))
        time.sleep(5) # Simulating a GPU-bound/CPU-bound intensive DL/ML inference task (don't remove)
        return self.faceCascade.detectMultiScale(photo, 1.1, 6, minSize=(96, 96)).tolist()