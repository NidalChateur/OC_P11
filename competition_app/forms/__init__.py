from datetime import datetime, time, timedelta

from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, TimeField, ValidationError
from wtforms.validators import DataRequired, NumberRange

from club_app.forms import MixinName

from ..models.competition import Competition


class MixinCompetitionNameCreation(MixinName):
    def validate_name(self, field):
        if field.data:
            name_is_not_unique = Competition.query.filter_by(
                name=field.data.title()
            ).first()
            if name_is_not_unique:
                raise ValidationError("Ce nom de compétition est déjà utilisé !")


class MixinStartDate(FlaskForm):
    start_date = DateField(
        "Date de début de la compétition", validators=[DataRequired()]
    )
    start_hour = TimeField(
        "Heure de début de la compétition",
        validators=[DataRequired()],
        default=time(0, 0),
    )

    def validate_start_date(self, field):
        if field.data < datetime.utcnow().date() + timedelta(days=7):
            raise ValidationError(
                "Le début de la compétition ne doit pas commencer avant 7 jours !"
            )


class MixinCapacity(FlaskForm):
    capacity = IntegerField(
        "Nombre de places réservable",
        validators=[NumberRange(min=1)],
        default=50,
    )


class MixinNumberOfSpots(FlaskForm):
    number_of_spots = IntegerField(
        "Nombre de places à réserver",
        validators=[NumberRange(min=1, max=12)],
        description="12 maximum, sous condition de points de club et de places restantes dans la compétition.",
    )
