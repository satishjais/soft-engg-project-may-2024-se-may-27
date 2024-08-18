<template>
  <div class="div">
    <h4>W1PPA1:</h4>
    Print the first 5 positive integers in ascending order with one number in
    each line.
  </div>
  <div class="container">
    <div class="editor-container">
      <div id="editor"></div>
    </div>
    <div class="output-container">
      <button @click="submitCode" class="run-button">Run Code</button>
      <div v-if="testResults.length">
        <h4>Test Results:</h4>
        <ul>
          <li v-for="(result, index) in testResults" :key="index">
            <strong>Test Case {{ index + 1 }}:</strong>
            <p>Input: {{ result.input }}</p>
            <p>Expected Output: <br>{{ result.expected_output }}</p>
            <p>Actual Output: <br>{{ result.actual_output }}</p>
            <p :style="{ color: result.passed ? 'green' : 'red' }">
              {{ result.passed ? 'Passed' : 'Failed' }}
            </p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import ace from "ace-builds/src-noconflict/ace";
import "ace-builds/src-noconflict/theme-monokai";
import "ace-builds/src-noconflict/mode-python";

export default {
  name: "W1PPA1",
  data() {
    return {
      editor: null,
      output: "",
      testResults: [],
    };
  },
  mounted() {
    this.editor = ace.edit("editor");
    this.editor.setTheme("ace/theme/monokai");
    this.editor.session.setMode("ace/mode/python");
    this.editor.setOptions({
      fontSize: "12pt",
      wrap: true, // Enable line wrapping
      showPrintMargin: false, // Disable the print margin
      highlightActiveLine: true,
      autoScrollEditorIntoView: true, // Ensure the editor scrolls the view as needed
      useWorker: false, // Disable syntax checking to improve performance
    });
  },
  methods: {
    async submitCode() {
      const code = this.editor.getValue();
      const testCases = [
        { input: '', expected_output: '1\n2\n3\n4\n5' },
        // Add more test cases here
      ];

      try {
        const response = await fetch("http://localhost:2000/execute", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ code, test_cases: testCases }),
        });
        const result = await response.json();
        this.output = result.output || ""; // Ensure output is always a string
        this.testResults = result.test_results || []; // Ensure testResults is always an array
      } catch (error) {
        console.error("Error:", error);
        this.output = "Error executing code";
        this.testResults = [];
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
  font-family: "Courier New", monospace;
  border-radius: 15px;
  overflow-wrap: break-word; /* Ensure long words wrap */
}

.run-button {
  align-self: flex-start;
  margin-bottom: 10px;
  width: 265px;
  background-color: rgb(6, 150, 14);
  color: white;
  font-size: 16px;
  border-radius: 15px;
  border-color: white;
  padding: 5px;
}

.output-container {
  flex: 1;
  margin-left: 20px;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  border: 1px solid #ddd;
  padding: 10px;
  background-color: #f5f5f5;
  height: calc(100vh - 60px); /* Adjust based on button height */
  overflow-y: auto;
  font-family: "Courier New", monospace; /* Use monospaced font */
  white-space: pre; /* Preserve whitespace and formatting */
  text-align: left; /* Ensure left alignment */
  margin: 0; /* Remove default margins */
  border-radius: 15px;
}
</style>
