from typing import TypedDict, Dict

# Define the structure of the asset metadata
class AssetMetadata(TypedDict):
    path: str
    width: int
    height: int
    direction: str

# Dictionary to store asset metadata
# TODO: adhere to Open/Closed principle
assets_metadata: Dict[str, AssetMetadata] = {
    "fighter_1": {
        "path": "images/fighter_1.png",
        "width": 50,
        "height": 50,
        "direction": "up"
    },
    "fighter_2": {
        "path": "images/fighter_2.png",
        "width": 50,
        "height": 50,
        "direction": "up"
    },
    "bullet": {
        "path": "images/bullet.png",
        "width": 10,
        "height": 20,
        "direction": "up"
    },
    "enemy": {
        "path": "images/enemy.png",
        "width": 50,
        "height": 50,
        "direction": "down"
    }
}