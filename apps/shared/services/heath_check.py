

from ecom.settings import CHAT_ID_TELEGRAM_BOT

from ecom.services.telegram_service import send_telegram_message

from ..utils import utils_health_check as ut_hc
class HealthCheckServices:
    def health_check():
        details = {
            "database": ut_hc.check_database(),
            "redis_auth": ut_hc.check_redis(alias="auth"),
            "redis_default": ut_hc.check_redis(alias="default"),
            "minio": ut_hc.check_minio(),
            "kafka": ut_hc.check_kafka(),
        }
        critical_services = [name for name, status in details.items() if status == "CRITICAL"]
        warning_services = [name for name, status in details.items() if status == "WARNING"]
        if critical_services:
            overall_status = "CRITICAL"
            services_str = ", ".join(critical_services)
            message = f"[HEALTH CHECK] {overall_status}\nServices Down: {services_str}"
            
            send_telegram_message(
                chat_id=CHAT_ID_TELEGRAM_BOT,
                message=message
            )
        elif warning_services:
            overall_status = "WARNING"
        else:
            overall_status = "NORMAL"
        return {
            "status": overall_status,
            "details": details
        }