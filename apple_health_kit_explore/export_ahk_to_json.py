import logging
import oddish

ahk = oddish.load_apple_health_kit("apple_health_kit.pkl")
ahk.export_to_json("../web/oddish/src/ahk/ahk.json")



