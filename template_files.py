import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

template_paths = {
    "search": os.path.join(BASE_DIR, "assets", f"search.jpg"),
    "food": os.path.join(BASE_DIR, "assets", f"food.jpg"),
    "wood": os.path.join(BASE_DIR, "assets", f"wood.jpg"),
    "stone": os.path.join(BASE_DIR, "assets", f"stone.jpg"),
    "gold": os.path.join(BASE_DIR, "assets", f"gold.jpg"),
    "search_loc": os.path.join(BASE_DIR, "assets", f"search_loc.jpg"),
    "gather": os.path.join(BASE_DIR, "assets", f"gather.jpg"),
    "new_troops": os.path.join(BASE_DIR, "assets", f"new_troops.jpg"),
    "march": os.path.join(BASE_DIR, "assets", f"march.jpg"),
    "verify": os.path.join(BASE_DIR, "assets", f"verify.jpg"),
    "verification_whitespace": os.path.join(
        BASE_DIR, "assets", f"verification_whitespace.jpg"
    ),
    "submit_verification": os.path.join(BASE_DIR, "assets", f"submit_verification.jpg"),
    "build": os.path.join(BASE_DIR, "assets", f"build.jpg"),
    "exit": os.path.join(BASE_DIR, "assets", f"exit_button.jpg"),
}
