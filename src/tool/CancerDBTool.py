from agents import function_tool
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from src.main import settings
from agents import function_tool

@function_tool
def cancer_db_tool():
    """
    Tool for interacting with the cancer database.
    """

    engine = create_engine("sqlite:///src/database/cancer.db")
    db = SQLDatabase(engine=engine)
    llm = settings.llm  # Assuming get_azure_llm is defined in the same context
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    return agent_executor


def main():
    """
    Test function for the cancer database tool.
    """
    print("Testing Cancer Database Tool...")
    
    try:
        # Test database connection
        engine = create_engine("sqlite:///src/database/cancer.db")
        db = SQLDatabase(engine=engine)
        
        print("✅ Database connection successful")
        print(f"Available tables: {db.get_usable_table_names()}")
        
        # Test a simple query
        result = db.run("SELECT COUNT(*) as total_records FROM cancer LIMIT 1;")
        print(f"Total records in cancer table: {result}")
        
        # Test the tool (if settings.llm is available)
        try:
            agent = cancer_db_tool()
            print("✅ Cancer DB tool created successfully")
            
            # Test with a simple query
            test_query = "How many records are in the cancer dataset?"
            response = agent.invoke({"input": test_query})
            print(f"Test query: {test_query}")
            print(f"Response: {response}")
            
        except Exception as e:
            print(f"⚠️ Agent creation failed (likely missing LLM settings): {e}")
            
    except Exception as e:
        print(f"❌ Error testing cancer database tool: {e}")


if __name__ == "__main__":
    main()

