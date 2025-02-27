# Python imports
import os

# Django imports
from django.core.management.base import BaseCommand
from django.conf import settings

# Module imports
from plane.license.models import InstanceConfiguration
from plane.app.views.oidc import get_endpoint_information


class Command(BaseCommand):
    help = "Configure instance variables"

    def handle(self, *args, **options):
        from plane.license.utils.encryption import encrypt_data

        config_keys = [
            # Authentication Settings
            {
                "key": "ENABLE_SIGNUP",
                "value": os.environ.get("ENABLE_SIGNUP", "1"),
                "category": "AUTHENTICATION",
                "is_encrypted": False,
            },
            {
                "key": "ENABLE_EMAIL_PASSWORD",
                "value": os.environ.get("ENABLE_EMAIL_PASSWORD", "1"),
                "category": "AUTHENTICATION",
                "is_encrypted": False,
            },
            {
                "key": "ENABLE_MAGIC_LINK_LOGIN",
                "value": os.environ.get("ENABLE_MAGIC_LINK_LOGIN", "0"),
                "category": "AUTHENTICATION",
                "is_encrypted": False,
            },
            {
                "key": "GOOGLE_CLIENT_ID",
                "value": os.environ.get("GOOGLE_CLIENT_ID"),
                "category": "GOOGLE",
                "is_encrypted": False,
            },
            {
                "key": "GITHUB_CLIENT_ID",
                "value": os.environ.get("GITHUB_CLIENT_ID"),
                "category": "GITHUB",
                "is_encrypted": False,
            },
            {
                "key": "GITHUB_CLIENT_SECRET",
                "value": os.environ.get("GITHUB_CLIENT_SECRET"),
                "category": "GITHUB",
                "is_encrypted": True,
            },
            # OIDC Block START - Don't change the order!!!
            {
                "key": "OIDC_AUTO",
                "value": os.environ.get("OIDC_AUTO", "0"),
                "category": "OIDC",
                "is_encrypted": False,
            },
            {
                "key": "OIDC_DISCOVERY",
                "value": os.environ.get("OIDC_DISCOVERY"),
                "category": "OIDC",
                "is_encrypted": False,
            },
            {
                "key": "OIDC_CLIENT_ID",
                "value": os.environ.get("OIDC_CLIENT_ID"),
                "category": "OIDC",
                "is_encrypted": False,
            },
            {
                "key": "OIDC_CLIENT_SECRET",
                "value": os.environ.get("OIDC_CLIENT_SECRET"),
                "category": "OIDC",
                "is_encrypted": True,
            }, 
            {
                "key": "OIDC_URL_AUTHORIZATION",
                "value": os.environ.get("OIDC_URL_AUTHORIZATION"),
                "category": "OIDC",
                "is_encrypted": False,
            },
            {
                "key": "OIDC_URL_TOKEN",
                "value": os.environ.get("OIDC_URL_TOKEN"),
                "category": "OIDC",
                "is_encrypted": False,
            },
            {
                "key": "OIDC_URL_USERINFO",
                "value": os.environ.get("OIDC_URL_USERINFO"),
                "category": "OIDC",
                "is_encrypted": False,
            },
            {
                "key": "OIDC_URL_ENDSESSION",
                "value": os.environ.get("OIDC_URL_ENDSESSION"),
                "category": "OIDC",
                "is_encrypted": False,
            },
            # OIDC Block END - Don't change the order!!!
            {
                "key": "EMAIL_HOST",
                "value": os.environ.get("EMAIL_HOST", ""),
                "category": "SMTP",
                "is_encrypted": False,
            },
            {
                "key": "EMAIL_HOST_USER",
                "value": os.environ.get("EMAIL_HOST_USER", ""),
                "category": "SMTP",
                "is_encrypted": False,
            },
            {
                "key": "EMAIL_HOST_PASSWORD",
                "value": os.environ.get("EMAIL_HOST_PASSWORD", ""),
                "category": "SMTP",
                "is_encrypted": True,
            },
            {
                "key": "EMAIL_PORT",
                "value": os.environ.get("EMAIL_PORT", "587"),
                "category": "SMTP",
                "is_encrypted": False,
            },
            {
                "key": "EMAIL_FROM",
                "value": os.environ.get("EMAIL_FROM", ""),
                "category": "SMTP",
                "is_encrypted": False,
            },
            {
                "key": "EMAIL_USE_TLS",
                "value": os.environ.get("EMAIL_USE_TLS", "1"),
                "category": "SMTP",
                "is_encrypted": False,
            },
            {
                "key": "OPENAI_API_KEY",
                "value": os.environ.get("OPENAI_API_KEY"),
                "category": "OPENAI",
                "is_encrypted": True,
            },
            {
                "key": "GPT_ENGINE",
                "value": os.environ.get("GPT_ENGINE", "gpt-3.5-turbo"),
                "category": "SMTP",
                "is_encrypted": False,
            },
            {
                "key": "UNSPLASH_ACCESS_KEY",
                "value": os.environ.get("UNSPLASH_ACESS_KEY", ""),
                "category": "UNSPLASH",
                "is_encrypted": True,
            },
        ]

        # Autodiscovery of Settings for OIDC based on the OIDC_DISCOVERY
        for item in config_keys:
            if item.get("key") == "OIDC_DISCOVERY" and item.get("value"):
                (
                    OIDC_URL_AUTHORIZATION, 
                    OIDC_URL_TOKEN, 
                    OIDC_URL_USERINFO, 
                    OIDC_URL_ENDSESSION
                ) = get_endpoint_information(item.get("value"))
                issuerIndex = config_keys.index(item)
                config_keys[issuerIndex + 3]["value"] = OIDC_URL_AUTHORIZATION
                config_keys[issuerIndex + 4]["value"] = OIDC_URL_TOKEN
                config_keys[issuerIndex + 5]["value"] = OIDC_URL_USERINFO
                config_keys[issuerIndex + 6]["value"] = OIDC_URL_ENDSESSION
                config_keys.pop(issuerIndex)

        for item in config_keys:
            obj, created = InstanceConfiguration.objects.get_or_create(
                key=item.get("key")
            )
            if created:
                obj.category = item.get("category")
                obj.is_encrypted = item.get("is_encrypted", False)
                if item.get("is_encrypted", False):
                    obj.value = encrypt_data(item.get("value"))
                else:
                    obj.value = item.get("value")
                obj.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{obj.key} loaded with value from environment variable."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"{obj.key} configuration already exists"
                    )
                )
