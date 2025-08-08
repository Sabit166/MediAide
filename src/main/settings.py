import os
import dotenv
from langchain_openai import AzureChatOpenAI
from openai import AsyncOpenAI

dotenv.load_dotenv()


# Configure Azure

model_name = os.getenv("gpt_deployment_name")
azure_openai_api_key = os.environ["OPENAI_API_KEY"]
azure_openai_endpoint = os.environ["OPENAI_API_BASE"]
llm = AzureChatOpenAI(
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    azure_deployment=model_name,
    model_name=model_name,
    temperature=0.0
)

# Configure OpenAI

BASE_URL = os.getenv("BASE_URL") 
API_KEY = os.getenv("API_KEY") 
MODEL_NAME = os.getenv("MODEL_NAME") 

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set BASE_URL, API_KEY, and MODEL_NAME."
    )
    
client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)

#Configure SerpAPI

api_key = os.getenv("SERPAPI_KEY")
if api_key is None:
    raise ValueError("No SerpAPI key provided. Either pass it as argument or set SERPAPI_KEY environment variable.")
    
params = {
    "api_key": api_key,
    "engine": "google"  # You can change this to other engines like "bing", "yahoo" etc.
}