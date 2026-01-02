"""Constants for the Torn City integration."""

DOMAIN = "torn"

# API Configuration
API_BASE_URL = "https://api.torn.com/v2"
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
    {"path": "/user/basic", "key": "profile"},
    {"path": "/user/personalstats", "key": "personalstats", "params": {"cat": "all"}},
    # Add more endpoints as needed:
    # {"path": "/user/crimes", "key": "crimes"},
    # {"path": "/user/attacks", "key": "attacks", "params": {"limit": "100"}},
]
