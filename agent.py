from strands import Agent
from strands.models import BedrockModel
from strands_tools import http_request

agent = Agent(
    model=BedrockModel(
        model_id="us.amazon.nova-lite-v1:0",
        temperature=0.3
    ),
    tools=[http_request],
    system_prompt = "You are a helpful assistant that can answer questions and perform tasks using the provided tools. Use http_request for real-time data. ONLY use free APIs that require NO API KEY. DO NOT use OpenWeatherMap or any API that needs authentication. If data cannot be fetched without an API key, clearly say so."
)
# Use the agent
user_input = input("AMA:")
agent(user_input)