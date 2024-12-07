import oddish
import logging

logging.basicConfig(level=logging.DEBUG)
ahk = oddish.build_apple_health_kit("apple_health_export", "apple_health_kit.pkl")
print(ahk.quantities['HeartRate'])