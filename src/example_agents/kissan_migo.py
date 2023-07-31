#from langchain.tools import PythonREPLTool, ShellTool, GoogleSearchResults
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory


class KissanMigo:
    """Class enabling to define the KissanMigo ai agent.
    """
    def __init__(self, tools, llm, agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, **kwargs):
        self.tools = tools
        self.type = agent_type
        self._define_agent(llm, **kwargs)

    def _define_agent(self, llm, verbose=True, **kwargs):
        self.agent = initialize_agent(tools=self.tools, llm=llm, agent=self.type, verbose=verbose, **kwargs)