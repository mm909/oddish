import oddish
import logging
import json
import pandas as pd
from datetime import datetime


import oddish.apple_health_kit

logging.basicConfig(level=logging.DEBUG)

ahk_config = {
    'apple_health_kit_data': 'apple_health_export',
    'output_folder': 'AppleHealthKit',
    'save_exports': True,
}

ahk = oddish.AppleHealthKit(ahk_config)
# ahk = oddish.AppleHealthKit.load_apple_health_kit('apple_health_kit.pkl')
ahk.build()
ahk.save_to_pickle('apple_health_kit.pkl')

export_config = {
    'export_file': 'apple_health_kit.json',
    'export_start_date': datetime(2024, 1, 1),
}
ahk.export_to_json(export_config)

