<template>
    <div class="registration">
      <h1>Register</h1>
      <form @submit.prevent="register">
        <div>
          <label for="name">Name:</label>
          <input type="text" v-model="formData.name" required />
        </div>
        <div>
          <label for="username">Username:</label>
          <input type="text" v-model="formData.username" required />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" v-model="formData.password" required />
        </div>
        <div>
          <label for="email">Email:</label>
          <input type="email" v-model="formData.email" required />
        </div>
        <div>
          <label for="mob">Mobile:</label>
          <input type="text" v-model="formData.mob" required />
        </div>
        <!-- <div>
          <label for="courses">Courses:</label>
          <input type="text" v-model="formData.courses" />
        </div> -->
        <button type="submit">Register</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        formData: {
          name: '',
          username: '',
          password: '',
          email: '',
          mob: '',
        //   courses: ''
        },
        message: ''
      };
    },
    methods: {
      async register() {
        try {
          const response = await axios.post('/register', this.formData);
          if (response.data.code === 201) {
            this.message = 'User created successfully';
            this.$router.push('/login'); // Redirect to login page
          } else {
            this.message = response.data.error;
          }
        } catch (error) {
          this.message = 'An error occurred: ' + (error.response?.data?.error || error.message);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .registration {
    max-width: 400px;
    margin: 0 auto;
    padding: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .registration h1 {
    text-align: center;
  }
  
  .registration form {
    display: flex;
    flex-direction: column;
  }
  
  .registration div {
    margin-bottom: 1rem;
  }
  
  .registration label {
    margin-bottom: 0.5rem;
  }
  
  .registration input {
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .registration button {
    padding: 0.5rem;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .registration button:hover {
    background-color: #218838;
  }
  
  .registration p {
    text-align: center;
    color: red;
  }
  </style>
  