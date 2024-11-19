import React, { useState } from 'react';
import OllamaStatus from './components/OllamaStatus';
import ModelSelector from './components/ModelSelector';
import ChatHistory from './components/ChatHistory';
import ChatInput from './components/ChatInput';
import { useChat } from './hooks/useChat';

function App() {
  const [selectedModel, setSelectedModel] = useState('llama2');
  const { messages, isLoading, sendChatMessage } = useChat();

  const handleSendMessage = async (message: string) => {
    await sendChatMessage(message, selectedModel);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-white shadow-sm p-4">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-800">MemoryBot</h1>
          <div className="flex items-center gap-4">
            <OllamaStatus />
            <ModelSelector selectedModel={selectedModel} onModelChange={setSelectedModel} />
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-4xl w-full mx-auto p-4 overflow-hidden flex flex-col">
        <ChatHistory messages={messages} />
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </main>
    </div>
  );
}

export default App;