from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model_name="gpt-4.1-mini",
      temperature=0.3,
      streaming = True
      )

def ask_llm(prompt:str)-> str:
    response= llm.invoke(prompt)
    return response.content
 
      