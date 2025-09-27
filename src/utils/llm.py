"""All utils for invoking the LLM."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """Write a short wikipedia style article on {term}. 
Please don't add any additional information or commentary. 
Do not add references or "See also". Also, do not add a title or heading.
Just the article content in markdown format."""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="gpt-oss:20b")
chain = prompt | model


def generate_article(term: str) -> str:
    """Generate a short article on the given term."""
    return chain.invoke({"term": term})
