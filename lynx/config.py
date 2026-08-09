from dotenv import load_dotenv
import os
load_dotenv()

def get_api_key():
    return { "ANTHROPIC_API_KEY" : os.getenv("ANTHROPIC_API_KEY"), "ASSEMBLY_API_KEY" : os.getenv("ASSEMBLY_API_KEY")}