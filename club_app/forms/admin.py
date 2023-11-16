from wtforms import SubmitField

from . import (
    MixinClubNameCreation,
    MixinEmailCreation,
    MixinEmailUpdate,
    MixinName,
    MixinPoints,
)


class CreateClubForm(
    MixinEmailCreation,
    MixinClubNameCreation,
    MixinPoints,
):
    submit = SubmitField("Enregistrer")


class UpdateClubForm(
    MixinEmailUpdate,
    MixinName,
    MixinPoints,
):
    submit = SubmitField("Enregistrer")
