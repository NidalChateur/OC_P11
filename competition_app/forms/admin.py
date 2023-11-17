from wtforms import SubmitField

from . import MixinCapacity, MixinCompetitionNameCreation, MixinStartDate


class CreateCompetitionForm(
    MixinCompetitionNameCreation,
    MixinStartDate,
    MixinCapacity,
):
    submit = SubmitField("Enregistrer")
