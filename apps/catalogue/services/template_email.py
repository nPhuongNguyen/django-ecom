

from ..repositories.template_email import TemplateEmailRepository
from apps.logging import logging_log as lg

class TemplateEmailService:
    def __init__(self):
        self.template_email_repository = TemplateEmailRepository()

    def get_template_by_code(self, code, is_active=True):
        try:
            return self.template_email_repository.template_email_repository(code, is_active)
        except Exception as e:
            lg.log_error("[ERROR] get_template_by_code",code=code,is_active=is_active,error=str(e))
            return None