"""Constants for the Torn City integration."""

DOMAIN = "torn"

# API Configuration
API_BASE_URL = "https://api.torn.com"
API_TIMEOUT = 10
API_RATE_LIMIT = 100  # requests per minute

# Configuration
CONF_API_KEY = "api_key"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_THROTTLE_API = "throttle_api"
CONF_ENABLE_MONEY = "enable_money"
CONF_ENABLE_TRAVEL = "enable_travel"
CONF_ENABLE_COOLDOWNS = "enable_cooldowns"
CONF_ENABLE_STATS = "enable_stats"
CONF_ENABLE_SKILLS = "enable_skills"
CONF_ENABLE_COMPANY = "enable_company"
CONF_ENABLE_STOCKS = "enable_stocks"
CONF_ENABLE_REFILLS = "enable_refills"
CONF_ENABLE_LOG = "enable_log"

# Default values
DEFAULT_SCAN_INTERVAL = 1

# Cache durations for different endpoint types (in seconds)
CACHE_DURATION_SHORT = 5
CACHE_DURATION_MEDIUM = 60
CACHE_DURATION_LONG = 600

# Endpoint categories and their mapping
# Each category can be enabled/disabled in options
ENDPOINT_CATEGORIES = {
    "core": {
        "name": "Profile & Bars",
        "description": "Essential player information (always enabled)",
        "enabled_by_default": True,
        "can_disable": False,
        "endpoints": [
            {"path": "/v2/user/basic", "key": "profile", "cache_for": CACHE_DURATION_SHORT},
            {"path": "/v2/user/bars", "key": "bars", "cache_for": CACHE_DURATION_SHORT},
        ],
    },
    CONF_ENABLE_MONEY: {
        "name": "Money & Banking",
        "description": "Wallet, vault, banks, faction funds",
        "enabled_by_default": True,
        "can_disable": True,
        "endpoints": [
            {"path": "/v2/user/money", "key": "money", "cache_for": CACHE_DURATION_SHORT},
        ],
    },
    CONF_ENABLE_TRAVEL: {
        "name": "Travel",
        "description": "Travel status and destination",
        "enabled_by_default": True,
        "can_disable": True,
        "endpoints": [
            {"path": "/v2/user/travel", "key": "travel", "cache_for": CACHE_DURATION_SHORT},
        ],
    },
    CONF_ENABLE_COOLDOWNS: {
        "name": "Cooldowns",
        "description": "Drug, medical, booster cooldowns",
        "enabled_by_default": True,
        "can_disable": True,
        "endpoints": [
            {"path": "/v2/user/cooldowns", "key": "cooldowns", "cache_for": CACHE_DURATION_MEDIUM},
        ],
    },
    CONF_ENABLE_STATS: {
        "name": "Personal Stats",
        "description": "Personal statistics",
        "enabled_by_default": True,
        "can_disable": True,
        "endpoints": [
            {"path": "/v2/user/personalstats", "key": "personalstats", "params": {"cat": "all"}, "cache_for": CACHE_DURATION_MEDIUM},
        ],
    },
    CONF_ENABLE_SKILLS: {
        "name": "Skills",
        "description": "Player skills",
        "enabled_by_default": True,
        "can_disable": True,
        "endpoints": [
            {"path": "/v2/user/skills", "key": "skills", "cache_for": CACHE_DURATION_LONG},
        ],
    },
    CONF_ENABLE_COMPANY: {
        "name": "Company",
        "description": "Company information and stats",
        "enabled_by_default": True,
        "can_disable": True,
        "endpoints": [
            {"path": "/company", "key": "company_detailed", "params": {"selections": "detailed"}, "cache_for": CACHE_DURATION_MEDIUM},
            {"path": "/company", "key": "company", "cache_for": CACHE_DURATION_MEDIUM},
        ],
    },
    CONF_ENABLE_STOCKS: {
        "name": "Stocks",
        "description": "Stock market data and holdings",
        "enabled_by_default": True,
        "can_disable": True,
        "endpoints": [
            {"path": "/torn", "key": "torn_stocks", "params": {"selections": "stocks"}, "cache_for": CACHE_DURATION_MEDIUM},
            {"path": "/user", "key": "user_stocks", "params": {"selections": "stocks"}, "cache_for": CACHE_DURATION_MEDIUM},
        ],
    },
    CONF_ENABLE_REFILLS: {
        "name": "Refills",
        "description": "Refill information",
        "enabled_by_default": True,
        "can_disable": True,
        "endpoints": [
            {"path": "/user", "key": "refills", "params": {"selections": "refills"}, "cache_for": CACHE_DURATION_LONG},
        ],
    },
    CONF_ENABLE_LOG: {
        "name": "Activity Log",
        "description": "Recent activity log",
        "enabled_by_default": True,
        "can_disable": True,
        "endpoints": [
            {"path": "/v2/user/log", "key": "log", "params": {"limit": "10"}, "cache_for": CACHE_DURATION_SHORT},
        ],
    },
}

# API Endpoints to fetch (built from enabled categories)
# This is now dynamically built based on enabled categories
API_ENDPOINTS = [
    {"path": "/v2/user/basic", "key": "profile", "cache_for": CACHE_DURATION_SHORT},
    {"path": "/v2/user/bars", "key": "bars", "cache_for": CACHE_DURATION_SHORT},
    {"path": "/v2/user/money", "key": "money", "cache_for": CACHE_DURATION_SHORT},
    {"path": "/v2/user/travel", "key": "travel", "cache_for": CACHE_DURATION_SHORT},
    {"path": "/v2/user/log", "key": "log", "params": {"limit": "10"}, "cache_for": CACHE_DURATION_SHORT},
    {"path": "/v2/user/cooldowns", "key": "cooldowns", "cache_for": CACHE_DURATION_MEDIUM},
    {"path": "/v2/user/personalstats", "key": "personalstats", "params": {"cat": "all"}, "cache_for": CACHE_DURATION_MEDIUM},
    {"path": "/company", "key": "company_detailed", "params": {"selections": "detailed"}, "cache_for": CACHE_DURATION_MEDIUM},
    {"path": "/company", "key": "company", "cache_for": CACHE_DURATION_MEDIUM},
    {"path": "/v2/user/skills", "key": "skills", "cache_for": CACHE_DURATION_LONG},
    {"path": "/user", "key": "refills", "params": {"selections": "refills"}, "cache_for": CACHE_DURATION_LONG},
    {"path": "/torn", "key": "torn_stocks", "params": {"selections": "stocks"}, "cache_for": CACHE_DURATION_MEDIUM},
    {"path": "/user", "key": "user_stocks", "params": {"selections": "stocks"}, "cache_for": CACHE_DURATION_MEDIUM},
]


def get_enabled_endpoints(options: dict) -> list[dict]:
    """Get list of enabled endpoints based on options."""
    enabled_endpoints = []

    for category_key, category_config in ENDPOINT_CATEGORIES.items():
        # Core endpoints are always enabled
        if category_key == "core":
            enabled_endpoints.extend(category_config["endpoints"])
            continue

        # Check if category is enabled in options (default to enabled_by_default)
        is_enabled = options.get(category_key, category_config["enabled_by_default"])

        if is_enabled:
            enabled_endpoints.extend(category_config["endpoints"])

    return enabled_endpoints
