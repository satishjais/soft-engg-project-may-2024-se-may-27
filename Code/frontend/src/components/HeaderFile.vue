<template>
  <header class="header">
    <h5>September 2024: Introduction to Programming in Python</h5>
    <button @click="logout" class="logout-button">Logout</button>
  </header>
</template>

<script>
export default {
  name: "HeaderFile",
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
    }
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
</style>
