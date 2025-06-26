import streamlit as st
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.playback import play # While pydub.playback is here, direct playback in Streamlit needs st.audio
import google.generativeai as genai
from dotenv import load_dotenv
import json # For simple history storage
import datetime # For timestamps in history

# --- Configuration ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Session State Initialization ---
# This is crucial for managing interview flow and data across user interactions
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'interview_history' not in st.session_state:
    st.session_state.interview_history = []
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'selected_interview_type' not in st.session_state:
    st.session_state.selected_interview_type = "Technical" # Default
if 'selected_difficulty' not in st.session_state:
    st.session_state.selected_difficulty = "Beginner" # Default
if 'current_question_list' not in st.session_state:
    st.session_state.current_question_list = []

# --- Question Bank (More comprehensive) ---
question_bank = {
    "HR": {
        "Beginner": [
            "Tell me about yourself.",
            "Why should we hire you?",
            "What are your strengths and weaknesses?"
        ],
        "Advanced": [
            "Describe a conflict at work and how you handled it.",
            "Tell me about a time you showed leadership in a difficult situation.",
            "How do you handle pressure and tight deadlines?"
        ]
    },
    "Technical": {
        "Beginner": [
            "What is Object-Oriented Programming?",
            "Explain the concept of inheritance in Python.",
            "What are the advantages of using functions in programming?",
            "What is the difference between a list and a tuple in Python?",
            "Explain what Git is and why it's used."
        ],
        "Advanced": [
            "What is the difference between REST and GraphQL?",
            "Explain multithreading vs multiprocessing with examples.",
            "Describe how garbage collection works in Java or Python.",
            "How would you design a scalable microservices architecture?",
            "Explain ACID properties in databases and their importance."
        ]
    },
    "Behavioral": {
        "Beginner": [
            "How do you handle feedback?",
            "Describe a time when you worked in a team.",
            "How do you prioritize tasks when everything is a priority?"
        ],
        "Advanced": [
            "Describe a time when you missed a deadline. What did you do?",
            "Tell me about a mistake you made and how you learned from it.",
            "Describe a situation where you had to motivate a team or colleague."
        ]
    },
    "Communication": {
        "Beginner": [
            "How would you explain a technical topic to a non-technical person?",
            "How do you ensure clear communication in a team?"
        ],
        "Advanced": [
            "Give an example where you had to present a complex idea effectively.",
            "Describe a situation where miscommunication caused a problem.",
            "How do you handle disagreements or conflicts during team discussions?"
        ]
    }
}

