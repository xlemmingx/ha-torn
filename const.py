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

# Default values
DEFAULT_SCAN_INTERVAL = 1

# Cache durations for different endpoint types (in seconds)
CACHE_DURATION_SHORT = 5
CACHE_DURATION_MEDIUM = 60
CACHE_DURATION_LONG = 600

# API Endpoints to fetch
# Add new endpoints here to extend functionality
# Format: {"path": "/endpoint", "key": "data_key", "params": {"param": "value"}, "cache_for": duration}
# cache_for: Optional cache duration in seconds. If not set, fetches on every update cycle.
#            Use CACHE_DURATION_SHORT, CACHE_DURATION_MEDIUM, or CACHE_DURATION_LONG
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
