import React, { useState, useRef } from 'react';
import { Mic, Send } from 'lucide-react';

function VoiceCommand({ onTextCommand, onVoiceCommand }) {
  const [isRecording, setIsRecording] = useState(false);
  const [textInput, setTextInput] = useState('');
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setIsLoading(true);
        try {
          const res = await onVoiceCommand(audioBlob);
          setResponse(res);
        } catch (err) {
          setResponse({ message: "Error processing voice command." });
        } finally {
          setIsLoading(false);
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Error accessing microphone:", err);
      alert("Microphone access is required for voice commands.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  const handleToggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const handleSendText = async (e) => {
    e.preventDefault();
    if (!textInput.trim()) return;
    
    setIsLoading(true);
    try {
      const res = await onTextCommand(textInput);
      setResponse(res);
      setTextInput('');
    } catch (err) {
      setResponse({ message: "Error processing text command." });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="voice-section">
      <button 
        className={`mic-btn ${isRecording ? 'recording' : ''}`}
        onClick={handleToggleRecording}
      >
        <Mic size={40} />
      </button>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem', fontSize: '0.9rem' }}>
        {isRecording ? "Listening... Click to stop" : "Click the microphone to speak"}
      </p>

      <form className="text-input-container" onSubmit={handleSendText}>
        <input 
          type="text" 
          className="text-input" 
          placeholder="Or type your command here..." 
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          disabled={isLoading}
        />
        <button type="submit" className="send-btn" disabled={isLoading || !textInput.trim()}>
          {isLoading ? <div className="loader" style={{ width: '16px', height: '16px', borderWidth: '2px' }}></div> : <Send size={18} />}
        </button>
      </form>

      {response && (
        <div className="ai-response-box">
          <div className="ai-label">🤖 AI Response</div>
          {response.transcription && <p style={{ fontStyle: 'italic', color: 'var(--text-secondary)', marginBottom: '0.5rem', fontSize: '0.9rem' }}>"{response.transcription}"</p>}
          <p style={{ color: 'var(--text-primary)', lineHeight: 1.6 }}>{response.message}</p>
        </div>
      )}
    </div>
  );
}

export default VoiceCommand;
