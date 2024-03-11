from pathlib import Path

UTM_SOURCE = 'automation'

current_file = Path(__file__)
ROOT_DIR = Path(current_file.parent.parent)

# Closer
CLOSER_CONFIGS_DIR = Path(ROOT_DIR/ "closer_configs" / "configs")
# Closer config json
CLOSER_ONBOARDING_URLS = Path(CLOSER_CONFIGS_DIR / "onboarding_urls_config.json")
CLOSER_EMAIL_ALIAS_CONFIG = Path(CLOSER_CONFIGS_DIR / "email_alias_config.json")
CLOSER_EXPECTED_PAGES_CONFIG = Path(CLOSER_CONFIGS_DIR / "expected_pages_config.json")
CLOSER_EVENTS_LIST_CONFIG = Path(CLOSER_CONFIGS_DIR / "events_list_config.json")
CLOSER_ONBOARDING_EVENTS_CONFIG = Path(CLOSER_CONFIGS_DIR / "onboarding_events_config.json")
CLOSER_LANDING_TYPES_LIST_CONFIG = Path(CLOSER_CONFIGS_DIR / "landing_types_list_config.json")
CLOSER_ONBOARDING_LANDING_TYPES_CONFIG = Path(CLOSER_CONFIGS_DIR / "onboarding_landing_types_config.json")
CLOSER_SUBSCRIPTION_LIST_CONFIG = Path(CLOSER_CONFIGS_DIR / "subscriptions_list_config.json")
CLOSER_ONBOARDING_SUBSCRIPTIONS_CONFIG = Path(CLOSER_CONFIGS_DIR / "onboarding_subscriptions_config.json")
CLOSER_3DS_SETTINGS_CONFIG = Path(CLOSER_CONFIGS_DIR / "supported_3ds_settings_config.json")

BASIC_CONFIG_DIR = Path(ROOT_DIR / "basic_configs")

# basic config jsons
ANALYTICS_SYSTEMS_URLS_CONFIG = Path(BASIC_CONFIG_DIR / "analytics_systems_urls_config.json")
PAYMENT_CARDS_CONFIG = Path(BASIC_CONFIG_DIR / "payment_cards_config.json")
