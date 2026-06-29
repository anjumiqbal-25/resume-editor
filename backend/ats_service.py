import logging
from backend.prompts import ats_prompt
from backend.openai_services import get_completion

logger = logging.getLogger(__name__)


def get_ats_analysis(resume_text: str, job_description: str, job_role: str) -> str:
    """Generate ATS analysis for a resume against a job description."""
    logger.debug(f"Running ATS analysis for role: '{job_role}'")

    if not resume_text.strip():
        raise ValueError("Resume text is empty. Cannot perform ATS analysis.")
    if not job_description.strip():
        raise ValueError("Job description is empty. Cannot perform ATS analysis.")
    if not job_role.strip():
        raise ValueError("Job role is empty. Cannot perform ATS analysis.")

    try:
        prompt = ats_prompt(resume_text, job_description, job_role)
        result = get_completion(prompt)
        logger.debug("ATS analysis completed successfully.")
        return result

    except Exception as e:
        logger.exception(f"Error during ATS analysis: {e}")
        raise
