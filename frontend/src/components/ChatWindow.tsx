import React, { useState, useRef, useEffect } from 'react';
import { MessageBubble } from './MessageBubble';
import { Message } from '../types';
import { Send, AlertCircle } from 'lucide-react';

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
  onSendMessage: (msg: string) => void;
  error?: string | null;
}

export function ChatWindow({ messages, isLoading, onSendMessage, error }: ChatWindowProps) {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  return (
    <div className="flex flex-col h-[600px] w-full max-w-2xl bg-gray-50/50 rounded-2xl border border-gray-100 shadow-xl overflow-hidden">
      {/* Header */}
      <div className="bg-white border-b border-gray-100 px-6 py-4 flex items-center shadow-sm z-10">
        <div className="h-3 w-3 bg-green-500 rounded-full mr-3 animate-pulse"></div>
        <h2 className="font-semibold text-gray-800 text-lg tracking-tight">AI Pre-Arrival Triage</h2>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 scroll-smooth">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-gray-400 opacity-80">
            <div className="bg-blue-50 text-blue-500 p-4 rounded-full mb-4 shadow-inner">
               <AlertCircle size={32} />
            </div>
            <p className="text-center font-medium">Describe your symptoms to begin.</p>
            <p className="text-sm mt-2 text-gray-400 max-w-[250px] text-center">We will ask a few follow-up questions to understand your situation.</p>
          </div>
        ) : (
          messages.map((m, idx) => <MessageBubble key={idx} message={m} />)
        )}
        
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-white border border-gray-100 text-gray-500 rounded-2xl rounded-bl-none px-5 py-4 shadow-sm flex space-x-2">
              <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '-0.3s' }}></div>
              <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '-0.15s' }}></div>
              <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce"></div>
            </div>
          </div>
        )}
        
        {error && (
          <div className="flex justify-center mb-4">
             <div className="bg-red-50 text-red-600 px-4 py-2 rounded-lg text-sm font-medium border border-red-100 shadow-sm flex items-center">
               <AlertCircle size={16} className="mr-2" />
               {error}
             </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white p-4 border-t border-gray-100">
        <form onSubmit={handleSend} className="relative flex items-center">
          <input
            type="text"
            className="w-full bg-gray-50 border border-gray-200 text-gray-800 rounded-full pl-6 pr-14 py-4 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-medium placeholder:font-normal"
            placeholder="Type your symptoms..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="absolute right-2 p-2.5 bg-blue-600 text-white rounded-full hover:bg-blue-700 disabled:opacity-50 disabled:hover:bg-blue-600 transition-colors shadow-md shadow-blue-500/20"
          >
            <Send size={18} className="translate-x-[1px] translate-y-[1px]" />
          </button>
        </form>
      </div>
    </div>
  );
}
