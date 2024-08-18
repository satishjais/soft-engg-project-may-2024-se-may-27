<template>
  <header class="header">
    <h5>September 2024: Introduction to Programming in Python</h5>
    <button @click="openAdminModal" class="logout-button">Support</button>
    <button @click="logout" class="logout-button">Logout</button>

    <!-- Gajaa - Admin Support -->
    <div class="sidebar-item" :class="{ open: isOpen('adminbot') }">
        <h2 @click="toggleSection('adminbot')">
          Gajaa - Admin Support
          <span class="toggle-icon">{{ isOpen("adminbot") ? "▼" : "▶" }}</span>
        </h2>
        <ul ref="adminbot" class="collapse-content">
          <li>
            <a href="#" @click.prevent="openAdminModal">Chat with Admin Support</a>
          </li>
        </ul>
      </div>

    <!-- Admin Modal HTML -->
    <div
      class="modal fade"
      id="adminModal"
      tabindex="-1"
      aria-labelledby="adminModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="adminModalLabel">Gajaa - Admin Support</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <!-- Admin Support Content Here -->
            <div class="admin-container">
              <textarea
                v-model="adminInput"
                @keyup.enter="sendAdminQuery"
                placeholder="Ask an admin question..."
              ></textarea>
              <button @click="sendAdminQuery" :disabled="isAdminLoading">Send</button>
              <div v-if="adminResponse" class="admin-response">
                <h4>Response:</h4>
                <div v-html="adminResponse"></div>
              </div>
              <div v-if="isAdminLoading" class="admin-loading">Loading...</div>
              <div v-if="adminError" class="admin-error">{{ adminError }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { Modal } from "bootstrap";
import hljs from "highlight.js";
import "highlight.js/styles/github.css";
import "highlight.js/styles/monokai-sublime.css";
import "highlight.js/styles/atom-one-dark.css";
export default {
  name: "HeaderFile",
  data() {
    return {
      openSections: {
        chatContent: "",
        chatLoading: false,
      },
      // Admin Modal Data
      adminInput: "",
      adminResponse: "",
      adminError: "",
      isAdminLoading: false,
    };
  },
  methods: {
    logout() {
      // Make an API call to the logout endpoint
      fetch('http://127.0.0.1:2000/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.code === 200) {
          console.log('Logout successful');
          // Clear the token from localStorage
          localStorage.removeItem('token');
          // Redirect to login page using Vue Router
          this.$router.push('/login');
        } else {
          alert('Logout failed: ' + data.message);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    },
    async openAdminModal() {
      this.chatLoading = true;
      this.isAdminLoading = false;
      this.adminError = null;
      this.adminResponse = "";
      this.adminInput = "";

      const adminModalElement = document.getElementById("adminModal");
      if (adminModalElement) {
        const myModal = new Modal(adminModalElement, {
          backdrop: "static",
          keyboard: false,
          focus: true,
          scrollable: true,
        });
        myModal.show();
      }
    },

    async sendAdminQuery() {
      if (!this.adminInput.trim()) return;
      this.isAdminLoading = true;
      this.adminError = null;
      this.adminResponse = "";
      try {
        const result = await fetch("http://127.0.0.1:2000/supportchat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: this.adminInput,
          }),
        });
        const data = await result.json();
        this.adminResponse = data.response;
      } catch (error) {
        this.adminError = "An error occurred while fetching the response.";
      } finally {
        this.isAdminLoading = false;
      }
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
  }
};
</script>

<style scoped>
.logout-button {
  background-color: #ccc;
  color: #333;
  font-size: 12px;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #bbb;
}
.hljs {
    background: none;
  }


  .admin-container textarea {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
  }
  
  .admin-container button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .admin-response {
    margin-top: 20px;
    padding: 10px;
    background-color: #f1f1f1;
    border-radius: 5px;
  }
  
  .admin-loading {
    color: gray;
  }
  
  .admin-error {
    color: red;
  }
</style>
