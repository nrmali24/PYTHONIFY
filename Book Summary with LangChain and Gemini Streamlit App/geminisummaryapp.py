import streamlit as st
import os
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import google.generativeai as genai

import sys
sys.path.append("/config")



from config import key


# Set the Gemini API key
genai.configure(api_key=key)
google_llm = GoogleGenerativeAI(model="gemini-pro", api_key=key)

# Streamlit app title
st.title('Book Summary')

input_text = st.text_input("Search the book you want")

# Prompt Template for Book Summary
first_input_prompt = PromptTemplate(
                                    input_variables=['name'],
                                    template="Provide me a summary of the book {name}"
                                    )

# LLM Chain for summarizing the book
chain1 = LLMChain(llm=google_llm, prompt=first_input_prompt, verbose=True, output_key='summaryofbook')

# Prompt Template for book publish date
second_input_prompt = PromptTemplate(
                                    input_variables=['summaryofbook'],
                                    template="When was the book '{summaryofbook}' published?"
                                    )

# LLM Chain for finding the book's publish date
chain2 = LLMChain(llm=google_llm, prompt=second_input_prompt, verbose=True, output_key='bookpublishdate')

# Prompt Template for book authors
third_input_prompt = PromptTemplate(
                                    input_variables=['summaryofbook'],
                                    template="Please tell me about the authors of the book '{summaryofbook}'"
                                    )

# LLM Chain for getting the authors of the book
chain3 = LLMChain(llm=google_llm, prompt=third_input_prompt, verbose=True, output_key='authorsofthebook')

# Sequential Chain to summarize, get publish date, and authors
parent_chain = SequentialChain(
                                chains=[chain1, chain2, chain3],
                                input_variables=['name'],
                                output_variables=['summaryofbook', 'bookpublishdate', 'authorsofthebook'],
                                verbose=True
                                )

if input_text:
    # Execute the parent chain with the input text (book name)
    result = parent_chain({'name': input_text})
    
    # Display the result in Streamlit
    st.write(f"Summary: {result['summaryofbook']}")
    st.write(f"Publish Date: {result['bookpublishdate']}")
    st.write(f"Authors: {result['authorsofthebook']}")
