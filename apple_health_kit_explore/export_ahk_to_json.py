import logging
from datetime import datetime

import oddish

export_config = {
    'export_file': "../web/oddish/src/ahk/ahk.json",
    'export_start_date': datetime(2024, 1, 1),
}

ahk = oddish.AppleHealthKit.load_apple_health_kit('apple_health_kit.pkl')
ahk.export_to_json(export_config)
