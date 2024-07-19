<template>
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-md-6 col-lg-4">
          <div class="card shadow">
            <div class="card-body">
              <h2 class="card-title text-center mb-4">Login</h2>
              <form @submit.prevent="login" class="needs-validation" novalidate>
                <div class="mb-3">
                  <label for="username" class="form-label">Username:</label>
                  <input v-model="username" type="text" id="username" class="form-control" required>
                  <div class="invalid-feedback">Please enter your username.</div>
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password:</label>
                  <input v-model="password" type="password" id="password" class="form-control" required>
                  <div class="invalid-feedback">Please enter your password.</div>
                </div>
                <div class="d-grid">
                  <button type="submit" class="btn btn-primary rounded-pill">Login</button>
                </div>
              </form>
              <div class="text-center mt-3">
                <p>
                  Don't have an account?
                  <router-link to="/RegisterUser" class="link-primary">Register</router-link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  
  <script>
//   import { jwtDecode } from 'jwt-decode'; // Named import for jwtDecode
  
  export default {
    name: 'LoginPage',
    data() {
      return {
        username: '',
        password: ''
      };
    },
    // methods: {
    //   async login() {
    //     try {
    //       const response = await fetch('http://localhost:5000/login', {
    //         method: 'POST',
    //         headers: {
    //           'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({
    //           username: this.username,
    //           password: this.password
    //         })
    //       });
  
    //       if (response.ok) { // Login successful
    //         const data = await response.json();
    //         console.log('Login successful!');
    //         this.$router.push('/');
  
    //         const decodedToken = jwtDecode(data.access_token); // Use jwtDecode directly
    //         localStorage.setItem('access_token', data.access_token);
    //         console.log(decodedToken);
  
    //         // Optionally, perform actions on successful login (e.g., store user info in Vuex)
    //       } else {
    //         const errorData = await response.json();
    //         throw new Error(errorData.message || 'Login failed'); // Handle failed login with error message
    //       }
    //     } catch (error) {
    //       console.error('An error occurred during login:', error.message);
    //       // Display an error message to the user
    //     }
    //   }
    // }
  };
  </script>
  
  <style scoped>
  .form-control {
    border-radius: 0.5rem;
  }
  .card {
    border-radius: 1rem;
  }
  .btn-primary {
    background-color: #007bff;
    border-color: #007bff;
  }
  .btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
  }
  .link-primary {
    color: #007bff;
  }
  </style>
  