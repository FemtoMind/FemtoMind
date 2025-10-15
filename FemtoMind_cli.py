import sys

from smolagents import CodeAgent, OpenAIServerModel
import matplotlib
matplotlib.use("Agg")  # non-interactive backend


#! Prompt user for API key
if len(sys.argv)==1:
    print("API key is required. Exiting.")
    exit(1)

api_key = sys.argv[1]


# Initialize the LLM / agent
model = OpenAIServerModel(
    model_id="gemini-2.0-flash",  # replace with your model
    api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key, 
)

agent = CodeAgent(tools=[], model=model)

# Chat history
history = []

print("=== FemtoMind CLI ===")
print("Type 'exit' or 'quit' to leave.")

while True:
    prompt = input("You: ")
    if prompt.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    # Run agent
    response = agent.run(prompt)

    # Save to history
    history.append({"user": prompt, "agent": response})

    # Display agent response
    print(f"Agent: {response}")






# Later in the loop:
response = agent.run(prompt)

# If agent returns a figure object
if hasattr(response, "savefig"):
    filename = f"plot_{len(history)}.png"
    response.savefig(filename)
    print(f"Agent generated a plot saved as {filename}")
else:
    print(f"Agent: {response}")


