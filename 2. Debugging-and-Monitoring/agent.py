from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import START, END
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langchain_tavily import TavilySearch
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['LANGSMITH_API_KEY'] = os.getenv('LANGSMITH_API_KEY')
os.environ['LANGSMITH_TRACING'] = 'true'
os.environ['LANGSMITH_PROJECT'] = 'TestProject1'

def make_tool_graph():
    from langchain.chat_models import init_chat_model
    llm = init_chat_model('groq:llama3-8b-8192')

    class State(TypedDict):
        messages:Annotated[list[BaseMessage], add_messages]

    @tool
    def add(a:float, b:float) -> float:
        """
        Add two numbers
        """
        return a+b

    search_tool = TavilySearch(max_results=2)

    tools = [search_tool, add]
    tool_node = ToolNode(tools)

    llm_with_tool = llm.bind_tools(tools)

    def call_llm_model(state:State):
        return {'messages': [llm_with_tool.invoke(state['messages'])]}
    
    ### Graph
    builder = StateGraph(State)

    ### Node definition
    builder.add_node('tool_calling_llm', call_llm_model)
    builder.add_node('tools', ToolNode(tools))

    ### Add Edges
    builder.add_edge(START, 'tool_calling_llm')
    builder.add_conditional_edges(
        'tool_calling_llm',
        tools_condition
    )
    builder.add_edge('tools', 'tool_calling_llm')

    ### Compile Graph
    graph = builder.compile()

    return graph

tool_agent = make_tool_graph()