"use client";

import { useState, useRef, KeyboardEvent, useEffect, forwardRef, useImperativeHandle } from "react";
import { Button } from "@/components/ui/button";
import { useSpeechRecognition, SpeechLanguage } from "@/lib/voice/use-speech-recognition";

interface MessageInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

// Expose methods to parent via ref
export interface MessageInputRef {
  setValue: (value: string) => void;
  focus: () => void;
}

export const MessageInput = forwardRef<MessageInputRef, MessageInputProps>(
  function MessageInput({
    onSend,
    disabled = false,
    placeholder = "Type a message...",
  }, ref) {
  const [message, setMessage] = useState("");
  const [voiceLang, setVoiceLang] = useState<SpeechLanguage>("ur-PK");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Expose methods to parent
  useImperativeHandle(ref, () => ({
    setValue: (value: string) => {
      setMessage(value);
      // Focus the textarea
      if (textareaRef.current) {
        textareaRef.current.focus();
      }
    },
    focus: () => {
      textareaRef.current?.focus();
    }
  }));

  const {
    isListening,
    isSupported,
    transcript,
    interimTranscript,
    error: speechError,
    startListening,
    stopListening,
    resetTranscript,
    setLanguage,
  } = useSpeechRecognition({
    language: voiceLang,
    continuous: false,
    interimResults: true,
  });

  // Update message when transcript changes
  useEffect(() => {
    if (transcript) {
      setMessage(transcript);
      // Auto-send after final transcript
      if (!isListening && transcript.trim()) {
        onSend(transcript.trim());
        resetTranscript();
        setMessage("");
      }
    }
  }, [transcript, isListening, onSend, resetTranscript]);

  // Show interim results in textarea
  useEffect(() => {
    if (isListening && interimTranscript) {
      setMessage(interimTranscript);
    }
  }, [interimTranscript, isListening]);

  const handleSend = () => {
    const trimmedMessage = message.trim();
    if (!trimmedMessage || disabled) return;

    onSend(trimmedMessage);
    setMessage("");
    resetTranscript();

    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  };

  const handleMicClick = () => {
    if (isListening) {
      stopListening();
    } else {
      resetTranscript();
      setMessage("");
      startListening();
    }
  };

  const toggleLanguage = () => {
    const newLang = voiceLang === "ur-PK" ? "en-US" : "ur-PK";
    setVoiceLang(newLang);
    setLanguage(newLang);
  };

  return (
    <div className="p-4 border-t bg-background">
      {/* Language toggle + error display */}
      <div className="flex items-center justify-between mb-2 text-xs">
        <button
          onClick={toggleLanguage}
          className="text-muted-foreground hover:text-foreground transition-colors"
          title="Toggle voice language"
        >
          🎤 {voiceLang === "ur-PK" ? "اردو" : "English"}
        </button>
        {speechError && (
          <span className="text-destructive">{speechError}</span>
        )}
        {isListening && (
          <span className="text-red-500 animate-pulse flex items-center gap-1">
            <span className="w-2 h-2 bg-red-500 rounded-full"></span>
            Listening...
          </span>
        )}
      </div>

      {/* Input row */}
      <div className="flex gap-2 items-end">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          onInput={handleInput}
          placeholder={isListening ? "Listening..." : placeholder}
          disabled={disabled || isListening}
          rows={2}
          className="flex-1 resize-none rounded-lg border border-input bg-background px-4 py-3 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 min-h-[4.5rem]"
        />

        {/* Mic button */}
        {isSupported && (
          <Button
            type="button"
            variant={isListening ? "destructive" : "outline"}
            onClick={handleMicClick}
            disabled={disabled}
            className="h-12 w-12 p-0"
            title={isListening ? "Stop listening" : "Start voice input"}
          >
            {isListening ? "⏹️" : "🎤"}
          </Button>
        )}

        {/* Send button */}
        <Button
          onClick={handleSend}
          disabled={disabled || !message.trim() || isListening}
          className="h-12 px-6"
        >
          {disabled ? "..." : "➤"}
        </Button>
      </div>
    </div>
  );
});
