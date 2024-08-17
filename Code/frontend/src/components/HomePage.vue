<template>
  <div class="container-fluid bodyplacer">
    <div class="row full-height no-scroll">
      <!-- Text on the left (70%) -->
      <div class="col-md-8 col-sm-12 text-container text-left">
        <div class="text-content" style="margin-left: 2%;">
          <h1 class="display-1 fw-bold font-bold">
            Welcome to
            <span class="display-1">WonCourse</span>
          </h1>
          <h4 class="fst" style="margin: 1%;">The Ultimate Classroom for One Course</h4>
          <div class="mt-4 button-container" style="padding-top: 5%;">
            <button class="btn btn-primary custom-btn" style="margin-left: 1%;" @click="goToLogin">
              Sign In
            </button>
          </div>
        </div>
      </div>

      <!-- Image on the right (30%) -->
      <div class="col-md-4 col-sm-12 image-container">
        <img src="@/assets/image.jpg" alt="Welcome Image" class="welcome-image" />
      </div>
    </div>

    <!-- Moving footer -->
    <div class="moving-footer">
      <div class="scrolling-text">
        © 2024 Software Engineering Project Team 27 | May 2024 Term. All rights reserved.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  methods: {
    goToLogin() {
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.bodyplacer {
  height: 100vh; /* Full height of the viewport */
  padding: 0;
  margin: 0;
  overflow: hidden; /* Prevent unnecessary scrolling */
}

.full-height {
  height: 100%;
  display: flex;
}

.image-container {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.welcome-image {
  width: 100%;
  height: 100vh; /* Full height of the viewport */
  object-fit: cover; /* Crop the image to cover the full container */
}

.text-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
  padding: 20px;
}

.text-content {
  width: 100%;
}

.custom-btn {
  font-size: 1.25rem; /* Slightly smaller button */
  padding: 8px 16px; /* Adjust padding for a smaller button */
  margin-left: 0; /* Align button with the starting position of the text */
}

.button-container {
  margin-top: 20px;
  padding: 0;
}

.moving-footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  overflow: hidden;
  background-color: #333; /* Dark background for contrast */
  color: #fff;
  font-size: 0.9rem;
  padding: 0.2%;
}

.scrolling-text {
  display: inline-block;
  white-space: nowrap;
  padding-left: 100%; /* Start off-screen */
  animation: scrollText 15s linear infinite; /* Adjust duration as needed */
}

@keyframes scrollText {
  0% {
    transform: translateX(0%);
  }
  100% {
    transform: translateX(-100%);
  }
}

@media (max-width: 768px) {
  .image-container, .text-container {
    flex-basis: 100%;
    text-align: center;
    align-items: center;
  }

  .full-height {
    flex-direction: column;
  }

  .welcome-image {
    height: 50vh; /* Adjust image height for smaller screens */
  }
}
</style>
