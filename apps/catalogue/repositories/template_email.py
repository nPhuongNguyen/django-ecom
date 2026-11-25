

from ...auth.models.send_mail import TemplateEmail


class TemplateEmailRepository:
    _teamplate_model = TemplateEmail

    def get_by_code(self, code):
        return self._teamplate_model.objects.filter(code=code).first()
    
template_email_repository = TemplateEmailRepository()