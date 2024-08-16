<template> 
  <div class="container-fluid bodyplacer">
    <div class="centred-item text-center">
      <h1 class="display-1 fw-bold">Welcome to <h1 class="display-1 font-monospace">WonCourse</h1></h1>
      <br />
      <h4 class="fst-italic">The Ultimate Classroom for One Course</h4>
      <br />
      <div class="mt-4">
        <button class="btn btn-primary btn-lg mx-3" @click="goToLogin">
          Login
        </button>
        <button class="btn btn-primary btn-lg mx-3" @click="goToRegister">
          Register
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  methods: {
    goToRegister() {
      this.$router.push('/register');
    },
    goToLogin() {
      this.$router.push('/login');
    }
  }
}
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

.btn-close {
  position: right;
}
.button-container {
  display: flex;
  justify-content: center;
  gap: 15px; /* Adjust the gap between buttons */
  margin-top: 20px;
}
</style>