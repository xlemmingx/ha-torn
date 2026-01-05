"""Constants for the Torn City integration."""

DOMAIN = "torn"

# API Configuration
API_BASE_URL = "https://api.torn.com"
API_TIMEOUT = 10
API_RATE_LIMIT = 100  # requests per minute

# Configuration
CONF_API_KEY = "api_key"
CONF_UPDATE_INTERVAL = "update_interval"

# Default values
DEFAULT_SCAN_INTERVAL = 60  # 1 minute

# API Endpoints to fetch
# Add new endpoints here to extend functionality
# Format: {"path": "/endpoint", "key": "data_key", "params": {"param": "value"}}
API_ENDPOINTS = [
    {"path": "/v2/user/basic", "key": "profile"},
    {"path": "/v2/user/personalstats", "key": "personalstats", "params": {"cat": "all"}},
    {"path": "/v2/user/bars", "key": "bars"},
    {"path": "/v2/user/cooldowns", "key": "cooldowns"},
    {"path": "/v2/user/money", "key": "money"},
    {"path": "/v2/user/skills", "key": "skills"},
    {"path": "/v2/user/travel", "key": "travel"},
    {"path": "/v2/user/log", "key": "log", "params": {"limit": "10"}},
    {"path": "/company", "key": "company_detailed", "params": {"selections": "detailed"}},
    {"path": "/company", "key": "company"},
    {"path": "/user", "key": "refills", "params": {"selections": "refills"}},
    # Add more endpoints as needed:
    # {"path": "/v2/user/organizedcrime", "key": "organizedcrime"},
    # {"path": "/v2/user/crimes", "key": "crimes"},
    # {"path": "/v2/user/attacks", "key": "attacks", "params": {"limit": "100"}},
]
