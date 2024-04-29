from attrs import define

from griptape.config import StructureConfig
from griptape.drivers import (
    AmazonBedrockImageGenerationDriver,
    AmazonBedrockImageQueryDriver,
    AmazonBedrockPromptDriver,
    AmazonBedrockTitanEmbeddingDriver,
    BedrockClaudePromptModelDriver,
    BedrockClaudeImageQueryModelDriver,
    BedrockTitanImageGenerationModelDriver,
    LocalVectorStoreDriver,
)


@define()
class AmazonBedrockStructureConfig(StructureConfig):
    prompt_driver = AmazonBedrockPromptDriver(
        model="anthropic.claude-3-sonnet-20240229-v1:0",
        stream=False,
        prompt_model_driver=BedrockClaudePromptModelDriver(),
    )
    image_generation_driver = AmazonBedrockImageGenerationDriver(
        model="amazon.titan-image-generator-v1", image_generation_model_driver=BedrockTitanImageGenerationModelDriver()
    )
    image_query_driver = AmazonBedrockImageQueryDriver(
        model="anthropic.claude-3-sonnet-20240229-v1:0", image_query_model_driver=BedrockClaudeImageQueryModelDriver()
    )
    embedding_driver = AmazonBedrockTitanEmbeddingDriver(model="amazon.titan-embed-text-v1")
    vector_store_driver = LocalVectorStoreDriver(
        embedding_driver=AmazonBedrockTitanEmbeddingDriver(model="amazon.titan-embed-text-v1")
    )
