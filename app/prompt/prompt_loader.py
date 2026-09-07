"""提示词加载器：根据名称读取 prompts 目录下的 .prompt 文件。"""

from pathlib import Path

# prompts 目录：项目根目录下的 prompts 文件夹
PROMPTS_DIR = Path(__file__).resolve().parents[2] / 'prompts'


class PromptLoader:
    """根据方法名加载 prompts 目录下对应的提示词文件。"""

    def load(self, name: str) -> str:
        """根据方法名读取对应提示词文件内容。

        Args:
            name: 提示词名称（对应 prompts 目录下的文件名，不含 .prompt 后缀）。
                  例如 name='generate_sql' 会读取 prompts/generate_sql.prompt。

        Returns:
            提示词文件内容字符串。

        Raises:
            FileNotFoundError: 当对应的提示词文件不存在时。
        """
        prompt_file = PROMPTS_DIR / f'{name}.prompt'
        if not prompt_file.is_file():
            raise FileNotFoundError(f'提示词文件不存在: {prompt_file}')
        return prompt_file.read_text(encoding='utf-8')


# 全局提示词加载器实例，供各节点直接引用
prompt_loader = PromptLoader()
if __name__ == '__main__':
    print(prompt_loader.load("correct_sql"))