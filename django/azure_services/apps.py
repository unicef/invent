from django.apps import AppConfig


# Created new app to avoid conflicts with the azure package
class AzureConfig(AppConfig):
    name = "azure_services"
