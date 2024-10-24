from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import action
from rest_framework.request import Request
from django.db import connection
from django_redis import get_redis_connection
import logging

class HealthView(ViewSet):
    authentication_classes = ()

    @action(["GET"], detail=False, url_path="check")
    def health(self, request: Request):
        data = {
            "base_url": request.build_absolute_uri(),
            "main_database": self.__get_main_database_connection_info(),
            "cache_database": self.__get_redis_connection_info()
        }
        logging.getLogger(__name__).info("HealthView.health data=%s", data)
        return Response(data=data, status=HTTP_200_OK)
    
    def __get_redis_connection_info(self):
        try:
            redis_connection = get_redis_connection("default")
            conn_kwagrs = redis_connection.connection_pool.connection_kwargs
            conn_inf = {
                "status": redis_connection.ping(),
                "host": conn_kwagrs['host'],
                "port": conn_kwagrs['port'],
                "database": conn_kwagrs.get('db', '-')
            }
            return conn_inf
        except Exception as e:
            return {
                "status": False,
                "error": str(e)
            }
        
    def __get_main_database_connection_info(self):
        try:
            main_database_connection = connection
            return {
                "status": main_database_connection.ensure_connection() == None
            }
        except Exception as e:
            return {
                "status": False,
                "error": str(e)
            }