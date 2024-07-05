""" Initialise the chroma db
    store image tensor pixel values as embedding
    unique_id generated from image tensor and
    generated basic caption.

    Returns:
"""

import uuid
import hashlib
import torch
import chromadb
from chromadb.config import Settings
from utils.logger import log


def initialize_chroma_client():
    """
    Initialise the chroma client.
    This should be initialized at the start of the application

    Returns:
    chromadb.Client: The initialized chroma client
    """
    return chromadb.PersistentClient(
        path="sqlite_chroma_db", settings=Settings(anonymized_telemetry=False)
    )


def get_chroma_collection(chroma_client, collection_name):
    """
    After the initialization of the Chromadb, either we need to
    create a collection or get the collection if that exists.

    Args:
    chroma_client (chromadb): The initiated chroma client.
    collection_name (str): Name of the collection

    Returns:
    chroma collection: Returns a chroma
    collection type object.
    """
    try:
        collection = chroma_client.create_collection(collection_name)
    except:
        collection = chroma_client.get_collection(collection_name)
    return collection


def add_image_to_chroma(collection, unique_id, input_tensor, caption):
    """
    Add an image tensor pixel values as embedding to the chromadb

    Args:
    collection (chromadb.collection): The initiated chroma client's collection.
    unique_id (str): unique_id of the image tensor's pixel values
    generated using the image tensor
    input_tensor (torch.tensor): The image tensor pixel values
    caption (str): BLIP2 model generated basic caption.

    Returns:
    None: Adds the image tensor pixel values as embedding to the chromadb
    """
    existing_ids = collection.get(ids=[unique_id])
    if existing_ids["ids"] == [unique_id]:
        log.warn(f"Entry with unique_id {unique_id} already exists. Skipping addition.")
        return

    input_tensor_flatten = input_tensor.flatten().tolist()
    input_tesnor_shape = str(input_tensor.shape)
    collection.add(
        embeddings=input_tensor_flatten,
        ids=[unique_id],
        metadatas=[{"caption": caption, "image_tensor_shape": input_tesnor_shape}],
    )
    log.info(f"Added entry with unique_id {unique_id}.")


def get_unique_image_id(input_tensor):
    """
    Creates an unique id from the image tensor's pixel value

    Args:
    input_tensor (torch.tensor): The image tensor pixel values

    Returns:
    unique_id (str): generated unique id string from the image tensor.
    """
    input_tensor = input_tensor.cpu()
    input_bytes = input_tensor.numpy().tobytes()
    hash_object = hashlib.sha256(input_bytes)
    unique_id = str(uuid.UUID(hash_object.hexdigest()[:32]))
    return unique_id


def get_reconstructed_flattened_input_tensor(input_tensor_flatten, image_tensor_shape):
    """
    Reconstruct the image tensor pixel values from
    the flattened list of pixel values.

    Args:
    input_tensor_flatten (list): Flattened
    image tensor pixel values
    image_tensor_shape (str): Stringified image tensor original shape

    Returns:
    tensor (torch.tensor): Reconstructed original image tensor.
    """
    shape_tuple = tuple(map(int, image_tensor_shape.strip("()").split(",")))
    tensor = torch.tensor(input_tensor_flatten).view(shape_tuple)
    return tensor
