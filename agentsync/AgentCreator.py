from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from typing import List, Optional, Any

class AgentCreator:
    """
    A utility class for creating customizable LangChain agents.
    
    This class provides a flexible interface for creating agents with 
    customizable models, tools, prompts, and other parameters.
    """
    
    def __init__(self):
        """Initialize the AgentCreator."""
        pass
        
    def create_agent(
        self,
        model: Optional[Any] = None,
        tools: List[BaseTool] = None,
        name: str = "default_agent",
        prompt: str = None,
        **kwargs
    ):
        """
        Create a LangChain agent with the specified configuration.
        
        Args:
            model: A pre-configured LLM instance. If None, one will be created.
            tools: A list of tools the agent can use.
            name: The name of the agent.
            prompt: The system prompt for the agent.
            **kwargs: Additional arguments to pass to the agent executor.
            
        Returns:
            An AgentExecutor instance.
        """
        # Initialize default values
        if tools is None:
            tools = []

        # Set default system prompt if not provided
        if prompt is None:
            prompt = f"""You are {name}, an AI assistant designed to help with various tasks.
            You have access to the following tools: {[tool.name for tool in tools]}.
            Use these tools when appropriate to complete user requests."""
        
        # Create the agent
        agent = create_react_agent(
            model=model,
            tools=tools,
            name=name,
            prompt=prompt
        )
        
        # Create and return the agent executor
        return agent