from wtforms import SubmitField

from . import MixinNumberOfSpots


class CreateReservationForm(MixinNumberOfSpots):
    submit = SubmitField("Réserver")
