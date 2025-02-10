import pygame
import os
from .assets_metadata import ASSETS_METADATA, AssetMetadata
from base_dir import BASE_DIR

# Dictionary to store loaded images
loaded_images: dict[str, pygame.Surface] = {}

def get_image(name: str) -> pygame.Surface:
    if name in loaded_images:
        metadata = ASSETS_METADATA[name]
        return loaded_images[name]
    
    if name not in ASSETS_METADATA:
        raise ValueError(f"Asset metadata not found for {name}")
    
    metadata = ASSETS_METADATA[name]
    image_path = os.path.join(BASE_DIR, "assets", metadata["path"])
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (metadata["width"], metadata["height"]))
    loaded_images[name] = image
    return image

def get_image_metadata(name: str) -> AssetMetadata:
    metadata = ASSETS_METADATA[name]
    return metadata