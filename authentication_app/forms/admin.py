from wtforms import SubmitField

from . import (
    MixinBirthdate,
    MixinEmail,
    MixinEmailCreation,
    MixinImage,
    MixinName,
    MixinPasswordCreation,
    MixinRole,
)


class CreateUserForm(
    MixinRole,
    MixinName,
    MixinBirthdate,
    MixinEmailCreation,
    MixinImage,
    MixinPasswordCreation,
):
    submit = SubmitField("Enregistrer")


class UpdateUserForm(MixinRole, MixinName, MixinBirthdate, MixinEmail):
    submit = SubmitField("Enregistrer")
