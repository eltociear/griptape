from attrs import define

from griptape.config import StructureConfig
from griptape.drivers import (
    AnthropicImageQueryDriver,
    AnthropicPromptDriver,
    LocalVectorStoreDriver,
    VoyageAiEmbeddingDriver,
)


@define
class AnthropicStructureConfig(StructureConfig):
    prompt_driver = AnthropicPromptDriver(model="claude-3-opus-20240229")
    embedding_driver = VoyageAiEmbeddingDriver(model="voyage-large-2")
    vector_store_driver = LocalVectorStoreDriver(embedding_driver=VoyageAiEmbeddingDriver(model="voyage-large-2"))
    image_query_driver = AnthropicImageQueryDriver(model="claude-3-opus-20240229")
