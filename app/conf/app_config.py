"""
解析app_config.yaml文件, 生成指定类型的对象
"""
from pathlib import Path
from omegaconf import OmegaConf
from dataclasses import dataclass

# ==================== 日志配置模型 ====================
@dataclass
class File:
    enable: bool
    level: str
    path: str
    rotation: str
    retention: str


@dataclass
class Console:
    enable: bool
    level: str


@dataclass
class LoggingConfig:
    file: File
    console: Console


# ==================== database配置模型 ====================

@dataclass
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

# ==================== Qdrant 配置模型 ====================

@dataclass
class QdrantConfig:
    host: str
    port: int
    embedding_size: int


# ==================== Embedding 配置模型 ====================

@dataclass
class EmbeddingConfig:
    host: str
    port: int
    model: str


# ==================== ES 配置模型 ====================

@dataclass
class ESConfig:
    host: str
    port: int
    index_name: str


# ==================== LLM 配置模型 ====================

@dataclass
class LLMConfig:
    model_name: str
    api_key: str


# ==================== app总配置模型 ====================

@dataclass
class AppConfig:
    logging: LoggingConfig
    db_meta: DBConfig
    db_dw: DBConfig
    qdrant: QdrantConfig
    embedding: EmbeddingConfig
    es: ESConfig
    llm: LLMConfig


# 获取yaml文件的路径
_yaml_path = Path(__file__).parents[2] / 'conf/app_config.yaml'

# 根据文件路径加载yaml数据 -> OmegaConf对象
_yaml_data = OmegaConf.load(_yaml_path)

# 将OmegaConf对象转成AppConfig对象
app_config: AppConfig = OmegaConf.to_object(OmegaConf.merge(AppConfig, _yaml_data))

if __name__ == '__main__':
    print(app_config)
    print(type(app_config))
    print(app_config.logging.file.level) # INFO