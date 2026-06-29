import logging
from backend.prompts import resume_qa_prompt
from backend.openai_services import get_completion

logger = logging.getLogger(__name__)


def ask_resume_question(resume_text: str, user_question: str, history: list) -> str:
    """Answer a user's question based on resume text and conversation history."""
    logger.debug(f"QA request — question: '{user_question[:80]}...' | history length: {len(history)}")

    if not resume_text.strip():
        raise ValueError("Resume text is empty. Please upload and analyze a resume first.")
    if not user_question.strip():
        raise ValueError("Question cannot be empty.")

    try:
        prompt = resume_qa_prompt(resume_text, user_question, history)
        result = get_completion(prompt)
        logger.debug("QA response generated successfully.")
        return result

    except Exception as e:
        logger.exception(f"Error generating QA response: {e}")
        raise
