import os

import yaml  # type: ignore[import-untyped]


def load_agent_config():
    prompts_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_file = f"{prompts_dir}/prompts.yaml"
    try:
        with open(prompt_file, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"An error ocurred in load_agent_config: {e}")
