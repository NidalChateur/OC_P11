from wtforms import PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired

from authentication_app.models.user import User

from . import MixinEmail, MixinNewPassword, MixinPasswordConfirm, admin


class SignupForm(admin.CreateUserForm):
    role = None
    submit = SubmitField("Envoyer")


class LoginForm(MixinEmail):
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")

    def validate(self) -> bool:
        """multi field validator :
        check if the email and password are valid to login"""

        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        user = User.query.filter_by(email=self.email.data).first()

        # check if the email exists
        if user is None:
            self.email.errors.append(
                "Cet e-mail n'est pas enregistré. Veuillez vous inscrire d'abord."
            )

            return False

        # check if the user account is active
        if not user.is_activated:
            self.email.errors.append(
                "Compte en attente d'activation par l'administrateur."
            )

            return False

        # check if the user password is correct
        if not user.is_a_valid_password(self.password.data):
            self.password.errors.append("Mot de passe incorrect !")

            return False

        return True


class ForgottenPasswordForm(MixinEmail):
    submit = SubmitField("Demander la réinitialisation de mon mot de passe")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data.lower()).first()
        if not user:
            raise ValidationError(
                "Aucun utilisateur n'est enregistré avec cette adresse email."
            )


class ResetPasswordForm(MixinNewPassword, MixinPasswordConfirm):
    submit = SubmitField("Réinitialiser mon mot de passe")
