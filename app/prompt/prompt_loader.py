from pathlib import Path


# 加载指定提示词模板的内容
def load_prompt(name: str):
    # 获取文件路径
    prompt_path = Path(__file__).parents[2] / 'prompts'/f'{name}.prompt'
    # 读取文件内容
    return prompt_path.read_text(encoding='utf-8')


if __name__ == '__main__':
    print(load_prompt('correct_sql'))
