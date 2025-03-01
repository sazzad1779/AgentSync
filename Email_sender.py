from typing import Annotated
from dotenv import load_dotenv
from langchain_core.tools import tool
from agentsync.AgentCreator import AgentCreator
from agentsync.SupervisorCreator import SupervisorCreator
from agentsync.tools.gmail_tool import GmailTool
from langchain_openai import ChatOpenAI
from prompt import EMAIL_CREATOR_PROMPT, SUPERVISOR_PROMPT


load_dotenv()
## load model
model = ChatOpenAI(model="gpt-3.5-turbo")

# tool for sending summary
@tool
def send_email(
    recipient: Annotated[str, "this is the recipient mail address."],
    subject: Annotated[str, "this is the subject of email"],
    content: Annotated[str, "content of the email which generated from llm"]
) -> str:
    """Sends the mail to specific recipient.content will be the  supervisor's agent generated mail.
    after execution output should be the email content and the message is it success or fail.
    """
    # Assuming AgentB can send emails
    gmail = GmailTool()

    # Define email details
    if gmail.send_email(recipient, subject, content):
        return f"{content}\n\n📩 Final email sent to {recipient} successfully."
    else:
        return f"❌ Failed to send final email to {recipient}."

def main():
    # Initialize creators
    agent_creator = AgentCreator()
    supervisor_creator = SupervisorCreator()
    
    # Create validation specialized agent using prompt key from prompts.py
    agent_a = agent_creator.create_agent(
        model=model,
        tools=[send_email],
        name="Email_process",
        prompt=EMAIL_CREATOR_PROMPT
    )
    
    # Create supervisor workflow using prompt key from prompts.py
    supervisor = supervisor_creator.create_supervisor(
        agents=[agent_a],
        model=model,
        tools=[],
        prompt=SUPERVISOR_PROMPT,
        output_mode="last_message"
    )
    
    # Compile the workflow
    app = supervisor.compile()
    
    # Example user message to send an email

    instruction= """You are responsible for automating email generation and sending the generated email to mdsazzad1779@gmail.com. Execute the following steps in the correct order, utilizing the appropriate agents and tools:"""
    user_message = {
        "messages": [
            {
                "role": "user",
                "content": instruction
            }
        ]
    }
    # Invoke the app with the user message
    print("Running Email generation Automation...")
    result = app.invoke(user_message)

    # Print the summary
    print("\nEmail generation Execution Completed. Summary:")
    # print(result)
    for m in result["messages"]:
        m.pretty_print()

if __name__ == "__main__":
    main()