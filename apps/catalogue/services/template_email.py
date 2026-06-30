

from ..repositories.template_email import template_email_repository
from apps.logging import logging_log as lg

class TemplateEmailService:
    def get_template_by_code(self, code, is_active=True):
        try:
            return template_email_repository.template_email_repository(code, is_active)
        except Exception as e:
            lg.log_error("[ERROR] get_template_by_code",code=code,is_active=is_active,error=str(e))
            return None
template_email_service = TemplateEmailService()