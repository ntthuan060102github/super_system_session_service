import importlib
import pkgutil
from django.urls import path, include
from django.apps import apps

parent_module = __import__("appbase.routes", fromlist=[""])
package_path = parent_module.__path__[0]
child_modules = [module_name for _, module_name, _ in pkgutil.iter_modules([package_path])]

urls = []

for module in child_modules:
    urls += importlib.import_module(f"appbase.routes.{module}").urls

urlpatterns = [path(apps.get_app_config("appbase").api_prefix, include(urls))]