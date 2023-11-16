import mimetypes
import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from PIL import Image
from wtforms import DateField, PasswordField, SelectField, StringField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from authentication_app.models.user import User


class MixinRole(FlaskForm):
    role = SelectField(
        "Rôle",
        choices=[("admin", "Administrateur"), ("secretary", "Secrétaire")],
        validators=[DataRequired()],
    )


class MixinName(FlaskForm):
    first_name = StringField("Prénom", validators=[DataRequired()])
    last_name = StringField("Nom", validators=[DataRequired()])


class MixinBirthdate(FlaskForm):
    birthdate = DateField(
        "Date de naissance", format="%Y-%m-%d", validators=[DataRequired()]
    )

    def validate_birthdate(self, field):
        if User.age(field.data) < 18:
            raise ValidationError("L'utilisateur doit être majeur (18 ans ou plus).")


class MixinEmail(FlaskForm):
    email = StringField(
        "Adresse e-mail",
        validators=[DataRequired(), Email()],
    )


class MixinEmailCreation(MixinEmail):
    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Cet e-mail est déjà utilisé par un utilisateur.")


class MixinOldPassword(FlaskForm):
    old_password = PasswordField("Ancien mot de passe", validators=[DataRequired()])


class MixinPassword(FlaskForm):
    password = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired(),
            EqualTo("password_confirm", "Les mots de passe ne correspondent pas."),
        ],
        description="Votre mot de passe doit contenir au minimum 8 caractères,"
        + " un chiffre, une lettre, une majuscule, une miniscule et un caractère spécial",
    )


class MixinNewPassword(FlaskForm):
    password = PasswordField(
        "Nouveau mot de passe",
        validators=[
            DataRequired(),
            EqualTo("password_confirm", "Les mots de passe ne correspondent pas."),
        ],
        description="Votre mot de passe doit contenir au minimum 8 caractères, un chiffre,"
        + " une lettre, une majuscule, une miniscule et un caractère spécial.",
    )


class MixinPasswordConfirm(FlaskForm):
    password_confirm = PasswordField(
        "Confirmer mot de passe",
        validators=[
            DataRequired(),
        ],
    )

    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError(
                "Votre mot de passe doit contenir au minimum 8 caractères."
            )
        if field.data.isdigit():
            raise ValidationError(
                "Votre mot de passe ne peut pas être entièrement numérique."
            )
        if field.data.isalpha():
            raise ValidationError(
                "Votre mot de passe doit contenir au moins un chiffre."
            )

        if not re.search(r"[A-Z]", field.data):
            raise ValidationError(
                "Votre mot de passe doit contenir au moins une lettre majuscule."
            )
        if not re.search(r"[a-z]", field.data):
            raise ValidationError(
                "Votre mot de passe doit contenir au moins une lettre minuscule."
            )

        if all([character in field.data for character in User.SPECIAL_CHARACTERS]):
            raise ValidationError(
                "Votre mot de passe doit contenir au moins un caractère spécial."
            )


class MixinPasswordCreation(MixinPassword, MixinPasswordConfirm):
    pass


class MixinImage(FlaskForm):
    MAX_IMAGE_FILE_SIZE = 5 * 1024 * 1024
    ALLOWED_MIME_TYPES = [
        "image/jpg",
        "image/png",
        "image/jpeg",
        "image/gif",
        "image/bmp",
        "image/ico",
        "image/tiff",
    ]

    image = FileField(
        "Photo de profil",
        validators=[FileAllowed(User.ALLOWED_IMAGE_EXTENSION)],
    )

    def validate_image(self, field):
        """check
        1. if the image integrity with PIL.Image and mimetypes
        2. check if the image size (should be < 5MB)"""

        if field.data:
            try:
                img = Image.open(field.data)
                img.verify()
            except Exception:
                raise ValidationError("Type de fichier non autorisé !")

            file_mime_type, _ = mimetypes.guess_type(field.data.filename)
            if file_mime_type not in self.ALLOWED_MIME_TYPES:
                raise ValidationError("Type de fichier non autorisé !")

            if len(field.data.read()) > self.MAX_IMAGE_FILE_SIZE:
                raise ValidationError("La taille du fichier ne doit pas dépasser 5Mo !")
