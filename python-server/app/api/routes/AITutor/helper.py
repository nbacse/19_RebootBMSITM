from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from typing import List
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate



async def generate_hints(question: str, code: str):
   
    class Hint(BaseModel):
        hint: List[str]

    parser = JsonOutputParser(pydantic_object=Hint)

    
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.4)

    prompt = PromptTemplate(
        template="""
You are a precise and disciplined lab assistant helping students solve coding problems.

Your task is to analyze the coding problem and the user's submitted code, then provide to-the-point hints.

Rules:
- Do not generate code.
- Do not solve the problem for the user.
- Offer only targeted guidance, hints, or leading questions.
- Be accurate, minimal, and helpful.

---

Coding Problem:
{question}

User Submission:
{code}

---
Based on the problem and the submission, provide your hints.
{format_instructions}
""",
        input_variables=["question", "code"],

        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    response = await chain.ainvoke({"question": question, "code": code})
    
    print("Successfully parsed response:", response)
    return response


async def generate_quiz(problem_description):
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.4)

    class QuestionItem(BaseModel):
        questionNo: int
        question: str
        options: List[str] 
        answer: str

    class Quiz(BaseModel):
        testName: str
        testDescription: str
        totalQuestions: int
        questions: List[QuestionItem]
        difficulty: str

    parser = JsonOutputParser(pydantic_object=Quiz)
    prompt = PromptTemplate(
        template="""
        You are an expert in creating interview preparation quizzes. Based on the question description and the code given in the string format, 
        generate a quiz for job role preparation. 
        Do not make the questions language specific
        Your output must be valid JSON that includes the following fields:
        - testName: Name of the test tailored to the job role.
        - testDescription: A brief description of the test purpose.
        - totalQuestions: The total number of questions.
        - questions: A list of 10 questions, where each question includes:
            - questionNo: The question number.
            - question: The text of the question.
            - options: A list of 4 answer options.
            - answer: The correct answer.
        - difficulty: The difficulty level based on the content.
        
        Ensure that your response is valid JSON.
        
        Problem description:
        {problem_description}
        """,
        input_variables=["problem_description"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser
    response = chain.invoke({"problem_description": problem_description})
    return response



