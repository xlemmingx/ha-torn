"""Constants for the Torn City integration."""

DOMAIN = "torn"

# API Configuration
API_BASE_URL = "https://api.torn.com/v2"
API_TIMEOUT = 10
API_RATE_LIMIT = 100  # requests per minute

# Configuration
CONF_API_KEY = "api_key"

# Default values
DEFAULT_SCAN_INTERVAL = 300  # 5 minutes

# API Endpoints to fetch
# Add new endpoints here to extend functionality
API_ENDPOINTS = [
    {"path": "/user/basic", "key": "profile"},
    {"path": "/user/personalstats", "key": "personalstats"},
    # Add more endpoints as needed:
    # {"path": "/user/crimes", "key": "crimes"},
    # {"path": "/user/attacks", "key": "attacks"},
]
