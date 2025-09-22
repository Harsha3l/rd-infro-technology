// Frontend Integration Example for ECHOAL
// This shows how to connect your frontend to the backend API

class ECHOALAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    // Send a message to the AI
    async sendMessage(content, conversationId = null) {
        try {
            const response = await fetch(`${this.baseURL}/api/chat/send`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: content,
                    conversation_id: conversationId
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }

    // Get all conversations
    async getConversations() {
        try {
            const response = await fetch(`${this.baseURL}/api/conversations`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting conversations:', error);
            throw error;
        }
    }

    // Get messages for a specific conversation
    async getMessages(conversationId) {
        try {
            const response = await fetch(`${this.baseURL}/api/conversations/${conversationId}/messages`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting messages:', error);
            throw error;
        }
    }

    // Delete a conversation
    async deleteConversation(conversationId) {
        try {
            const response = await fetch(`${this.baseURL}/api/conversations/${conversationId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error deleting conversation:', error);
            throw error;
        }
    }

    // Update conversation title
    async updateConversationTitle(conversationId, title) {
        try {
            const response = await fetch(`${this.baseURL}/api/conversations/${conversationId}/title`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title: title })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error updating title:', error);
            throw error;
        }
    }

    // Get settings
    async getSettings() {
        try {
            const response = await fetch(`${this.baseURL}/api/settings`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting settings:', error);
            throw error;
        }
    }

    // Update settings
    async updateSettings(settings) {
        try {
            const response = await fetch(`${this.baseURL}/api/settings`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(settings)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error updating settings:', error);
            throw error;
        }
    }

    // Reset settings to default
    async resetSettings() {
        try {
            const response = await fetch(`${this.baseURL}/api/settings/reset`, {
                method: 'POST'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error resetting settings:', error);
            throw error;
        }
    }

    // Get available themes
    async getAvailableThemes() {
        try {
            const response = await fetch(`${this.baseURL}/api/settings/themes`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting themes:', error);
            throw error;
        }
    }

    // Get available languages
    async getAvailableLanguages() {
        try {
            const response = await fetch(`${this.baseURL}/api/settings/languages`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting languages:', error);
            throw error;
        }
    }

    // Get available AI models
    async getAvailableAIModels() {
        try {
            const response = await fetch(`${this.baseURL}/api/settings/ai-models`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting AI models:', error);
            throw error;
        }
    }

    // Health check
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error checking health:', error);
            throw error;
        }
    }
}

// Usage example:
const api = new ECHOALAPI();

// Example: Send a message
async function sendMessage() {
    try {
        const result = await api.sendMessage("Hello, how are you?");
        console.log('AI Response:', result.message.content);
        console.log('Conversation ID:', result.conversation_id);
        return result;
    } catch (error) {
        console.error('Failed to send message:', error);
    }
}

// Example: Get all conversations
async function loadConversations() {
    try {
        const conversations = await api.getConversations();
        console.log('Conversations:', conversations);
        return conversations;
    } catch (error) {
        console.error('Failed to load conversations:', error);
    }
}

// Example: Get messages for a conversation
async function loadMessages(conversationId) {
    try {
        const messages = await api.getMessages(conversationId);
        console.log('Messages:', messages);
        return messages;
    } catch (error) {
        console.error('Failed to load messages:', error);
    }
}

// Example: Load and display settings
async function loadSettings() {
    try {
        const settings = await api.getSettings();
        console.log('Current settings:', settings);
        return settings;
    } catch (error) {
        console.error('Failed to load settings:', error);
    }
}

// Example: Update theme
async function changeTheme(theme) {
    try {
        const result = await api.updateSettings({ theme: theme });
        console.log('Theme updated:', result);
        return result;
    } catch (error) {
        console.error('Failed to update theme:', error);
    }
}

// Example: Update language
async function changeLanguage(language) {
    try {
        const result = await api.updateSettings({ language: language });
        console.log('Language updated:', result);
        return result;
    } catch (error) {
        console.error('Failed to update language:', error);
    }
}

// Example: Update AI model
async function changeAIModel(model) {
    try {
        const result = await api.updateSettings({ ai_model: model });
        console.log('AI model updated:', result);
        return result;
    } catch (error) {
        console.error('Failed to update AI model:', error);
    }
}

// Example: Reset all settings
async function resetAllSettings() {
    try {
        const result = await api.resetSettings();
        console.log('Settings reset:', result);
        return result;
    } catch (error) {
        console.error('Failed to reset settings:', error);
    }
}

// Export for use in your frontend
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ECHOALAPI;
}
