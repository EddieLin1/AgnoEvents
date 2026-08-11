import os
from agno.agent import Agent
from agno.models.google import Gemini
#load environment variables from .env file
from dotenv import load_dotenv

from agnoevents.events import get_eventbrite_events_calgary, get_ticketmaster_events_calgary


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
    tools=[get_eventbrite_events_calgary, get_ticketmaster_events_calgary],
    instructions="You help the user find events using the Eventbrite and Ticketmaster tools available to you.",
    markdown=True,
)



def main() -> None:

    print("Agent ready. Type your message (or 'exit' to quit).\n")
 
    while True:
        user_input = input("You: ").strip()
    
        if user_input.lower() in ("exit", "quit"):
            break
    
        if not user_input:
            continue
    
        agent.print_response(user_input, stream=True)

