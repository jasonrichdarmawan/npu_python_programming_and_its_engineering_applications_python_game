import pygame
import os
from .assets_metadata import assets_metadata, AssetMetadata
from base_dir import BASE_DIR

# Dictionary to store loaded images
loaded_images: dict[str, pygame.Surface] = {}

def get_image(name: str) -> pygame.Surface:
    if name in loaded_images:
        metadata = assets_metadata[name]
        return loaded_images[name]
    
    if name not in assets_metadata:
        raise ValueError(f"Asset metadata not found for {name}")
    
    metadata = assets_metadata[name]
    image_path = os.path.join(BASE_DIR, "assets", metadata["path"])
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (metadata["width"], metadata["height"]))
    loaded_images[name] = image
    return image

def get_image_metadata(name: str) -> AssetMetadata:
    metadata = assets_metadata[name]
    return metadata