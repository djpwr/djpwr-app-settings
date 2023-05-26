from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _

from djpwr.managers import get_model, get_manager


class AppConfig(BaseAppConfig):
    name = 'djpwr_app_settings'
    label = 'app_settings'
    verbose_name = _("Application settings")

    def ready(self):
        try:
            from .models import MODEL_LABELS

            # Generate SettingGroups and ApplicationSettings for all registered models
            for model_label in MODEL_LABELS:
                model_class = get_model(model_label)

                group_name = model_class.name_from_class()

                setting_group = get_manager('app_settings.SettingGroup').create_group(group_name)

                get_manager('app_settings.ApplicationSetting').create_for_group(setting_group)
        except:
            # Bootstrapping: Migrations need to be run before the above will work.
            pass
