from django.db import connections
from django.db.backends.signals import connection_created
from apps.logging.sql import QueryLogger

def setup_sql_logger():
    def _attach_wrapper(sender, connection, **kwargs):
        if not hasattr(connection, "_query_logger_attached"):
            connection.execute_wrappers.append(QueryLogger())
            connection._query_logger_attached = True
    connection_created.connect(_attach_wrapper)
