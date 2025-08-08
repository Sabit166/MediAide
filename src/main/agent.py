from agents import Agent, OpenAIChatCompletionsModel
from src.tool.CancerDBTool import cancer_db_tool
from src.tool.DiabetesDBTool import diabetes_db_tool
from src.tool.HeartDiseaseDBTool import heart_disease_db_tool
from src.tool.MedicalWebSearchTool import web_search as web_search_tool
import settings

agent = Agent(
    name = 'MedicalAgent',
    description = 'An agent that can answer questions about cancer and diabetes using their respective databases and can conduct web searches.',
    instructions="""
    You are a medical agent capable for conducting web searches and querying databases related to cancer, diabetes and heart attack.
    
    You are supplied with three database tools:
    1. DiabetesDBTool: For querying the diabetes database.
    2. CancerDBTool: For querying the cancer database.
    3. HeartDiseaseDBTool: For querying the heart disease database.
    You also have a web search tool to find information online.
    
    Your tasks include:
    1. Use the web search tool to find information about cancer and diabetes.
    2. Query the respective databases for more detailed information.
    3. Provide concise and accurate answers to user queries.
    
    Your main goal is to assist users by providing accurate and relevant information about cancer, diabetes, and heart disease.
    Always give precise response based on the data available in the databases and the results from web searches.
    If you do not have enough information, you can conduct a web search to find the necessary information.
    Be sure to format your responses clearly and concisely.
    """,
    model=OpenAIChatCompletionsModel(model=settings.MODEL_NAME, openai_client=settings.openai_client),
    tools=[
        diabetes_db_tool,
        cancer_db_tool,
        heart_disease_db_tool,
        web_search_tool
    ]
)