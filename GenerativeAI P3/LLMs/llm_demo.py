from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.9)

input_text = "What is the capital of France?"

response = llm(input_text)

print(response)