from djpwr.managers import get_model, get_manager

default_app_config = 'djpwr.app_settings.apps.AppConfig'


class AppSettingDict:
    def __getitem__(self, setting_label):
        app_label, model_name, setting_name = setting_label.split('.')

        setting = get_manager('app_settings.ApplicationSetting').get(
            group__group_name='.'.join([app_label, model_name]),
            name=setting_name
        )

        return setting.value

    def __setitem__(self, setting_label, value):
        app_label, model_name, setting_name = setting_label.split('.')

        setting_group = get_model('.'.join([app_label, model_name]))

        setting = get_manager('app_settings.ApplicationSetting').get(
            group__group_name='.'.join([app_label, model_name]),
            name=setting_name
        )
        setting.value = value
        setting.save()

        get_manager('app_settings.SettingGroup').touch_last_modified(setting_group)


app_settings = AppSettingDict()

APP_SETTINGS = app_settings
