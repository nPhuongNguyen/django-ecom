import time
from apps.logging import logging_log as lg


class QueryLogger:
    def __init__(self):
        self.queries = []

    def __call__(self, execute, sql, params, many, context):
        # start = time.monotonic()
        start = time.perf_counter()

        try:
            result = execute(sql, params, many, context)
            return result
        except Exception as e:
            # duration_ms = (time.monotonic() - start) * 1000
            duration_ms = (time.perf_counter() - start) * 1000
            lg.log_error(
                message="[SQL][ERROR]",
                sql=sql,
                params=params,
                many=many,
                duration_ms=round(duration_ms, 3),
                error=str(e),
            )
        finally:
            # Sử dụng per_couter thay vì monotonic để đo thời gian chính xác hơn
            # duration_ms = (time.monotonic() - start) * 1000
            duration_ms = (time.perf_counter() - start) * 1000

            log_data = {
                "sql": sql,
                "params": params,
                "many": many,
                "duration": f"{round(duration_ms, 3)} ms",
            }

            lg.log_info(
                message="[SQL][EXECUTED]",
                **log_data
            )

            self.queries.append(log_data)