
from  typing_extensions import TypedDict


class ApplicationState(TypedDict):
    resume_text: str
    job_description: str
    ats_response: str
    job_role:str
    tailored_resume:str
    cover_letter:str
    interview_questions:str
    application_summary:str
    agent_result: str

    
