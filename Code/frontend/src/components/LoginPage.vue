<template>
  <div class="container">
    <div class="row justify-content-center align-items-center min-vh-100">
      <div class="col-md-6 col-lg-4">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">Login</h2>
            <form @submit.prevent="login" class="needs-validation" novalidate>
              <div class="mb-3">
                <label for="username" class="form-label">Username:</label>
                <input 
                  v-model="username" 
                  type="text" 
                  id="username" 
                  class="form-control" 
                  required
                >
                <div class="invalid-feedback">Please enter your username.</div>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password:</label>
                <input 
                  v-model="password" 
                  type="password" 
                  id="password" 
                  class="form-control" 
                  required
                >
                <div class="invalid-feedback">Please enter your password.</div>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Login</button>
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
export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      console.log('Sending login request:', {
        username: this.username,
        password: this.password
      });

      try {
        const response = await fetch('http://127.0.0.1:2000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });

        const data = await response.json();

        if (data.code === 200) {
          // Success case
          console.log('Login successful!', data);
          localStorage.setItem('access_token', data.token);
          localStorage.setItem('user_id', data.user_id);
          console.log(data.token, data.user_id);
          const userId = data.user_id; 
          this.$router.push(`/dashboard/${userId}`);
        
        } else {
          // Handling different error codes
          alert('Login failed: ' + data.error);
        }
      } catch (error) {
        console.error('An error occurred during login:', error.message);
        alert('Login failed: ' + error.message); 
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 100%;
  padding: 15px;
  margin: 0 auto;
}

.row {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.card {
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.card-title {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.form-label {
  margin-bottom: 0.5rem;
}

.form-control {
  border-radius: 4px;
  padding: 10px;
  font-size: 1rem;
}

.btn {
  border-radius: 20px;
  padding: 10px 20px;
  font-size: 1rem;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}

.link-primary {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.link-primary:hover {
  color: #0056b3;
  text-decoration: underline;
}

.mt-3 {
  margin-top: 1rem;
}
</style>