<template>
  <router-view />
  <AceEditor />
</template>

<script>
import AceEditor from './components/AceEditor.vue'

export default {
  name: 'App',
  components: {
    AceEditor
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
