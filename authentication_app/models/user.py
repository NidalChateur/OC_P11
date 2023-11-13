""" 
flask shell : 
from authentication_app.models import User
from datetime import date
d=date(1999,1,1)
user=User(role="admin", first_name="john", last_name="doe", birthdate=d, email="admin@gmail.com")
 """

import re
import secrets
from datetime import date, datetime, timedelta

from flask_login import UserMixin
from . import CrudMixin, db, bcrypt
from sqlalchemy.orm import validates


class User(db.Model, CrudMixin, UserMixin):
    IMAGE_PATH = "img/profile_photo/"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum("admin", "secretary"), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    is_activated = db.Column(db.Boolean, default=True)
    image = db.Column(db.String(255), nullable=True)
    token = db.Column(db.String(100), nullable=True, unique=True)
    token_expiration_date = db.Column(db.DateTime, nullable=True)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(
        self, role: str, first_name: str, last_name: str, birthdate: date, email: str
    ):
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.email = email

    def __str__(self) -> str:
        user_id = f"id : {self.id}"
        user_role = f"role : {self.role}"
        user_full_name = f"first_name : {self.first_name}, last_name : {self.last_name}"
        user_birthdate = f"birthdate : {self.birthdate_formatter}"
        user_email = f"email : {self.email}"
        user_image = f"image : {self.image}"

        if self.image:
            return f"{user_id}, {user_role}, {user_full_name}, {user_birthdate}, {user_email}, {user_image}"
        return (
            f"{user_id}, {user_role}, {user_full_name}, {user_birthdate}, {user_email}"
        )

    def __repr__(self) -> str:
        return str(self)

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    @property
    def birthdate_formatter(self) -> str:
        birthdate = self.birthdate

        return f"{birthdate.day} {self.MONTHS[birthdate.month-1]} {birthdate.year}"

    def _validate_password(self, password: str):
        if not isinstance(password, str):
            raise ValueError("Votre mot de passe doit être du type str (string)")

        if len(password) < 8:
            raise ValueError(
                "Votre mot de passe doit contenir au minimum 8 caractères."
            )
        if password.isdigit():
            raise ValueError(
                "Votre mot de passe ne peut pas être entièrement numérique."
            )
        if password.isalpha():
            raise ValueError("Votre mot de passe doit contenir au moins un chiffre.")

        if not re.search(r"[A-Z]", password):
            raise ValueError(
                "Votre mot de passe doit contenir au moins une lettre majuscule."
            )
        if not re.search(r"[a-z]", password):
            raise ValueError(
                "Votre mot de passe doit contenir au moins une lettre minuscule."
            )

        if all([character in password for character in self.SPECIAL_CHARACTERS]):
            raise ValueError(
                "Votre mot de passe doit contenir au moins un caractère spécial."
            )

    def set_password(self, password: str):
        """hash and save the password in db,
        used to create the password"""

        self._validate_password(password)
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.save()

    def is_a_valid_password(self, password: str) -> bool:
        """check the password entered by the user before login,
        used in login view"""

        # the first argument is the hashed password and the second the clear one
        # entered by the user in form
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def age(birthdate: date) -> int:
        """return the user age from his birthdate"""

        today = date.today()
        age = (
            today.year
            - birthdate.year
            - ((today.month, today.day) < (birthdate.month, birthdate.day))
        )

        return age

    @validates("birthdate")
    def validate_date_of_birth(self, key, value):
        """check if the user age is > 18"""

        if self.age(value) < 18:
            raise ValueError("L'utilisateur doit être majeur (18 ans ou plus).")
        return value

    @validates("email")
    def validate_email(self, key, value):
        """check the email format and if the email is unique in db,
        email format should be like xxxxx@xxxx.xx"""

        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Adresse e-mail invalide")

        used_email = User.query.filter_by(email=value).first()

        # case when the user is already registered
        if self.id and self.email != value and used_email:
            raise ValueError("Cet e-mail est déjà utilisé par un utilisateur !")

        # case when the user is being registered
        if not self.id and used_email:
            raise ValueError("Cet e-mail est déjà utilisé par un utilisateur !")

        return value

    @validates("password")
    def validate_password(self, key, value):
        """check the password complexity"""

        if value:
            self._validate_password(value)

        return value

    def generate_reset_token(self):
        self.token = secrets.token_urlsafe(32)
        self.token_expiration_date = datetime.utcnow() + timedelta(hours=1)
        self.save()

    @staticmethod
    def create_admin():
        user = User(
            role="admin",
            first_name="admin",
            last_name="admin",
            birthdate=date(2000, 1, 1),
            email="admin@gmail.com",
        )
        user.create()
        user.set_password("00000000pW-")
