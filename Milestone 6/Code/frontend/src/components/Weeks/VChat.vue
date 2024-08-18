<template>
  <div class="chat-container">
    <div class="chat-interface">
        <textarea
        v-model="userInput"
        @keyup.enter="sendQuery"
        placeholder="Ask a question about the video..."
        ></textarea>
        <div class="div">
          <select v-model="currentTheme" @change="changeTheme" class="theme">
            <option value="github">GitHub</option>
            <option value="monokai-sublime">Monokai Sublime</option>
            <option value="atom-one-dark">Atom One Dark</option>
          </select>
        </div>
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
import hljs from "highlight.js";
import "highlight.js/styles/github.css";
import "highlight.js/styles/monokai-sublime.css";
import "highlight.js/styles/atom-one-dark.css";

export default {
  data() {
    return {
      userInput: "",
      response: "",
      isLoading: false,
      error: null,
      currentTheme: "atom-one-dark",
    };
  },
  
  computed: {
    formattedResponse() {
      if (!this.response) return "";
      return this.formatText(this.response);
    },
  },
  methods: {
    async sendQuery() {
      console.log("SEND BUTTON CLICKED!!");
      if (!this.userInput.trim()) return;

      this.isLoading = true;
      this.error = null;
      this.response = "";
      console.log("this.input:", this.userInput);
      try {
        const result = await fetch("http://127.0.0.1:2000/videochat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: this.userInput,
          }),
        });
        const data = await result.json();
        console.log("RESULTS:", data);
        this.response = data.response;
        console.log("this.response", this.response);
      } catch (error) {
        console.error("Error:", error);
        this.error = "An error occurred while fetching the response.";
      } finally {
        this.isLoading = false;
      }
    },

    changeTheme() {
      document.body.className = this.currentTheme;
    },

    formatText(text) {
      // Split the text into lines
      const lines = text.split("\n");
      let formattedText = "";
      let inCodeBlock = false;
      let codeBlockContent = "";
      let language = "";

      for (const line of lines) {
        if (line.startsWith("```")) {
          if (inCodeBlock) {
            // End of code block
            const highlightedCode = hljs.highlightAuto(codeBlockContent, [
              language,
            ]).value;
            formattedText += `<pre><code class="hljs ${language}">${highlightedCode}</code></pre>`;
            inCodeBlock = false;
            codeBlockContent = "";
            language = "";
          } else {
            // Start of code block
            inCodeBlock = true;
            language = line.slice(3).trim(); // Get the language specified after ```
          }
        } else if (inCodeBlock) {
          codeBlockContent += line + "\n";
        } else {
          // Regular text
          formattedText += this.formatLine(line) + "<br>";
        }
      }

      return formattedText;
    },
    formatLine(line) {
      // Basic formatting for non-code text
      line = line.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>"); // Bold
      line = line.replace(/\*(.*?)\*/g, "<em>$1</em>"); // Italic
      line = line.replace(/`(.*?)`/g, "<code>$1</code>"); // Inline code
      return line;
    },

  },
};
</script>

<style>
.video-chat {
  display: flex;
  max-width: 1200px; /* Adjusted width to accommodate both video and chat */
  margin: 0 auto;
  padding: 10px;
  text-align: left;
}

.content-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.video-container {
  flex: 1; /* Let the video take up more space */
}

.chat-container {

  width: 300px; /* Fixed width for the chat container */
  margin-left: 20px; /* Space between video and chat */
  overflow-y: auto;
}

/* Custom scrollbar styles */
.chat-container::-webkit-scrollbar {
  width: 1px; /* Width of the scrollbar */
}

.chat-container::-webkit-scrollbar-track {
  background: transparent; /* Track color */
  border-radius: 20px; /* Rounded edges */
}

.chat-container::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  border: 2px solid transparent;
  background-clip: padding-box;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.3);
}

/* Firefox scrollbar styles */
.chat-container {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

.chat-interface {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  margin-bottom: 20px;
}

textarea {
  padding: 10px;
  font-size: 16px;
  border-radius: 15px;
  margin-bottom: 10px;
  resize: vertical;
  overflow-y: auto;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 15px;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
}

.response,
.loading,
.error {
  margin-top: 0px;
  /* overflow-x: scroll; */
  overflow-y: scroll;
  height: 50vh;
  /* width: 40vh; */
  /* text-align: justify;*/
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
  font-family: "Courier New", Courier, monospace;
}

.theme {
  border-radius: 12px;
  max-width: 380px;
  margin-bottom: 7px;
  padding: 5px;
}
</style>
