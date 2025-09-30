import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.prompts import PromptTemplate

load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')


class Clarity:
    def __init__(self, question=None):
        self.question = question
        self.llm = HuggingFaceEndpoint(repo_id='deepseek-ai/DeepSeek-V3.1-Terminus', task='text-generation',
                            temperature=0.3,   do_sample=False,     max_new_tokens=20  )
        self.chatmodel = ChatHuggingFace(llm=self.llm)
        self.dict_of_whys = {}
    
    def __str__(self):
        return f'you are here to ask a question, you have this {self.question}'


    def getAnswers(self, followUpQuestion = None, questionNumber=0):

        self.followUpQuestion = followUpQuestion

        if not self.followUpQuestion:
            self.followUpQuestion = self.question
        
        
        if questionNumber == 0:
            #self.dict_of_whys = {}

            template = 'Answer in one sentence: {question} ? Please give very short one sentence summary as answer.'
            prompt = PromptTemplate(input_variables=['question'], template=template)
            chain = prompt | self.chatmodel
            response = chain.invoke({'question': self.followUpQuestion})
                
            self.dict_of_whys[self.followUpQuestion] =  response.content
            return response.content

        else:
                
            template = '\n a follow up question to you answer is:.. {followq}. Please give very short one sentence summary as answer.'
            prompt = PromptTemplate(input_variables=['followq'], template=template)
            chain = prompt | self.chatmodel
            response = chain.invoke({'followq':self.followUpQuestion })
                
            self.dict_of_whys[self.followUpQuestion] =  response.content
            return response.content

            

    def getSummary(self):
        
        template = '''based on the question and the follow up and answers given as shown in the dictionary {whys}, the questions are 
                the keys and the answers as the values, use the 5 whys, 
                to list a summary of the 5 questions asked and their short answer. 
                for each of the answers, give 3 academic papers that has researched the question and concluded with the answer as valid for
                the question.
                and give a statement of the final problem discovered as a result of the  5 questions. let it be a short statement '''

        prompt = PromptTemplate(input_variables=['whys'], template = template)

        chain = prompt | self.chatmodel
        response = chain.invoke({'whys': self.dict_of_whys})
        return response.content


if __name__ == '__main__':
    clarity =  Clarity('why do we get old')
    
    clarity.getAnswers(questionNumber= 0)
    print(clarity.dict_of_whys)
    clarity.getAnswers(followUpQuestion='why cant we stop growing', questionNumber= 1)
    print(clarity.dict_of_whys)
    clarity.getAnswers(followUpQuestion='why cant we reverse ageing', questionNumber= 2)
    print(clarity.dict_of_whys)
    print(clarity.getSummary())
    


    

