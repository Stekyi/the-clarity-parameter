import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.prompts import PromptTemplate

load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')


llm = HuggingFaceEndpoint(repo_id='deepseek-ai/DeepSeek-V3.1-Terminus', task='text-generation',
                          temperature=0.3,   do_sample=False,     max_new_tokens=20  )
chatmodel = ChatHuggingFace(llm=llm)


mainQuestion = ''
followUp = ''
dict_of_whys = {}


for i in range(0,5):
    if i == 0:
        
        mainQuestion = input('ask ur question:..  ')
        template = 'Answer in one sentence: {question} ? Please give very short one sentence summary as answer.'
        prompt = PromptTemplate(input_variables=['question'], template=template)
        chain = prompt | chatmodel
        response = chain.invoke({'question': mainQuestion})
        print(response.content)

        dict_of_whys[mainQuestion] =  response.content

    else:
        followUp = input(f' Ask your {i} follow-up')
        template = '\na follow up question to you answer is:.. {followq}. Please give very short one sentence summary as answer.'
        prompt = PromptTemplate(input_variables=['followq'], template=template)
        chain = prompt | chatmodel
        response = chain.invoke({'followq':followUp })
        print(response.content)

        dict_of_whys[followUp] =  response.content
      

template = '''based on the question and the follow up and answers given as shown in the dictionary {whys}, the questions are 
            the keys and the answers as the values, use the 5 whys, 
            to list a summary of the 5 questions asked and their short answer. 
            for each of the answers, give 3 academic papers that has researched the question and concluded with the answer as valid for
            the question.
            and give a statement of the final problem discovered as a result of the  5 questions. let it be a short statement '''

prompt = PromptTemplate(input_variables=['whys'], template = template)

chain = prompt | chatmodel

response = chain.invoke({'whys': dict_of_whys})

print(response.content)
