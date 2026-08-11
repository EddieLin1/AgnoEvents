import os
# imports for agent and using gemini model
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.sql import SQLTools
from sqlalchemy import create_engine

# for short term storage of events in sqlite database
from agno.db.sqlite import SqliteDb

# load environment variables from .env file
from dotenv import load_dotenv

from agnoevents.events import get_eventbrite_events_calgary, get_ticketmaster_events_calgary
from agnoevents.db import update_calgary_events


load_dotenv()

storage = SqliteDb(session_table="agent_sessions", db_file="tmp/agent_sessions.db")

engine = create_engine("sqlite:///agnoevents.db")

agent = Agent(
    model=Gemini(
        id = os.environ['DEFAULT_MODEL'],
        api_key = os.environ['GOOGLE_API_KEY'],
    ),
    db=storage,
    tools=[get_eventbrite_events_calgary, get_ticketmaster_events_calgary, SQLTools(db_engine = engine), update_calgary_events],
    instructions="You help the user find events in calgary using the Eventbrite and Ticketmaster and sql tools available to you.",
    markdown=True,
    add_history_to_context=True,
    add_datetime_to_context=True,
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

