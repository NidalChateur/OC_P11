import os

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from sqlalchemy.orm import validates

# from config import BASE_DIR, UPLOAD_FOLDER
from config import Development

# used to create a database
db = SQLAlchemy()

# used to hash the password
bcrypt = Bcrypt()


class CrudMixin(object):
    IMAGE_WIDTH = 200
    ALLOWED_IMAGE_EXTENSION = ["jpg", "png", "jpeg", "gif", "bmp", "ico", "tiff"]

    def _check_image_file(self, image_file) -> bool:
        try:
            image = Image.open(image_file)
            image.verify()

            return True

        except Exception as e:
            raise ValueError(f"Type de fichier non autorisé ! {e}")

    def _resize_image(self, image_file) -> Image:
        """HEIGHT is determinate in function of WIDTH=200 to keep
        the original ratio"""

        if self._check_image_file(image_file):
            image = Image.open(image_file)

            # get the original height/width aspect ratio
            width, height = image.size

            # get the new height/width aspect ratio
            new_width = self.IMAGE_WIDTH
            new_height = int(height * (new_width / width))

            # resize the image
            image = image.resize((new_width, new_height), Image.LANCZOS)

            return image

    def resize_and_save_image(self, file):
        file_extension = file.filename.rsplit(".", 1)[-1].lower()
        filename = f"{self.IMAGE_PATH}{self.id}.{file_extension}"

        image = self._resize_image(file)
        if image:
            image.save(Development.BASE_DIR / Development.UPLOAD_FOLDER / filename)
            self.image = filename
            self.save()

    @validates("image")
    def validate_image(self, key, value):
        """check the image extension"""

        if value:
            if not isinstance(value, str):
                raise ValueError("L'attribut image doit être de type str !")

            image_extension = value.rsplit(".", 1)[-1].lower()
            if image_extension not in self.ALLOWED_IMAGE_EXTENSION:
                raise ValueError("Type de fichier non autorisé !")

            if value != f"{self.IMAGE_PATH}{self.id}.{image_extension}":
                raise ValueError("Nom de fichier non autorisé !")

        return value

    def delete_image(self):
        if hasattr(self, "image"):
            if self.image:
                user_image = (
                    Development.BASE_DIR / Development.UPLOAD_FOLDER / self.image
                )
                if os.path.exists(user_image):
                    os.remove(user_image)
                self.image = None
                self.save()

    def create(self):
        """save the instance in db"""

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def save():
        "(update) update the instance attributes in db"

        db.session.commit()

    def delete(self):
        """delete the instance from db"""

        self.delete_image()
        db.session.delete(self)
        db.session.commit()
