from wtforms import SubmitField

from . import MixinClubNameCreation, MixinName


class CreateClubForm(MixinClubNameCreation):
    submit = SubmitField("Enregistrer")


class UpdateClubForm(MixinName):
    submit = SubmitField("Enregistrer")
