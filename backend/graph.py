
import os, sys
from langgraph.graph import StateGraph, START, END 

from backend.state import ApplicationState
from backend.llm import ask_llm
from backend.pdf_utils import save_uploaded_file


#---------------RESUME REWRITER AGENT----------------------
def resume_rewriter_agent(state : ApplicationState):
    prompt =f"""
You are a resume rewriter agent. 
Your task is to rewrite the given resume text to make it more effective and tailored for the specified job role.

Rules:
1. Keep the same work history.
2. Do not invent experience or skills that are not present in the original resume.
3. Improve bullet points.
4. Ensure that the rewritten resume is concise and relevant to the job description.
5. Keep it ATS- friendly and professional.

Resume:
{state["resume_text"]}

Job Description:
{state["job_description"]}
"""
    
    tailored_resume = ask_llm(prompt)

    return{
        "tailored_resume": tailored_resume
    }
    


#----------------COVER LETTER AGENT---------------------

def cover_letter_agent(state : ApplicationState):
    prompt = f"""
You are a cover letter writing agent.
Your task is to generate a professional, a one-pagecover letter based on the provided resume and job description.

Job Role:
{state["job_role"]}

Resume:
{state["resume_text"]}

Job Description:
{state["resume_text"]}

use a professional, natural tone.
Do not add experience which is not present in the resume text.
"""
    cover_letter = ask_llm(prompt)

    return {
        "cover_letter": cover_letter
    }



#----------INTERVIEW QUESTION AGENT-------------

def interview_question_agent(state: ApplicationState):
    prompt = f"""
You are an interview preparation agent.
Generate 10 interview preparation questions and sample answers.

Rules:
1. Questions must match the job description.
2. Answers must be based on the resume provided.
3. Include technical, and role-fit questions.

Resume:
{state["resume_text"]}

Job Description:
{state["job_description"]}
    """

    interview_questions = ask_llm(prompt)

    return{
        "interview_questions" : interview_questions

    }


#--------------APPLICATION Summariser AGENT---------------

def application_manager_agent(state: ApplicationState):

    summary = f"""

Application Kit Complete

Role: {state["job_role"]}

Generate summary in concise and professional manner.

Generated files:
- outputs/tailored_resume.md
- outputs/cover_letter.md
- outputs/interview_questions.md
- outputs/application_summary.md
"""
    
    

    save_uploaded_file("outputs/tailored_resume.md", state.get("tailored_resume", ""))
    save_uploaded_file("outputs/cover_letter.md", state.get("cover_letter", ""))
    save_uploaded_file("outputs/interview_questions.md", state.get("interview_questions", ""))
    save_uploaded_file("outputs/application_summary.md", summary)   
    
    return {
        **state,          #this will keep the previous state values and adds the application_summary
        "application_summary": summary
    }


#---------------BUILDING THE GRAPH------------------
def build_graph():
 builder = StateGraph(ApplicationState)

#-------making nodes----------
 builder.add_node("resume_rewriter", resume_rewriter_agent)
 builder.add_node("cover_letter_writer", cover_letter_agent)
 builder.add_node("interview_question_writer", interview_question_agent)
 builder.add_node("application_summary", application_manager_agent)


#--------making edges----------

 builder.add_edge(START, "resume_rewriter")
 builder.add_edge("resume_rewriter", "cover_letter_writer")
 builder.add_edge("cover_letter_writer", "interview_question_writer")
 builder.add_edge("interview_question_writer", "application_summary")
 builder.add_edge("application_summary", END)




# --------compiling the graph-------------
 return  builder.compile()
















   




