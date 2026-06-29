import logging
import streamlit as st
from backend.ats_service import get_ats_analysis
from backend.qa_service import ask_resume_question
from backend.graph import build_graph
from backend.pdf_utils import read_text_file
from pypdf import PdfReader
from backend.pdf_utils import extract_text_from_pdf
from backend.resume_db import create_tables, save_chat



create_tables()
save_chat("role" ,"content")


if "agent_result" not in st.session_state:
    st.session_state.agent_result = None




logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Resume Optimization and ATS Analysis",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Resume Optimization and ATS Analyser")

# ---------SESSION STATE FOR HISTORY----------------
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------UI INPUTS-------------------
job_role = st.text_input("Enter the job title (e.g. AI Engineer, Software Engineer):")
job_description = st.text_area("Enter the job description:")
uploaded_file = st.file_uploader("Upload your resume (PDF format only):", type=["pdf"])

# ------------------ATS ANALYSIS BUTTON-------------------
resume_text=""
if st.button("Analyse Resume"):
    if not resume_text.strip():
         st.error("Please upload a Resume before Analysing.")
         st.stop()
   
    # if uploaded_file is not None:
    #    resume_text = extract_text_from_pdf(uploaded_file)
    #    st.write(resume_text)

    if uploaded_file is None:
       st.warning("Please upload a resume in PDF format.")

    elif not job_role or not job_description:
     st.warning("Please enter both the job title and job description.")

else:
    with st.spinner("Analysing your resume..."):

    # Extract text from the uploaded Pdf  file
        logger.debug("Starting PDF extraction.")
        resume_text = extract_text_from_pdf(uploaded_file)
        st.session_state.resume_text = resume_text
        logger.debug(f"PDF extracted: {len(resume_text)} characters.")
        result = get_ats_analysis(
            resume_text,
            job_description,
            job_role
             
        )
        st.session_state.ats_result = result
        st.success("ATS analysis complete!")

        if st.session_state.ats_result:
            st.subheader("📊 ATS Result")
            st.markdown(st.session_state.ats_result)


           
# -------------Generating the Application Kit Button---------- 
if st.button("Generate Application Kit"):
        if uploaded_file is None:
           st.warning("Please upload a resume in PDF format.")

        elif not job_role or not job_description:
            st.warning("Please enter the jon title and job description.")


        else:
            with st.spinner("Generating Application Kit..."):

            # resume_path = save_uploaded_file(uploaded_file , job_description)
                resume_text = extract_text_from_pdf(uploaded_file)
                st.session_state.resume_text = resume_text


                graph = build_graph()

                result = graph.invoke({
                    "resume_text": resume_text,
                    "job_description": job_description,
                    "job_role": job_role,
                    "tailored_resume": "",
                    "cover_letter": "",
                    "interview_questions": "",
                    "application_summary": ""
                })

                st.session_state.agent_result = result
                st.success("✅ Application kit generated!")


if st.session_state.agent_result:
    result = st.session_state.agent_result

# ------------creating the tabs
    tab1, tab2, tab3, tab4 = st.tabs([
            "Cover Letter",
            "Tailored Resume",
            "Interview Questions",
            "Application Summary"
    ])
    with tab1:
            st.subheader("Cover Letter")
            st.markdown(result["cover_letter"])

    with tab2:
            st.subheader("Tailored Resume")
            st.markdown(result["tailored_resume"])

    with tab3:
            st.subheader("Mock Interview Questions")
            st.markdown(result["interview_questions"])

    with tab4:
            st.subheader("Application Summary")
            st.markdown(result["application_summary"])

           
           
# -----------------RESUME Q & A-------------------
if st.session_state.resume_text:
    st.divider()
    st.subheader("💬 Ask Questions about Your Resume:")

        # Display chat history
    for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # User input
    user_question = st.chat_input("Ask a question about your resume:")

    if user_question:
            logger.debug(f"User asked: {user_question}")

            # Storing and displaying the user message
            st.session_state.messages.append({
                "role": "user", 
                "content": user_question
            })
            with st.chat_message("user"):
                st.write(user_question)


            # Getting LLM response
            with st.spinner("Generating response..."):
                try:
                    answer = ask_resume_question(
                        st.session_state.resume_text,
                        user_question,
                        st.session_state.messages
                    )
                    logger.debug("QA response received.")

                except ValueError as e:
                    logger.warning(f"Validation error in QA: {e}")
                    answer = f"⚠️ {e}"

                except Exception as e:
                    logger.exception(f"Unexpected error in QA: {e}")
                    answer = "❌ Something went wrong in generating a response. Please try again."

            # Store and display assistant message
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)



    

# -----------------CLEAR CHAT HISTORY BUTTON-------------------
if st.session_state.messages:
    if st.button("🧹 Clear Chat"):
         st.session_state.messages = []
         st.rerun()


# -----------------------Invoking the graph-----------

def main():
    resume_text = PdfReader("resume/resume.pdf")
    jd_text = read_text_file("job_descriptions/jd.txt")


    graph = build_graph()

    result = graph.invoke({
        "resume_text": resume_text,
        "job_description": jd_text,
        "company_name": "Example Company",
        "role_title" : "Software Engineer",
        "tailored_resume": "",
        "cover_letter": "",
        "interview_questions": "",
        "application_summary": ""
    })                

    print(result["application_summary"])

    if __name__ == "__main__":
        main()


