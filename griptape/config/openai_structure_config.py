from attrs import define

from griptape.config import StructureConfig
from griptape.drivers import (
    LocalVectorStoreDriver,
    OpenAiChatPromptDriver,
    OpenAiEmbeddingDriver,
    OpenAiImageGenerationDriver,
    OpenAiVisionImageQueryDriver,
)


@define
class OpenAiStructureConfig(StructureConfig):
    prompt_driver = OpenAiChatPromptDriver(model="gpt-4")
    image_generation_driver = OpenAiImageGenerationDriver(model="dall-e-2", image_size="512x512")
    image_query_driver = OpenAiVisionImageQueryDriver(model="gpt-4-vision-preview")
    embedding_driver = OpenAiEmbeddingDriver(model="text-embedding-3-small")
    vector_store_driver = LocalVectorStoreDriver(embedding_driver=OpenAiEmbeddingDriver(model="text-embedding-3-small"))
