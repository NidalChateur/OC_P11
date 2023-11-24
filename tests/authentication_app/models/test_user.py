import os
import re
from datetime import date, datetime

import pytest
from PIL import Image
from werkzeug.datastructures import FileStorage

from authentication_app.models.user import User, db
from config import Config


class TestUser:
    VALID_PASSWORD = "00000000pW-"
    INVALID_PASSWORD = "11111111pW-"

    def _drop_and_create_db(self):
        db.drop_all()
        db.create_all()

    def _create_user_instance(self, app) -> User:
        user_test = User(
            role="secretary",
            first_name="first_name",
            last_name="last_name",
            birthdate=date(year=2000, month=1, day=1),
            email="test@test.com",
        )

        return user_test

    def test_str_rpr(self, app):
        self._drop_and_create_db()

        user = self._create_user_instance(app)
        user.id = 1

        user_id = f"id : {user.id}"
        user_role = f"role : {user.role}"
        user_full_name = f"first_name : {user.first_name}, last_name : {user.last_name}"
        user_birthdate = f"birthdate : {user.birthdate_formatter}"
        user_email = f"email : {user.email}"

        # case 1 : user without image
        assert (
            str(user)
            == f"{user_id}, {user_role}, {user_full_name}, {user_birthdate}, {user_email}"
        )

        assert str(user) == repr(user)

        # case 2 : user with image
        user.image = f"{User.IMAGE_PATH}{user.id}.jpg"
        user_image = f"image : {user.image}"

        assert (
            str(user)
            == f"{user_id}, {user_role}, {user_full_name}, {user_birthdate}, {user_email}, {user_image}"
        )

        assert str(user) == repr(user)

    def test_is_admin_property(self, app):
        user = self._create_user_instance(app)

        assert user.is_admin == (user.role == "admin")

    def test_birthdate_formatter_property(self, app):
        user = self._create_user_instance(app)

        assert user.birthdate_formatter == user.birthdate.strftime("%d/%m/%Y")

    def test_age(self, app):
        user = self._create_user_instance(app)

        today = date.today()
        user_age = (
            today.year
            - user.birthdate.year
            - ((today.month, today.day) < (user.birthdate.month, user.birthdate.day))
        )

        assert User.age(birthdate=user.birthdate) == user_age

    def test_create(self, app):
        user = self._create_user_instance(app)
        user.create()

        user_saved_in_db = User.query.filter_by(
            role="secretary",
            first_name="first_name",
            last_name="last_name",
            birthdate=date(year=2000, month=1, day=1),
            email="test@test.com",
        ).first()

        assert user.role == user_saved_in_db.role
        assert user.first_name == user_saved_in_db.first_name
        assert user.last_name == user_saved_in_db.last_name
        assert user.birthdate == user_saved_in_db.birthdate
        assert user.email == user_saved_in_db.email
        assert user_saved_in_db.id is not None
        assert isinstance(user_saved_in_db.id, int)

    def test_save(self, app):
        """Test plan :
        1. getting a user saved in db
        2. checking if the user attributes saved in the db are different from the new_user_attributes
        3. updating the user attributes saved in db with new_user_attributes
        4. checking the update"""

        # 1. getting a user saved in db
        user_saved_in_db = db.session.get(User, 1)

        new_user_attributes = {
            "role": "admin",
            "first_name": "first_name_2",
            "last_name": "last_name_2",
            "birthdate": date(year=2002, month=2, day=2),
            "email": "test2@test2.com",
        }

        # 2. checking if the user attributes saved in the db are different from the new_user_attributes
        assert user_saved_in_db.role != new_user_attributes["role"]
        assert user_saved_in_db.first_name != new_user_attributes["first_name"]
        assert user_saved_in_db.last_name != new_user_attributes["last_name"]
        assert user_saved_in_db.birthdate != new_user_attributes["birthdate"]
        assert user_saved_in_db.email != new_user_attributes["email"]

        # 3. updating the user attributes saved in db with new_user_attributes
        user_saved_in_db.role = new_user_attributes["role"]
        user_saved_in_db.first_name = new_user_attributes["first_name"]
        user_saved_in_db.last_name = new_user_attributes["last_name"]
        user_saved_in_db.birthdate = new_user_attributes["birthdate"]
        user_saved_in_db.email = new_user_attributes["email"]
        user_saved_in_db.save()

        # 4. checking the update
        updated_user_in_db = db.session.get(User, 1)

        assert updated_user_in_db.role == new_user_attributes["role"]
        assert updated_user_in_db.first_name == new_user_attributes["first_name"]
        assert updated_user_in_db.last_name == new_user_attributes["last_name"]
        assert updated_user_in_db.birthdate == new_user_attributes["birthdate"]
        assert updated_user_in_db.email == new_user_attributes["email"]

    def test_delete(self, app):
        user_saved_in_db = db.session.get(User, 1)

        assert user_saved_in_db is not None

        user_saved_in_db.delete()

        assert db.session.get(User, 1) is None

    def test_resize_and_save_image(self, app):
        """Test plan :
        1. checking that user in db has no image
        2. creating a FilStorage() object similar to form.image.data obtained from a FlaskForm
        3. calling User.resize_and_save_image() on the FileStorage() object created before
        4. checking that the user has now an image
        5. checking the user.image value after calling User.resize_and_save_image()
        6. checking the saved image width
        """

        # 1. checking that the user created in db has no image
        user = self._create_user_instance(app)
        user.create()

        assert user.image is None

        # 2. creating a FilStorage() object similar to form.image.data obtained from a FlaskForm
        image_path = "tests/authentication_app/models/naruto.jpg"
        with open(image_path, "rb") as image_file:
            image_data = FileStorage(
                stream=image_file, filename="naruto.jpg", content_type="image/jpeg"
            )

            # 3. calling User.resize_and_save_image() on the FileStorage() object created before
            user.resize_and_save_image(image_data)

        # 4. checking that the user has now an image
        assert user.image is not None

        # 5. checking the user.image value after calling User.resize_and_save_image()
        file_extension = image_data.filename.rsplit(".", 1)[-1].lower()

        assert user.image == f"{User.IMAGE_PATH}{user.id}.{file_extension}"

        # 6. checking the saved image width
        image = Image.open(f"{Config.UPLOAD_FOLDER}/{user.image}")
        width, height = image.size

        assert width == 200

    def test_resize_and_save_image_with_wrong_file(self, app):
        """Test plan :
        1. retrieving a user saved in the database
        2. defining the awaited error message
        3. defining a file path that points to a wrong file : "__init__.py"
        4. creating a FilStorage() object similar to form.image.data obtained from a FlaskForm
        5. calling User.resize_and_save_image() on the FileStorage() object created before
        6. awaiting a ValueError with a specific error message
        """
        # 1. retrieving a user saved in the database
        user_saved_in_db = db.session.get(User, 1)

        # 2. defining the awaited error message
        # re.escape() allows the use of special characters in the error message
        error_message = re.escape(
            "Type de fichier non autorisé ! cannot identify image file <FileStorage: 'naruto.jpg' ('image/jpeg')>"
        )

        # 3. defining a file path that points to a wrong file : "__init__.py"
        image_path = "tests/authentication_app/models/__init__.py"

        # 4. creating a FilStorage() object similar to form.image.data obtained from a FlaskForm
        with open(image_path, "rb") as image_file:
            image_data = FileStorage(
                stream=image_file, filename="naruto.jpg", content_type="image/jpeg"
            )

            # 5. calling User.resize_and_save_image() on the FileStorage() object created before
            # 6. awaiting a ValueError with a specific error message
            with pytest.raises(ValueError, match=error_message):
                user_saved_in_db.resize_and_save_image(image_data)

    def test_delete_image(self, app):
        """Test plan :
        1. retrieving a user saved in the database
        2. checking that the user has an image
        3. checking that the user has no image after calling .delete_image()
        4. checking that the user image file has been deleted
        """

        # 1. retrieving a user saved in the database
        user = db.session.get(User, 1)

        # 2. checking that the user has an image
        assert user.image is not None
        assert os.path.exists(f"./{Config.UPLOAD_FOLDER}/{user.image}")

        # 3. checking that the user has no image after calling .delete_image()
        user.delete_image()

        assert user.image is None

        # 4. checking that the user image file has been deleted
        # for each allowed extension
        for extension in User.ALLOWED_IMAGE_EXTENSION:
            image_path = (
                f"./{Config.UPLOAD_FOLDER}/{User.IMAGE_PATH}{user.id}.{extension}"
            )
            assert not os.path.exists(image_path)

    @pytest.mark.parametrize(
        "image_filename, error_message",
        [
            (111, "L'attribut image doit être de type str !"),
            ("image.py", "Type de fichier non autorisé !"),
            ("image.jpg", "Nom de fichier non autorisé !"),
            (f"{User.IMAGE_PATH}image.jpg", "Nom de fichier non autorisé !"),
        ],
    )
    def test_validate_image(self, app, image_filename, error_message):
        """Test plan :
        1. checking that the user retrieved from db has no image
        2. updating user.image with a wrong value
        3. awaiting a ValueError with a specific error message
        4. check that user.image is still None
        """
        # 1. checking that the user retrieved from db has no image
        user = db.session.get(User, 1)

        assert user.image is None

        # 2. updating user.image with a wrong value
        # 3. awaiting a ValueError with a specific error message
        with pytest.raises(ValueError, match=error_message):
            user.image = image_filename

        # 4. check that user.image is still None
        assert user.image is None

    @pytest.mark.parametrize(
        "birthdate, error_message",
        [
            ("01/01/2023", "L'attribut birthdate doit être de type date !"),
            (
                date(year=2023, month=1, day=1),
                "L'utilisateur doit avoir 18 ans ou plus !",
            ),
        ],
    )
    def test_validate_birthdate(self, app, birthdate, error_message):
        with pytest.raises(ValueError, match=error_message):
            User(
                role="secretary",
                first_name="first_name",
                last_name="last_name",
                birthdate=birthdate,
                email="test@test.com",
            )

    @pytest.mark.parametrize(
        "email, error_message",
        [
            (123456789, "L'attribut email doit être de type str !"),
            ("email", "Adresse e-mail invalide !"),
            ("email@", "Adresse e-mail invalide !"),
            ("@email.com", "Adresse e-mail invalide !"),
            ("email@email.", "Adresse e-mail invalide !"),
            ("email@email.", "Adresse e-mail invalide !"),
            ("test@test.com", "Cet e-mail est déjà utilisé par un utilisateur !"),
        ],
    )
    def test_validate_email(self, app, email, error_message):
        # 1. attempting to create user with an invalid email format
        with pytest.raises(ValueError, match=error_message):
            User(
                role="secretary",
                first_name="first_name",
                last_name="last_name",
                birthdate=date(year=2001, month=1, day=1),
                email=email,
            )

        # 2. attempting to update an existing user with a non-unique email.
        if email == "test@test.com":
            user = User.query.filter_by(email=email).first()

            # 2.1 checking that there is an existing user with the email 'test@test.com'
            assert user is not None

            # 2.2 creating a new user with valid and unique data
            user_2 = User(
                role="secretary",
                first_name="first_name_2",
                last_name="last_name_2",
                birthdate=date(year=2002, month=2, day=2),
                email="test2@test2.com",
            )
            user_2.create()

            # 2.3 attempting to update an existing user with a non-unique email.
            with pytest.raises(ValueError, match=error_message):
                user_2.email = "test@test.com"

    def test_set_password(self, app):
        user = db.session.get(User, 1)

        assert user.password is None

        user.set_password(self.VALID_PASSWORD)

        assert user.password is not None

    def test_is_a_valid_password(self, app):
        user = db.session.get(User, 1)

        assert user.password is not None

        assert user.is_a_valid_password(self.VALID_PASSWORD) is True

        assert user.is_a_valid_password(self.INVALID_PASSWORD) is False

    @pytest.mark.parametrize(
        "password, error_message",
        [
            (123456789, "Votre mot de passe doit être de type str !"),
            ("pw", "Votre mot de passe doit contenir au minimum 8 caractères !"),
            (
                "123456789",
                "Votre mot de passe ne peut pas être entièrement numérique !",
            ),
            ("password", "Votre mot de passe doit contenir au moins un chiffre !"),
            (
                "password18",
                "Votre mot de passe doit contenir au moins une lettre majuscule !",
            ),
            (
                "PASSWORD18",
                "Votre mot de passe doit contenir au moins une lettre minuscule !",
            ),
            (
                "pASSWORD18",
                "Votre mot de passe doit contenir au moins un caractère spécial !",
            ),
        ],
    )
    def test_validate_password(self, app, password, error_message):
        user = db.session.get(User, 1)

        with pytest.raises(ValueError, match=error_message):
            user.password = password

    def test_generate_reset_token(self, app):
        user = db.session.get(User, 1)

        # 0. checking that the retrieved user has no token
        assert user.token is None
        assert user.token_expiration_date is None

        # 1. generating token
        user.generate_reset_token()

        # 2. checking user.token
        assert user.token is not None
        assert len(user.token) >= User.TOKEN_LENGTH

        # 3. checking user.token_expiration_date
        assert user.token_expiration_date is not None
        assert user.token_expiration_date > datetime.utcnow()

    def test_init_db(self, app):
        self._drop_and_create_db()

        admin = User.query.filter_by(
            role="admin",
            first_name="Sys",
            last_name="Moderator",
            birthdate=date(2001, 1, 1),
            email="admin@admin.com",
        ).first()

        assert admin is None

        secretary_1 = User.query.filter_by(
            role="secretary",
            first_name="John",
            last_name="Doe",
            birthdate=date(2001, 1, 1),
            email="john@simplylift.co",
        ).first()

        assert secretary_1 is None

        secretary_2 = User.query.filter_by(
            role="secretary",
            first_name="Iron",
            last_name="Man",
            birthdate=date(2001, 1, 1),
            email="admin@irontemple.com",
        ).first()

        assert secretary_2 is None

        secretary_3 = User.query.filter_by(
            role="secretary",
            first_name="Kate",
            last_name="Woman",
            birthdate=date(2001, 1, 1),
            email="kate@shelifts.co.uk",
        ).first()

        assert secretary_3 is None

        User.init_db()

        admin = User.query.filter_by(
            role="admin",
            first_name="Sys",
            last_name="Moderator",
            birthdate=date(2001, 1, 1),
            email="admin@admin.com",
        ).first()

        assert admin is not None
        assert admin.is_a_valid_password(self.VALID_PASSWORD)

        secretary_1 = User.query.filter_by(
            role="secretary",
            first_name="John",
            last_name="Doe",
            birthdate=date(2001, 1, 1),
            email="john@simplylift.co",
        ).first()

        assert secretary_1 is not None
        assert secretary_1.is_a_valid_password(self.VALID_PASSWORD)

        secretary_2 = User.query.filter_by(
            role="secretary",
            first_name="Iron",
            last_name="Man",
            birthdate=date(2001, 1, 1),
            email="admin@irontemple.com",
        ).first()

        assert secretary_2 is not None
        assert secretary_2.is_a_valid_password(self.VALID_PASSWORD)

        secretary_3 = User.query.filter_by(
            role="secretary",
            first_name="Kate",
            last_name="Woman",
            birthdate=date(2001, 1, 1),
            email="kate@shelifts.co.uk",
        ).first()

        assert secretary_3 is not None
        assert secretary_3.is_a_valid_password(self.VALID_PASSWORD)
