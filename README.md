# SmartHome AI 🏠

An intelligent home automation system powered by AI, built with Streamlit and Groq API.

## Features

- 🤖 **AI-Powered Control**: Uses Groq API for intelligent home automation decisions
- 🎤 **Voice Recognition**: Speech-to-text integration for hands-free control
- 🎨 **Modern UI**: Beautiful, responsive interface built with Streamlit
- 🔒 **Secure**: Environment-based secret management
- 📱 **Easy to Use**: Intuitive controls and real-time feedback

## Requirements

- Python 3.8+
- Streamlit
- Groq API key
- SpeechRecognition
- pydub

## Installation

1. Clone the repository:
```bash
git clone https://github.com/NischithGowdaR/ai_home_automation_system.git
cd ai_home_automation_system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment:
Create a `.env` file with your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## Usage

Run the application:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
ai_home_automation_system/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not tracked)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Technologies Used

- **Streamlit**: Web framework for data apps
- **Groq API**: Powerful AI language model
- **SpeechRecognition**: Voice input processing
- **pydub**: Audio processing
- **python-dotenv**: Environment variable management

## License

MIT License - Feel free to use this project for your own purposes.

## Contributing

Contributions are welcome! Feel free to submit issues and enhancement requests.
