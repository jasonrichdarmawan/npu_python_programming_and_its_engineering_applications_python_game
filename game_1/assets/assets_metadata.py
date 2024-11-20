from typing import TypedDict, Dict

# Define the structure of the asset metadata
class AssetMetadata(TypedDict):
    path: str
    width: int
    height: int

# Dictionary to store asset metadata
# TODO: adhere to Open/Closed principle
assets_metadata: Dict[str, AssetMetadata] = {
    "fighter_1": {
        "path": "images/fighter_1.png",
        "width": 50,
        "height": 50
    },
    "fighter_2": {
        "path": "images/fighter_2.png",
        "width": 50,
        "height": 50
    },
    "bullet": {
        "path": "images/bullet.png",
        "width": 10,
        "height": 20
    },
    "enemy": {
        "path": "images/enemy.png",
        "width": 50,
        "height": 50
    }
}