from pydantic.dataclasses import dataclass
from pathlib import Path

import yaml
from omegaconf import OmegaConf

# D:\workspace\data-agent\app\conf\test_config.py
# print( Path(__file__) )

# D:\workspace\data-agent\conf\test_config.yaml
# yaml_path = Path(__file__).parent.parent.parent / 'conf/test_config.yaml'
# yaml_path = Path(__file__).parents[2] / 'conf/test_config.yaml'
# print(yaml_path)

# with open(yaml_path, 'r', encoding='utf-8') as f:
#     # yaml_data = f.read()
#     # print(yaml_data)
#
#     yaml_data = yaml.safe_load(f)
#     print(yaml_data) # {'name': '张三', 'age': 23, 'gender': '男'}
#     print(yaml_data['name']) # 张三

# 内置的yaml模块读取的yaml数据是字典，IDE没有提示，不友好


# 解决：使用 OmegaConf 插件

# 获取yaml文件的路径
yaml_path = Path(__file__).parents[2]/ 'conf/test_config.yaml'

# 读取yaml里面的数据
yaml_data = OmegaConf.load(yaml_path)
print(yaml_data) # {'name': '张三', 'age': 23, 'gender': '男'}
# print(yaml_data["name"]) # 张三

@dataclass
class Person:
    name: str
    age: int
    gender: str

person: Person = OmegaConf.to_object(yaml_data)
print(person)
print(type(person))
