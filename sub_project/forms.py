from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget = forms.EmailInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Enter your email",
            }
        )
        self.fields["email"].label = ""

    def get_users(self, email):
        # 이메일 필터링 로직 (활성화된 사용자만 가져오기)
        users = super().get_users(email)
        active_users = [user for user in users if user.is_active]
        return active_users


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Enter new password",
            }
        )
        self.fields["new_password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Confirm new password",
            }
        )
        self.fields["new_password1"].label = ""
        self.fields["new_password2"].label = ""
