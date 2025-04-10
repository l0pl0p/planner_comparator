import os
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

load_dotenv()

provider = os.getenv("PROVIDER").lower()

if provider == "azure":
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_API_VERSION"),
    )
else:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
