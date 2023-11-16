from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, Length, NumberRange

from authentication_app.models.user import User

from ..models.club import Club


class MixinEmail(FlaskForm):
    email = StringField(
        "Adresse e-mail du secrétaire",
        description="Le club sera assigné au compte du secrétaire.",
    )


class MixinEmailCreation(MixinEmail):
    def validate_email(self, field):
        secretary = User.query.filter_by(email=field.data.lower()).first()
        if not secretary:
            raise ValidationError(
                "Aucun compte secrétaire n'est associé à cet e-mail !"
            )

        if secretary:
            secretary_has_club = Club.query.filter_by(secretary_id=secretary.id).first()
            if secretary_has_club:
                raise ValidationError("Ce secrétaire est déjà assigné à un club !")


class MixinEmailUpdate(MixinEmail):
    def validate_email(self, field):
        if field.data:
            secretary = User.query.filter_by(email=field.data).first()
            if not secretary:
                raise ValidationError(
                    "Aucun compte secrétaire n'est associé à cet e-mail !"
                )


class MixinName(FlaskForm):
    name = StringField("Nom", validators=[DataRequired(), Length(min=2, max=50)])


class MixinClubNameCreation(MixinName):
    def validate_name(self, field):
        if field.data:
            name_is_not_unique = Club.query.filter_by(name=field.data.title()).first()
            if name_is_not_unique:
                raise ValidationError("Ce nom de club est déjà utilisé !")


class MixinPoints(FlaskForm):
    points = IntegerField("Points", validators=[NumberRange(min=0)], default=10)
