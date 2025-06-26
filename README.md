🎤 AI Mock Interview Assistant
Practice and perfect your interview skills with this AI-powered Mock Interview Assistant! This Streamlit application allows you to simulate interview sessions, answer questions using your voice, and receive instant, detailed feedback on your responses from Google's Gemini AI.

✨ Features
Diverse Interview Types: Choose from HR, Technical, Behavioral, and Communication interview types.

Adjustable Difficulty: Select between "Beginner" and "Advanced" difficulty levels to tailor the questions to your experience.

Voice-Enabled Responses: Speak your answers naturally, and the application will transcribe them for evaluation.

Real-time AI Feedback: Get comprehensive feedback from Google Gemini AI on your clarity, completeness, relevance, and areas for improvement.

Interview History: Review past questions, your answers, and the AI's evaluations to track your progress and learn from previous sessions.

Microphone Test: Built-in utility to test your microphone setup before starting an interview.

🚀 Demo
While a live demo isn't provided here, you can easily run this application locally by following the installation and usage instructions below.

🛠️ Installation
Follow these steps to set up and run the AI Mock Interview Assistant on your local machine.

Prerequisites
Python 3.8+

pip (Python package installer)

Steps
Clone the repository (or save the code):
If you have the code in a repository, clone it:

git clone <repository-url>
cd <repository-name>

If you have the code directly, save it as app.py (or any .py file) in a directory.

Create a Virtual Environment (Recommended):
It's highly recommended to use a virtual environment to manage dependencies and avoid conflicts with other Python projects.

python -m venv venv

Activate the Virtual Environment:

Windows:

.\venv\Scripts\activate

macOS/Linux:

source venv/bin/activate

Install Dependencies:
Install the required Python libraries using pip. You can create a requirements.txt file with the following content:

requirements.txt

streamlit
SpeechRecognition
pydub
python-dotenv
google-generativeai

Then, install them:

pip install -r requirements.txt

Additional Notes for pydub and SpeechRecognition:

pydub: This library requires ffmpeg to be installed on your system.

Windows: You can download a pre-built ffmpeg executable from ffmpeg.org and add its bin directory to your system's PATH.

macOS: brew install ffmpeg

Linux (Ubuntu/Debian): sudo apt update && sudo apt install ffmpeg

SpeechRecognition: For microphone access, you might also need PyAudio.

pip install pyaudio

If you encounter issues with PyAudio installation on Windows, you might need to install it from a wheel file. Search for PyAudio wheel files compatible with your Python version (e.g., PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl for Python 3.10 64-bit) and install it using pip install path/to/your/wheel_file.whl.

🔑 Configuration: Google Gemini API Key
This application uses Google's Gemini AI for evaluating your answers. You'll need to obtain an API key and set it up as an environment variable.

Get your Gemini API Key:

Go to Google AI Studio.

Sign in with your Google account.

Click on "Get API Key" and then "Create API Key".

Copy your newly generated API key.

Create a .env file:
In the root directory of your project (the same directory as app.py), create a file named .env and add the following line, replacing your_gemini_api_key_here with the actual key you obtained:

GEMINI_API_KEY="your_gemini_api_key_here"

The python-dotenv library will automatically load this key when the application starts.

🏃 Usage
Run the Streamlit application:
Open your terminal, navigate to the project directory (where app.py is located), and run:

streamlit run app.py

This will open the application in your web browser, usually at http://localhost:8501.

Start an Interview:

In the sidebar on the left, select your desired "Interview Type" (e.g., Technical, HR).

Choose a "Difficulty Level" (Beginner or Advanced).

(Optional but Recommended) Click "🎤 Test Microphone" to ensure your audio input is working correctly.

Click the "▶️ Start Interview Session" button.

Answer Questions:

The current interview question will be displayed prominently.

Click "🎙️ Start Recording Your Answer". Speak your answer clearly into your microphone. There's a maximum recording time of 15 seconds.

Once you stop speaking or the time limit is reached, your audio will be transcribed, and the AI will evaluate your answer.

The transcribed answer and the detailed AI feedback will appear on the screen.

Click "➡️ Next Question" to proceed to the next question in the sequence.

End Interview Session:

You can end the interview session at any time by clicking "🔄 End Interview Session" in the sidebar. This will clear the current progress and history.

Once all questions are completed, a "Session Summary" will be displayed, and you'll have the option to start a new session.

Review Interview History:

Scroll down to the "📝 Interview History" section to review all your past questions, your transcribed answers, and the AI's feedback from previous sessions. This is a great way to track your improvement over time.

📁 Project Structure
.
├── app.py
├── .env                  (for storing GEMINI_API_KEY)
└── requirements.txt
└── user_answer.wav       (temporary file for recorded audio)

app.py: The main Streamlit application file containing all the UI logic, speech recognition, and Gemini integration.

.env: Stores your Google Gemini API key as an environment variable.

requirements.txt: Lists all Python dependencies required for the project.

user_answer.wav: A temporary file created to save the user's recorded audio for transcription.

❓ Question Bank
The question_bank in app.py is a Python dictionary that stores interview questions categorized by type and difficulty. You can easily extend this bank by adding more questions to existing categories or creating entirely new categories.

Example:

question_bank = {
    "HR": {
        "Beginner": [
            "Tell me about yourself.",
            "Why should we hire you?",
            "What are your strengths and weaknesses?"
        ],
        # ... more questions
    },
    "Technical": {
        "Beginner": [
            "What is Object-Oriented Programming?",
            # ... more questions
        ],
        "Advanced": [
            "What is the difference between REST and GraphQL?",
            # ... more questions
        ]
    },
    # ... more interview types
}

💡 Future Enhancements
Text Input Option: Allow users to type their answers instead of or in addition to voice input.

Session Saving/Loading: Implement a way to save interview sessions (e.g., to a JSON file or a simple database) and load them later.

Customizable Questions: Allow users to input their own questions or add to the existing question bank via the UI.

Speech Rate and Clarity Analysis: Integrate more advanced speech analysis to provide feedback on speaking pace, filler words, and overall clarity.

Progress Tracking Visualizations: Display graphs or charts to visualize improvement in scores or specific feedback areas over time.

Interview Coaching Tips: Offer general interview tips or resources based on the selected interview type.

More Diverse AI Models: Experiment with different Gemini models or other LLMs for varied feedback styles.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

Fork the repository.

Create a new branch for your feature (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

📄 License
This project is open-source and available under the MIT License.

🙏 Acknowledgments
Streamlit for providing an amazing framework for building web applications with Python.

Google Gemini API for the powerful AI evaluation capabilities.

SpeechRecognition library for voice-to-text functionality.

pydub library for audio manipulation.

python-dotenv for environment variable management.

Image by storyset (modified) for the engaging visual.
