

from ...auth.models.send_mail import TemplateEmail


class TemplateEmailRepository:
    _teamplate_model = TemplateEmail

    def template_email_repository(self, code, is_active):
        return self._teamplate_model.objects.filter(code=code, is_active=is_active).first()