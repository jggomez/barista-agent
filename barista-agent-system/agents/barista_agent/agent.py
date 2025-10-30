import os

import google.cloud.logging
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

from .prompts.load_prompts import load_agent_config
from .tools.availability_check_tools import check_availability_coffee
from .tools.common_tools import get_today_date
from .tools.image_coffee_tools import create_image_coffee
from .tools.menu_tools import get_menu_items
from .tools.promotions_tools import get_current_promotion

client = google.cloud.logging.Client()
client.setup_logging()

load_dotenv()

LLM_AGENT = os.getenv("LLM_AGENT")

if not LLM_AGENT:
    raise ValueError("The LLM_AGENT environment variable is not set.")

agent_config = load_agent_config()

print(agent_config)


root_agent = LlmAgent(
    name="barista_agent",
    model=LLM_AGENT,
    description=agent_config["description"],
    instruction=agent_config["instruction"],
    tools=[
        get_menu_items,
        check_availability_coffee,
        get_today_date,
        get_current_promotion,
        create_image_coffee,
    ],
)
