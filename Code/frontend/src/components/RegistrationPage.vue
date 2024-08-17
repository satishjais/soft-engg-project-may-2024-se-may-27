<template>
  <div class="centred-item">
    <h1 align="center">Register</h1>
    <div v-if="error" class="alert alert-warning alert-dismissible fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close" @click="closeAlert" aria-label="Close"></button>
    </div>
    <form class="auth-form form-group" @submit.prevent="register">
      <input v-model="formData.name" type="text" class="form-control" placeholder="Name" required>
      <br>
      <input v-model="formData.username" type="text" class="form-control" placeholder="Username" required>
      <br>
      <input v-model="formData.email" type="email" class="form-control" placeholder="Email" required>
      <br>
      <input v-model="formData.password" type="password" class="form-control" placeholder="Password" required>
      <br>
      <input v-model="formData.confpass" type="password" class="form-control" placeholder="Confirm Password" required>
      <br>
      <input v-model="formData.mob" type="text" class="form-control" placeholder="Mobile" required>
      <br>
      <div align="center">
        <button type="submit" class="btn btn-primary" style="background-color: #062041;">Register</button>
        <br><br>
        <p>Already have an account? <router-link to="/login">Login here</router-link></p>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        username: '',
        password: '',
        confpass: '',
        email: '',
        mob: '',
        name: ''
      },
      error: null,
    };
  },
  methods: {
    async register() {
      try {
        const response = await fetch('http://127.0.0.1:2000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.formData),
        });

        const data = await response.json();

        if (response.status === 200) {
          this.$router.push('/login');
          alert("Registration Successful");
        } else {
          this.error = data.error || 'An error occurred while registering.';
        }
      } catch (error) {
        console.error('Error:', error);
        this.error = 'An error occurred while registering.';
      }
    },
    closeAlert() {
      this.error = null;
    },
  },
};
</script>

<style>
/* Adjust styles as needed */
.btn-close {
  position: right;
}
</style>


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

.btn-close {
  position: right;
}

</style>
