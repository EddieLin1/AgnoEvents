import os
from agno.agent import Agent
from agno.models.google import Gemini
#load environment variables from .env file
from dotenv import load_dotenv

from agnoevents.events import get_eventbrite_events


load_dotenv()

agent = Agent(
    model=Gemini(
        api_key = os.environ['GOOGLE_API_KEY'],

    )
)
agent = Agent(
    model=Gemini(
        api_key = os.environ['GOOGLE_API_KEY'],
    ),
    tools=[get_eventbrite_events],
    instructions="You help the user find events using the Eventbrite tools available to you.",
    markdown=True,
)



def main() -> None:
    agent.print_response("what events are happening in Calgary?", stream=True)
