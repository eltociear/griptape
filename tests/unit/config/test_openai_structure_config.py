from pytest import fixture
from griptape.config import OpenAiStructureConfig


class TestOpenAiStructureConfig:
    @fixture(autouse=True)
    def mock_openai(self, mocker):
        return mocker.patch("openai.OpenAI")

    @fixture
    def config(self):
        return OpenAiStructureConfig()

    def test_to_dict(self, config):
        assert config.to_dict() == {
            "type": "OpenAiStructureConfig",
            "global_drivers": {
                "type": "StructureGlobalDriversConfig",
                "prompt_driver": {
                    "type": "OpenAiChatPromptDriver",
                    "base_url": None,
                    "model": "gpt-4",
                    "organization": None,
                    "response_format": None,
                    "seed": None,
                    "temperature": 0.1,
                    "max_tokens": None,
                    "stream": False,
                    "user": "",
                },
                "conversation_memory_driver": None,
                "embedding_driver": {
                    "base_url": None,
                    "model": "text-embedding-3-small",
                    "organization": None,
                    "type": "OpenAiEmbeddingDriver",
                },
                "image_generation_driver": {
                    "api_version": None,
                    "base_url": None,
                    "image_size": "512x512",
                    "model": "dall-e-2",
                    "organization": None,
                    "quality": "standard",
                    "response_format": "b64_json",
                    "style": None,
                    "type": "OpenAiImageGenerationDriver",
                },
                "image_query_driver": {
                    "api_version": None,
                    "base_url": None,
                    "image_quality": "auto",
                    "max_tokens": 256,
                    "model": "gpt-4-vision-preview",
                    "organization": None,
                    "type": "OpenAiVisionImageQueryDriver",
                },
                "vector_store_driver": {
                    "embedding_driver": {
                        "base_url": None,
                        "model": "text-embedding-3-small",
                        "organization": None,
                        "type": "OpenAiEmbeddingDriver",
                    },
                    "type": "LocalVectorStoreDriver",
                },
            },
            "task_memory": {
                "type": "StructureTaskMemoryConfig",
                "query_engine": {
                    "type": "StructureTaskMemoryQueryEngineConfig",
                    "prompt_driver": {
                        "base_url": None,
                        "type": "OpenAiChatPromptDriver",
                        "model": "gpt-4",
                        "organization": None,
                        "response_format": None,
                        "seed": None,
                        "temperature": 0.1,
                        "max_tokens": None,
                        "stream": False,
                        "user": "",
                    },
                    "vector_store_driver": {
                        "type": "LocalVectorStoreDriver",
                        "embedding_driver": {
                            "type": "OpenAiEmbeddingDriver",
                            "base_url": None,
                            "organization": None,
                            "model": "text-embedding-3-small",
                        },
                    },
                },
                "extraction_engine": {
                    "type": "StructureTaskMemoryExtractionEngineConfig",
                    "csv": {
                        "type": "StructureTaskMemoryExtractionEngineCsvConfig",
                        "prompt_driver": {
                            "type": "OpenAiChatPromptDriver",
                            "base_url": None,
                            "model": "gpt-4",
                            "organization": None,
                            "response_format": None,
                            "seed": None,
                            "temperature": 0.1,
                            "max_tokens": None,
                            "stream": False,
                            "user": "",
                        },
                    },
                    "json": {
                        "type": "StructureTaskMemoryExtractionEngineJsonConfig",
                        "prompt_driver": {
                            "type": "OpenAiChatPromptDriver",
                            "base_url": None,
                            "model": "gpt-4",
                            "organization": None,
                            "response_format": None,
                            "seed": None,
                            "temperature": 0.1,
                            "max_tokens": None,
                            "stream": False,
                            "user": "",
                        },
                    },
                },
                "summary_engine": {
                    "type": "StructureTaskMemorySummaryEngineConfig",
                    "prompt_driver": {
                        "type": "OpenAiChatPromptDriver",
                        "base_url": None,
                        "model": "gpt-4",
                        "organization": None,
                        "response_format": None,
                        "seed": None,
                        "temperature": 0.1,
                        "max_tokens": None,
                        "stream": False,
                        "user": "",
                    },
                },
            },
        }

    def test_from_dict(self, config):
        assert OpenAiStructureConfig.from_dict(config.to_dict()).to_dict() == config.to_dict()
