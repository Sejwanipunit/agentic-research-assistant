from src.agent.runner import AgentRunner


def main():
    agent = AgentRunner()
    print("Agentic Research Assistant")
    print("Commands: 'quit' to exit, 'clear' to reset memory\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "clear":
            agent.clear_memory()
            continue

        print("\nAssistant: ", end="", flush=True)

        # Stream the response
        for chunk in agent.stream(user_input):
            print(chunk, end="", flush=True)

        print("\n")


if __name__ == "__main__":
    main()