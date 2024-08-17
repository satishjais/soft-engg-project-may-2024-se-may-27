<template>
  <div class="centred-item">
    <div v-if="error" class="alert alert-warning alert-dismissible fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close" @click="closeAlert" aria-label="Close"></button>
    </div>
    <h1 class="text-center">Login</h1>
    <form class="auth-form form-group" @submit.prevent="login">
      <input
        v-model="username"
        type="text"
        class="form-control"
        placeholder="Username"
        required
      />
      <br />
      <input
        v-model="password"
        type="password"
        class="form-control"
        placeholder="Password"
        required
      />
      <br />
      <div class="form-check">
        <input 
          class="form-check-input" 
          type="checkbox" 
          v-model="rememberMe" 
          id="rememberMe" 
        />
        <label class="form-check-label" for="rememberMe">
          Remember Login Info
        </label>
      </div>
      <br />
      <div class="text-center">
        <button
          type="submit"
          class="btn btn-primary"
        >
          Login
        </button>
        <br /><br /><br />
        <p>
          Don't have an account? <router-link to="/register">Register</router-link>
        </p>
        <br><br>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
      error: '',
    };
  },
  methods: {
    async login() {
      if (this.username === '' || this.password === '') {
        this.setError('Please enter both username and password.');
        return;
      }

      console.log('Sending login request:', {
        username: this.username,
        password: this.password,
        rememberMe: this.rememberMe,
      });

      try {
        const response = await fetch('http://127.0.0.1:2000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        const data = await response.json();

        if (response.ok && data.code === 200) {
          // Success case
          console.log('Login successful!', data);
          localStorage.setItem('access_token', data.token);
          localStorage.setItem('user_id', data.user_id);
          console.log(data.token, data.user_id);
          // Check the user's role and redirect accordingly
          if (data.role === 'Admin') {
            this.$router.push(`/dashboard/admin`);
          } else {
            this.$router.push(`/dashboard`);
          }
        } else {
          // Handle errors from the server response
          this.setError(data.message || 'Login failed. Please try again.');
        }
      } catch (error) {
        console.error('An error occurred during login:', error.message);
        this.setError('Login failed: ' + error.message);
      }
    },
    setError(errorMessage) {
      this.error = errorMessage;
    },
    closeAlert() {
      this.error = '';
    },
  },
};
</script>

<style scoped>
.centred-item {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70%;
  background-color: #ffffff1e;
  max-width: 600px;
}

@media (max-width: 768px) {
  .centred-item {
    width: 90%;
  }
}

@media (max-width: 480px) {
  .centred-item {
    width: 100%;
  }
}

.form-check {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.form-check-input {
  margin-right: 10px;
}

.btn-close {
  position: absolute;
  top: 10px;
  right: 10px;
}
</style>
