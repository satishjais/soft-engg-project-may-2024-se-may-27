<template>
  <NavBar />
  <router-view />
  <!-- <footer class="footer">
    <div class="container">
      <p>&copy; 2024 Team 27 <em>(Software Engineering)</em>. All rights reserved.</p>
    </div>
  </footer> -->
</template>

<script>
import NavBar from './components/NavBar.vue';

export default {
  name: 'App',
  components: {
    NavBar,
  },
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.btn-primary {
  background-color: #1d0808;
}

.btn-secondary {
  background-color: #F5F5F5;
}

.btn-outline-primary {
  color: #000000;
  border-color: #140707;
}

.footer {
  background-color: #f8f9fa;
  padding: 10px 0;
  text-align: center;
  position: fixed;
  bottom: 0;
  width: 100%;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.header {
  background-color: #fff;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #ddd;
}

.logo {
  height: 40px;
}

.user-info {
  font-size: 14px;
  color: #666;
}

.main-container {
  display: flex;
  flex-grow: 1;
  overflow: hidden;
}

.content-wrapper {
  display: flex;
  flex-grow: 1;
  overflow: hidden;
  text-align: left;
}

.course-sidebar {
  width: 300px;
  background-color: #f7f7f7;
  padding: 6px;
  overflow-y: auto;
}

.sidebar-item {
  margin-bottom: 10px;
}

.sidebar-item h2 {
  cursor: pointer;
  font-size: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #e0e0e0;
}

.toggle-icon {
  font-size: 12px;
}

.sidebar-item ul {
  list-style-type: none;
}

.sidebar-item ul li a {
  display: block;
  padding: 8px 10px;
  text-decoration: none;
  color: #333;
}

.sidebar-item ul li a.active {
  background-color: #ddd;
  font-weight: bold;
}

.content {
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto;
}

.content h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.rating {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.stars {
  color: #f8ce0b;
  font-size: 20px;
}

.rating-text {
  margin-left: 5px;
  color: #666;
}

.submit-review {
  margin-left: 10px;
  color: #1890ff;
  text-decoration: none;
}

.content p {
  margin-bottom: 15px;
  line-height: 1.6;
}

.content a {
  color: #1890ff;
  text-decoration: none;
}

.collapse-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
}

.sidebar-item.open .collapse-content {
  max-height: 1000px; /* Adjust this value based on your content */
}
</style>
