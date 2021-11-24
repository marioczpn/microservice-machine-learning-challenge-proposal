import base64
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile
from loguru import logger


class ImageUtil:
    """[ImageUtil]
        The utility class which contains static method can be reused across the application.
    """
    def __init__(self) -> None:
        pass
    
    def __save_upload_file_tmp(self, upload_file: UploadFile) -> Path:
        try:
            suffix = Path(upload_file.filename).suffix
            with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(upload_file.file, tmp)
                tmp_path = Path(tmp.name)
        finally:
            upload_file.file.close()
        return tmp_path
        
    def __convert_image_b64(self, upload_file: UploadFile):
        """[__convert_image_b64]
        It's a private method used by the class to conver the image to base64.
        
        Args:
            upload_file (UploadFile): [Image file]

        Returns:
            [imageToB64]: [returns the image encoded to base64.]
        """
        tmp_path = self.__save_upload_file_tmp(upload_file)
        image = open(tmp_path, 'rb')
        image_read = image.read()
        image_64_encode = base64.b64encode(image_read).decode('utf-8')
        return image_64_encode

    def prepare_img_msg(self, file: UploadFile):
        """[prepare_img_msg]
        It's a static method that prepare the image to base64
        
        Args:
            file (UploadFile): [Image file]

        Returns:
            [imageB64]: [the image in base64 encode]
        """
        logger.info(" [-] Encoding image as Base64..")
        img_msg = []
        image_64_encode = self.__convert_image_b64(file);          
        img_msg.append(image_64_encode)
        
        logger.info(" [X] Finished enconding.")
        return img_msg
