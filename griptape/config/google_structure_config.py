from attrs import define

from griptape.config import StructureConfig
from griptape.drivers import GoogleEmbeddingDriver, GooglePromptDriver, LocalVectorStoreDriver


@define
class GoogleStructureConfig(StructureConfig):
    prompt_driver = GooglePromptDriver(model="gemini-pro")
    embedding_driver = GoogleEmbeddingDriver(model="models/embedding-001")
    vector_store_driver = LocalVectorStoreDriver(embedding_driver=GoogleEmbeddingDriver(model="models/embedding-001"))
