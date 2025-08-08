from agents import function_tool
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from src.config.llm_config import get_azure_llm
from agents import function_tool

@function_tool
def cancer_db_tool():
    """
    Tool for interacting with the cancer database.
    """

    engine = create_engine("sqlite:///src/database/cancer.db")
    db = SQLDatabase(engine=engine)
    llm = get_azure_llm()  # Assuming get_azure_llm is defined in the same context
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    return agent_executor