# --- Gemini Scoring Function (Enhanced Prompt) ---
def evaluate_answer(question, answer, interview_type, difficulty):
    # The prompt is crucial for getting better feedback.
    # We instruct Gemini to be more specific.
    prompt = f"""You are an experienced professional interviewer and a highly skilled evaluator.
    A candidate was asked the following {interview_type} question at a {difficulty} level:
    "{question}"

    Their answer was:
    "{answer}"

    Please provide a comprehensive evaluation based on the following criteria:
    1.  **Score:** A score out of 10.
    2.  **Clarity & Coherence:** How clear, concise, and logical was the answer?
    3.  **Completeness & Accuracy:** Did the answer fully address the question? Was it technically accurate (if applicable)?
    4.  **Relevance:** Was the answer directly relevant to the question asked?
    5.  **Areas for Improvement:** Specific, actionable suggestions on how the candidate could improve their answer.
    6.  **Keywords (if Technical):** Mention any important keywords or concepts that were missing or could have been included (for technical questions).
    7.  **STAR Method (if Behavioral):** If this is a behavioral question, assess if the answer followed the STAR (Situation, Task, Action, Result) method effectively.

    Respond in a structured Markdown format, starting with the overall score.
    Example Format:
    **Overall Score: X/10**

    ---
    **Detailed Feedback:**
    * **Clarity & Coherence:** ...
    * **Completeness & Accuracy:** ...
    * **Relevance:** ...
    * **Areas for Improvement:** ...
    * **[Specific to question type, e.g., Keywords/STAR]:** ...
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash") # Use a model suitable for detailed responses
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error evaluating answer with Gemini: {e}")
        return "Evaluation currently unavailable due to an error."

# --- Helper Function for Microphone Check ---
def check_microphone():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Testing microphone... Please say something.")
            audio = r.listen(source, timeout=3, phrase_time_limit=3)
            test_text = r.recognize_google(audio)
            st.success(f"Microphone test successful! Heard: '{test_text}'")
            return True
    except sr.WaitTimeoutError:
        st.warning("No speech detected during microphone test. Please ensure your microphone is working and speak clearly.")
        return False
    except sr.UnknownValueError:
        st.warning("Could not understand audio during microphone test. Please try speaking clearer.")
        return False
    except sr.RequestError:
        st.error("Could not access Google Speech Recognition service during microphone test. Check your internet connection.")
        return False
    except Exception as e:
        st.error(f"An error occurred during microphone test: {e}. Please ensure your microphone is properly connected.")
        return False

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="AI Mock Interview Assistant", page_icon="🎙️")

st.title("🎤 AI Mock Interview Assistant")
st.markdown("Practice your interview skills with AI-powered feedback. Your responses are transcribed and evaluated by Gemini AI.")

# --- Sidebar for Navigation and Settings ---
with st.sidebar:
    st.header("Settings")
    # Section for interview configuration
    st.session_state.selected_interview_type = st.selectbox(
        "Select Interview Type",
        list(question_bank.keys()),
        index=list(question_bank.keys()).index(st.session_state.selected_interview_type),
        key="interview_type_selector"
    )
    st.session_state.selected_difficulty = st.selectbox(
        "Select Difficulty Level",
        ["Beginner", "Advanced"],
        index=["Beginner", "Advanced"].index(st.session_state.selected_difficulty),
        key="difficulty_selector"
    )

    if st.button("🎤 Test Microphone"):
        check_microphone()

    st.markdown("---")
    st.header("Interview Flow Control")
    if not st.session_state.interview_started:
        if st.button("▶️ Start Interview Session"):
            st.session_state.interview_started = True
            # Initialize questions based on selection
            st.session_state.current_question_list = question_bank[st.session_state.selected_interview_type][st.session_state.selected_difficulty]
            st.session_state.current_question_index = 0
            st.session_state.interview_history = [] # Reset history for new session
            st.experimental_rerun() # Rerun to update main content
    else:
        if st.button("🔄 End Interview Session", help="This will clear current progress and history."):
            st.session_state.interview_started = False
            st.session_state.current_question_index = 0
            st.session_state.interview_history = []
            st.session_state.current_question_list = []
            st.experimental_rerun() # Rerun to update main content

# --- Main Content Area ---
st.markdown("---") # Separator

if not st.session_state.interview_started:
    st.info("Select your interview type and difficulty from the sidebar and click 'Start Interview Session' to begin.")
    st.image("https://img.freepik.com/free-vector/interview-concept-illustration_114360-1493.jpg?w=740&t=st=1719244030~exp=1719244630~hmac=a4c95a2872d80d24177d5440d9b40026e64c11b2386295fc9f598a72c1c1f4e1",
             caption="Prepare for your next interview!", use_column_width=True)

else:
    # --- Interview in Progress ---
    current_questions = st.session_state.current_question_list

    if st.session_state.current_question_index < len(current_questions):
        current_question = current_questions[st.session_state.current_question_index]
        st.header(f"Question {st.session_state.current_question_index + 1}/{len(current_questions)}:")
        st.info(current_question)

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("🎙️ Start Recording Your Answer"):
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    st.write("---") # Visual separator
                    with st.spinner("Recording... Please speak clearly after the beep. (Max 15 seconds)"):
                        # Add a short delay or sound for user readiness (optional, more complex)
                        try:
                            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
                            audio_path = "user_answer.wav"
                            with open(audio_path, "wb") as f:
                                f.write(audio.get_wav_data())
                            st.success("Recording complete!")
                            st.audio(audio_path, format='audio/wav', start_time=0) # Playback for self-review
                            st.session_state.last_recorded_audio_path = audio_path # Store path
                            st.session_state.recording_successful = True # Flag for transcription step
                        except sr.WaitTimeoutError:
                            st.warning("No speech detected. Please try again.")
                            st.session_state.recording_successful = False
                        except Exception as e:
                            st.error(f"Error during recording: {e}")
                            st.session_state.recording_successful = False
        with col2:
             if st.session_state.get('recording_successful', False):
                st.markdown("### Your Transcribed Answer:")
                # Transcribe
                try:
                    # Load audio from saved file to avoid listening again if not needed
                    r = sr.Recognizer()
                    with sr.AudioFile(st.session_state.last_recorded_audio_path) as source:
                        audio_data = r.record(source) # read the entire audio file
                    text = r.recognize_google(audio_data)
                    st.info(text)
                    st.session_state.transcribed_answer = text # Store transcribed answer

                    # Evaluate via Gemini
                    st.markdown("### 🤖 Gemini Feedback")
                    with st.spinner("Evaluating your answer ..."):
                        evaluation = evaluate_answer(
                            current_question,
                            text,
                            st.session_state.selected_interview_type,
                            st.session_state.selected_difficulty
                        )
                        st.markdown(evaluation) # Display evaluation in markdown

                    # Store in history
                    st.session_state.interview_history.append({
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "type": st.session_state.selected_interview_type,
                        "difficulty": st.session_state.selected_difficulty,
                        "question": current_question,
                        "answer": text,
                        "evaluation": evaluation
                    })

                    # Reset recording flag
                    st.session_state.recording_successful = False

                except sr.UnknownValueError:
                    st.error("Could not understand audio. Please speak more clearly.")
                except sr.RequestError as e:
                    st.error(f"Could not request results from Google Speech Recognition service; {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred during transcription or evaluation: {e}")

        # Navigation for next question
        if st.session_state.get('transcribed_answer') and st.button("➡️ Next Question"):
            st.session_state.current_question_index += 1
            st.session_state.transcribed_answer = None # Clear for next question
            st.experimental_rerun()
    else:
        st.success("🎉 You've completed all questions in this session! 🎉")
        st.write("---")
        st.subheader("Session Summary")
        st.info("You can review your answers and feedback in the 'Interview History' section below.")
        if st.button("Start New Session"):
            st.session_state.interview_started = False
            st.session_state.current_question_index = 0
            st.session_state.current_question_list = []
            st.experimental_rerun()

# --- Interview History Section ---
st.markdown("---")
st.header("📝 Interview History")

if st.session_state.interview_history:
    # Allow filtering or sorting history if it grows large
    # st.subheader("Filter History:")
    # # TODO: Add filters by type, difficulty, etc.

    for i, entry in enumerate(reversed(st.session_state.interview_history)): # Show most recent first
        st.subheader(f"Session {len(st.session_state.interview_history) - i} - {entry['timestamp']}")
        st.markdown(f"**Type:** {entry['type']} | **Difficulty:** {entry['difficulty']}")
        st.markdown(f"**Question:** *{entry['question']}*")
        st.markdown(f"**Your Answer:**")
        st.code(entry['answer'])
        st.markdown(f"**AI Feedback:**")
        st.markdown(entry['evaluation']) # Use markdown to render the formatted evaluation
        st.markdown("---")
else:
    st.info("No interview history yet. Start a session to see your progress here!")