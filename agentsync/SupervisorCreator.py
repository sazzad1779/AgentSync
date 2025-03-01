from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langchain_core.tools import BaseTool
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SupervisorCreator:
    """
    A utility class for creating customizable supervisor agents that coordinate multiple agents.
    
    This class provides a flexible interface for creating supervisor workflows with 
    customizable models, agents, tools, prompts, and other parameters.
    """
    
    def __init__(self):
        """Initialize the SupervisorCreator."""
        pass
        
    def create_supervisor(
        self,
        agents: List[Any],
        model: Optional[Any] = None,
        tools: List[BaseTool] = None,
        prompt: str = None,
        output_mode: str = "last_message",

    ):
        """
        Create a LangGraph supervisor with the specified configuration.
        
        Args:
            agents: List of agent executors to be supervised.
            model: A pre-configured LLM instance. If None, one will be created.
            tools: A list of supervisor-level tools.
            prompt: The system prompt for the supervisor.
            output_mode: Output mode for the supervisor ("last_message" or "full_trace").            
        Returns:
            A compiled supervisor workflow.
        """
        # Initialize default values
        if tools is None:
            tools = []
        # Get agent names for default prompt
        agent_names = [getattr(agent, "name", f"Agent_{i}") for i, agent in enumerate(agents)]
        # print("agent_names: ",agent_names)
        # Set default system prompt if not provided
        if prompt is None:
            prompt = f"""You are a supervisor responsible for coordinating the following agents: {agent_names}.
            
            Each agent has specialized capabilities:
            {' '.join([f"- {name}" for name in agent_names])}
            
            Your task is to:
            1. Understand the user's request
            2. Delegate tasks to the appropriate specialized agents
            3. Integrate their results
            4. Provide a coherent response to the user
            
            Use the available tools when appropriate and ensure the workflow proceeds efficiently."""
        
        try:
            # Create the supervisor
            supervisor = create_supervisor(
                agents=agents,
                model=model,
                tools=tools,
                prompt=prompt,
                output_mode=output_mode
            )
            
            # Compile the workflow
            return supervisor
            
        except Exception as e:
            logger.error(f"Error creating supervisor: {str(e)}")
            raise