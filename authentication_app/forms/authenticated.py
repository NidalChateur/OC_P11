from wtforms import SubmitField

from . import (
    MixinImage,
    MixinNewPassword,
    MixinOldPassword,
    MixinPasswordConfirm,
    admin,
)


class UpdateMyProfileForm(admin.UpdateUserForm):
    role = None


class AddMyPhotoForm(MixinImage):
    submit = SubmitField("Enregistrer")


class ChangeMyPasswordForm(MixinOldPassword, MixinNewPassword, MixinPasswordConfirm):
    submit = SubmitField("Enregistrer")
