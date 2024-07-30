<template>
    <div class="video-chat">
      <h1>Python: List and Sets</h1>
      <div class="video-container">
        <iframe 
            width="853" 
            height="480" 
            src="https://www.youtube.com/embed/WQNxG2B85rc" 
            title="Lists and Sets" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            referrerpolicy="strict-origin-when-cross-origin" 
            allowfullscreen>
        </iframe>
      </div>
      <select v-model="currentTheme" @change="changeTheme" class="theme">
        <option value="github">GitHub</option>
        <option value="monokai-sublime">Monokai Sublime</option>
        <option value="atom-one-dark">Atom One Dark</option>
      </select>
      <div class="chat-interface">
        <textarea 
          v-model="userInput" 
          @keyup.enter="sendQuery" 
          placeholder="Ask a question about the video..." 
        ></textarea>
        <button @click="sendQuery" :disabled="isLoading">Send</button>
      </div>
      <div class="response" v-if="response">
        <h4>Response:</h4>
        <div v-html="formattedResponse"></div>
      </div>
      <div v-if="isLoading" class="loading">Loading...</div>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import hljs from 'highlight.js';
  import 'highlight.js/styles/github.css';
  import 'highlight.js/styles/monokai-sublime.css';
  import 'highlight.js/styles/atom-one-dark.css';
  
  export default {
    name: 'VideoChat',
    data() {
      return {
        userInput: '',
        response: '',
        isLoading: false,
        error: null,
        currentTheme: 'atom-one-dark',
      }
    },
    computed: {
      formattedResponse() {
        if (!this.response) return '';
        return this.formatText(this.response);
      }
    },
    methods: {
        changeTheme() {
            document.body.className = this.currentTheme;
        },
      async sendQuery() {
        if (!this.userInput.trim()) return;
        
        this.isLoading = true;
        this.error = null;
        this.response = '';
  
        try {
          const result = await axios.post('http://localhost:2000/videochat', {
            message: this.userInput
          });
          this.response = result.data.response;
        } catch (error) {
          console.error('Error:', error);
          this.error = 'An error occurred while fetching the response.';
        } finally {
          this.isLoading = false;
        }
      },
      formatText(text) {
        // Split the text into lines
        const lines = text.split('\n');
        let formattedText = '';
        let inCodeBlock = false;
        let codeBlockContent = '';
        let language = '';
  
        for (const line of lines) {
          if (line.startsWith('```')) {
            if (inCodeBlock) {
              // End of code block
              const highlightedCode = hljs.highlightAuto(codeBlockContent, [language]).value;
              formattedText += `<pre><code class="hljs ${language}">${highlightedCode}</code></pre>`;
              inCodeBlock = false;
              codeBlockContent = '';
              language = '';
            } else {
              // Start of code block
              inCodeBlock = true;
              language = line.slice(3).trim(); // Get the language specified after ```
            }
          } else if (inCodeBlock) {
            codeBlockContent += line + '\n';
          } else {
            // Regular text
            formattedText += this.formatLine(line) + '<br>';
          }
        }
  
        return formattedText;
      },
      formatLine(line) {
        // Basic formatting for non-code text
        line = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); // Bold
        line = line.replace(/\*(.*?)\*/g, '<em>$1</em>'); // Italic
        line = line.replace(/`(.*?)`/g, '<code>$1</code>'); // Inline code
        return line;
      }
    }
  }
  </script>
  
  <style>
  .video-chat {
    max-width: 855px;
    margin: 0 auto;
    padding: 20px;
    text-align: left;
  }
  
  .chat-interface {
    display: flex;
    align-items: flex-start;
    margin-bottom: 20px;
    
  }
  
  textarea {
    flex-grow: 1;
    padding: 10px;
    font-size: 16px;
    border-radius:15px;
    margin-right: 2px;
    resize: vertical;
    overflow-y: auto;
  }
  
  button {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 15px;
    cursor: pointer;
    flex-shrink: 0;
  }
  
  button:disabled {
    background-color: #cccccc;
  }
  
  .response, .loading, .error {
    margin-top: 20px;
  }
  
  .error {
    color: red;
  }
  
  pre {
    background-color: #f4f4f4;
    padding: 0px;
    overflow-x: auto;
    border-radius: 5px;
  }
  
  code {
    font-family: 'Courier New', Courier, monospace;
  }

  .theme {
    border-radius: 12px;
    max-width: 400px;
    margin-bottom: 2px;
  }
  
  </style>