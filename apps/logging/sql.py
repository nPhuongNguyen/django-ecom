import time
from apps.logging import logging as lg
import apps.utils as utils
class QueryLogger:
    def __init__(self):
        self.queries = []

    def __call__(self, execute, sql, params, many, context):
        start = time.monotonic()
        try:
            result = execute(sql, params, many, context)
        except Exception as e:
            status = "ERROR"
            lg.log_error(
                message=f"[SQL {status}] {sql} | params={params} | error={str(e)}"
            )
            raise
        else:
            status = "OK"
            return result
        finally:
            duration = time.monotonic() - start
            self.queries.append({
                "sql": sql,
                "params": params,
                "duration": duration,
                "status": status
            })
            lg.log_info(
                message=f"[SQL {status}] {sql} | params={params} | duration={duration:.6f}s"
            )
            