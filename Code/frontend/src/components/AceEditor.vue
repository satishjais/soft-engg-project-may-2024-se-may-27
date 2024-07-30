<template>
    <div align="center">
      <div id="editor" style="height: 500px; width: 50%;"></div>
      <button @click="submitCode">Run Code</button>
      <pre>{{ output }}</pre>
    </div>
  </template>
  
  <script>
  import ace from 'ace-builds/src-noconflict/ace';
  import 'ace-builds/src-noconflict/theme-monokai';
  import 'ace-builds/src-noconflict/mode-python';
  
  export default {
    data() {
      return {
        editor: null,
        output: ''
      }
    },
    mounted() {
      this.editor = ace.edit("editor");
      this.editor.setTheme("ace/theme/monokai");
      this.editor.session.setMode("ace/mode/python");
    },
    methods: {
      async submitCode() {
        const code = this.editor.getValue();
        // console.log(code);
        try {
          const response = await fetch('http://localhost:2000/execute', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
          });
          const result = await response.json();
          this.output = result.output;
        } catch (error) {
          console.error('Error:', error);
          this.output = 'Error executing code';
        }
      }
    }
  }
  </script>
  
  <style>
  #editor {
    border: 1px solid #ddd;
  }
  </style>
  