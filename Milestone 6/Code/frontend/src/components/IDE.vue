<template>
  <div class="container">
    <div class="editor-container">
      <div id="editor"></div>
    </div>
    <div class="output-container">
      <button @click="submitCode" class="run-button">Run Code</button>
      <pre class="output">{{ formattedOutput }}</pre>
    </div>
  </div>
</template>

<script>
import ace from "ace-builds/src-noconflict/ace";
import "ace-builds/src-noconflict/theme-monokai";
import "ace-builds/src-noconflict/mode-python";

export default {
  name: "IDEComp",
  data() {
    return {
      editor: null,
      output: "",
    };
  },
  mounted() {
    this.editor = ace.edit("editor");
    this.editor.setTheme("ace/theme/monokai");
    this.editor.session.setMode("ace/mode/python");
    this.editor.setOptions({
      // fontFamily: "monospace",
      fontSize: "20pt",
    });
  },
  computed: {
    formattedOutput() {
      // Preserve formatting with HTML entities
      return this.output
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\n/g, "\n") // Ensure new lines are preserved
        .replace(/ /g, " "); // Preserve spaces
    },
  },
  methods: {
    async submitCode() {
      const code = this.editor.getValue();
      try {
        const response = await fetch("http://localhost:2000/execute", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ code }),
        });
        const result = await response.json();
        this.output = result.output;
      } catch (error) {
        console.error("Error:", error);
        this.output = "Error executing code";
      }
    },
  },
};
</script>

<style>
.container {
  display: flex;
  height: 100vh;
  padding: 20px;
}

.editor-container {
  flex: 3;
  display: flex;
  flex-direction: column;
}

#editor {
  height: calc(100vh - 60px); /* Adjust based on button height */
  width: 100%;
  border: 1px solid #ddd;
  /*font-size: 22px;*/
  font-family: "Courier New", monospace;
  
}

.output-container {
  flex: 1;
  margin-left: 20px;
  display: flex;
  flex-direction: column;
}

.run-button {
  align-self: flex-start;
  margin-bottom: 10px;
}

.output {
  border: 1px solid #ddd;
  padding: 10px;
  background-color: #f5f5f5;
  height: calc(100vh - 60px); /* Adjust based on button height */
  overflow-y: auto;
  font-family: "Courier New", monospace; /* Use monospaced font */
  white-space: pre; /* Preserve whitespace and formatting */
  text-align: left; /* Ensure left alignment */
  margin: 0; /* Remove default margins */
}
</style>
