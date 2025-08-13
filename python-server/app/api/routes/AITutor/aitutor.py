from fastapi import APIRouter, Cookie, Request
from .helper import  generate_hints, generate_quiz
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/generate/hints")
async def generate_hints_router(question: str, code: str, token: str = Cookie(None)):
    
    try:
        hints_dict = await generate_hints(question, code)
        
        return JSONResponse(content={"hints": hints_dict.get("hint", [])})
    except Exception as e:
        print(f"An error occurred while generating hints: {e}")
        return JSONResponse(
            status_code=500, 
            content={"message": "An internal error occurred. Failed to generate hints."}
        )


@router.post("/generatequiz")
async def generate_roadmap_quiz(request: Request,token: str = Cookie(None)):
    problem = await request.json()
    print("Received problem data:", problem)
    
    question = problem.get("question", "")
    if not question:
        return JSONResponse(
            status_code=400, 
            content={"error": "Question is required"}
        )
    
    quiz = await generate_quiz(question)
    return quiz
