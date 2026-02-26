
from ..utils import utils_health_check as ut_hc
class HealthCheckServices:
    def health_check():
        return {
            "database": ut_hc.check_database(),
            "redis_auth": ut_hc.check_redis(alias="auth"),
            "redis_default": ut_hc.check_redis(alias="default"),
            "minio": ut_hc.check_minio(),
            "kafka": ut_hc.check_kafka(),
        }