// Production Configuration for ECHOAL Frontend
// Use this configuration in your Vercel-deployed frontend

const ECHOAL_CONFIG = {
    // Production Backend URL
    API_BASE_URL: 'https://echoai-5n2z.onrender.com',
    
    // Frontend URL (for reference)
    FRONTEND_URL: 'https://echoai-git-main-harsha-tri-lakshmis-projects.vercel.app',
    
    // API Endpoints
    ENDPOINTS: {
        CHAT_SEND: '/api/chat/send',
        CONVERSATIONS: '/api/conversations',
        MESSAGES: '/api/conversations/{id}/messages',
        DELETE_CONVERSATION: '/api/conversations/{id}',
        UPDATE_TITLE: '/api/conversations/{id}/title',
        SETTINGS: '/api/settings',
        SETTINGS_RESET: '/api/settings/reset',
        THEMES: '/api/settings/themes',
        LANGUAGES: '/api/settings/languages',
        AI_MODELS: '/api/settings/ai-models',
        HEALTH: '/health'
    },
    
    // Default settings
    DEFAULT_SETTINGS: {
        theme: 'light',
        language: 'en',
        ai_model: 'ECHOAL Assistant',
        temperature: 0.7,
        max_tokens: 500,
        auto_save: true,
        notifications: true
    },
    
    // Request configuration
    REQUEST_CONFIG: {
        headers: {
            'Content-Type': 'application/json',
        },
        timeout: 30000, // 30 seconds
        retryAttempts: 3
    }
};

// Enhanced ECHOAL API class for production
class ECHOALProductionAPI {
    constructor() {
        this.baseURL = ECHOAL_CONFIG.API_BASE_URL;
        this.config = ECHOAL_CONFIG.REQUEST_CONFIG;
    }

    // Helper method to build full URL
    buildURL(endpoint) {
        return `${this.baseURL}${endpoint}`;
    }

    // Helper method to handle requests with retry
    async makeRequest(url, options = {}, retryCount = 0) {
        try {
            const response = await fetch(url, {
                ...this.config,
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            if (retryCount < this.config.retryAttempts) {
                console.warn(`Request failed, retrying... (${retryCount + 1}/${this.config.retryAttempts})`);
                await new Promise(resolve => setTimeout(resolve, 1000 * (retryCount + 1))); // Exponential backoff
                return this.makeRequest(url, options, retryCount + 1);
            }
            throw error;
        }
    }

    // Send a message to the AI
    async sendMessage(content, conversationId = null) {
        const url = this.buildURL(ECHOAL_CONFIG.ENDPOINTS.CHAT_SEND);
        return this.makeRequest(url, {
            method: 'POST',
            body: JSON.stringify({
                content: content,
                conversation_id: conversationId
            })
        });
    }

    // Get all conversations
    async getConversations() {
        const url = this.buildURL(ECHOAL_CONFIG.ENDPOINTS.CONVERSATIONS);
        return this.makeRequest(url);
    }

    // Get messages for a specific conversation
    async getMessages(conversationId) {
        const url = this.buildURL(ECHOAL_CONFIG.ENDPOINTS.MESSAGES.replace('{id}', conversationId));
        return this.makeRequest(url);
    }

    // Delete a conversation
    async deleteConversation(conversationId) {
        const url = this.buildURL(ECHOAL_CONFIG.ENDPOINTS.DELETE_CONVERSATION.replace('{id}', conversationId));
        return this.makeRequest(url, { method: 'DELETE' });
    }

    // Update conversation title
    async updateConversationTitle(conversationId, title) {
        const url = this.buildURL(ECHOAL_CONFIG.ENDPOINTS.UPDATE_TITLE.replace('{id}', conversationId));
        return this.makeRequest(url, {
            method: 'PUT',
            body: JSON.stringify({ title: title })
        });
    }

    // Get current settings
    async getSettings() {
        const url = this.buildURL(ECHOAL_CONFIG.ENDPOINTS.SETTINGS);
        return this.makeRequest(url);
    }

    // Update settings
    async updateSettings(settings) {
        const url = this.buildURL(ECHOAL_CONFIG.ENDPOINTS.SETTINGS);
        return this.makeRequest(url, {
            method: 'PUT',
            body: JSON.stringify(settings)
        });
    }

    // Reset settings to default
    async resetSettings() {
        const url = this.buildURL(ECHOAL_CONFIG.ENDPOINTS.SETTINGS_RESET);
        return this.makeRequest(url, { method: 'POST' });
    }

    // Get available themes
    async getAvailableThemes() {
        const url = this.buildURL(ECHOAL_CONFIG.ENDPOINTS.THEMES);
        return this.makeRequest(url);
    }

    // Get available languages
    async getAvailableLanguages() {
        const url = this.buildURL(ECHOAL_CONFIG.ENDPOINTS.LANGUAGES);
        return this.makeRequest(url);
    }

    // Get available AI models
    async getAvailableAIModels() {
        const url = this.buildURL(ECHOAL_CONFIG.ENDPOINTS.AI_MODELS);
        return this.makeRequest(url);
    }

    // Health check
    async healthCheck() {
        const url = this.buildURL(ECHOAL_CONFIG.ENDPOINTS.HEALTH);
        return this.makeRequest(url);
    }
}

// Usage example for your Vercel frontend
const api = new ECHOALProductionAPI();

// Example: Initialize your frontend with production API
async function initializeECHOAL() {
    try {
        // Check if backend is available
        const health = await api.healthCheck();
        console.log('✅ Backend connected:', health);
        
        // Load settings
        const settings = await api.getSettings();
        console.log('⚙️ Settings loaded:', settings);
        
        // Load conversations
        const conversations = await api.getConversations();
        console.log('💬 Conversations loaded:', conversations);
        
        return { health, settings, conversations };
    } catch (error) {
        console.error('❌ Failed to initialize ECHOAL:', error);
        throw error;
    }
}

// Export for use in your frontend
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ECHOALProductionAPI, ECHOAL_CONFIG, initializeECHOAL };
}

// For browser usage
if (typeof window !== 'undefined') {
    window.ECHOALProductionAPI = ECHOALProductionAPI;
    window.ECHOAL_CONFIG = ECHOAL_CONFIG;
    window.initializeECHOAL = initializeECHOAL;
}
