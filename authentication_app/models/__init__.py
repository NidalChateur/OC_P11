import os

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from sqlalchemy.orm import validates

from config import BASE_DIR, UPLOAD_FOLDER

# used to create a database
db = SQLAlchemy()

# used to hash the password
bcrypt = Bcrypt()


class CrudMixin(object):
    MONTHS = [
        "janvier",
        "février",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "août",
        "septembre",
        "octobre",
        "novembre",
        "décembre",
    ]
    IMAGE_WIDTH = 200
    SPECIAL_CHARACTERS = '!@#$%^&*(),.;?":{}|<>_=/+-*µ£€§¤çàùéè°'
    ALLOWED_IMAGE_EXTENSION = ["jpg", "png", "jpeg", "gif", "bmp", "ico", "tiff"]

    def _resize_image(self, image) -> Image:
        """HEIGHT is determinate in function of WIDTH=200 to keep
        the original ratio"""

        image = Image.open(image)

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
        image.save(BASE_DIR / UPLOAD_FOLDER / filename)

        self.image = filename
        self.save()

    @validates("image")
    def validate_image(self, key, value):
        """check the image extension"""

        if value:
            image_extension = value.rsplit(".", 1)[-1].lower()
            if image_extension not in self.ALLOWED_IMAGE_EXTENSION:
                raise TypeError("Type de fichier non autorisé !")

            if value != f"{self.IMAGE_PATH}{self.id}.{image_extension}":
                raise TypeError("Nom de fichier non autorisé !")

        return value

    def delete_image(self):
        if self.image:
            user_image = BASE_DIR / UPLOAD_FOLDER / self.image
            if os.path.exists(user_image):
                os.remove(user_image)
            self.image = None
            self.save()

    def create(self):
        """save the user instance in db"""

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def save():
        "(update) save the user instance changes in db"

        db.session.commit()

    def delete(self):
        """delete the user instance from db"""

        self.delete_image()
        db.session.delete(self)
        db.session.commit()
