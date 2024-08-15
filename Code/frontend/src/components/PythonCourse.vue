<template>
    <div id="app">
      <HeaderFile />
      <div class="main-container">
        <div class="content-wrapper">
          <CourseSidebar :activeSection="activeSection" :setActiveSection="setActiveSection" />
          
          <main class="content">
            <div v-if="activeSection === 'aboutCourse'">
              <CourseIntroduction />
            </div>
            <div v-if="activeSection === 'learningStrategy'">
              <h2>Learning Strategy</h2>
              <p>Details about the learning strategy go here...</p>
            </div>
            <div v-if="activeSection === 'submitAssignment'">
              <h2>How to submit a programming assignment</h2>
              <p>Instructions on how to submit a programming assignment go here...</p>
            </div>
            <div v-if="activeSection === 'generalInstructions'">
              <h2>General Instructions</h2>
              <p>General instructions for the course go here...</p>
            </div>
            <div v-if="activeSection === 'W1L1Content'">
              <W1L1Content />
            </div>
            
          </main>
        </div>
      </div> 
    </div>
  </template>
  

<script>
import HeaderFile from './HeaderFile.vue';
import CourseSidebar from './CourseSidebar.vue';
import CourseIntroduction from './Week0/CourseIntroduction.vue';
import W1L1Content from './Week1/W1L1Content.vue';

export default {
  name: "CoursePage",
  components: {
    HeaderFile,
    CourseSidebar,
    CourseIntroduction,
    W1L1Content,
  },
  data() {
    return {
      activeSection: 'aboutCourse',
    };
  },
  methods: {
    setActiveSection(section) {
      this.activeSection = section;
    },
    
  },
};
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
  }
  
  #app {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
  
  .header {
    background-color: #fff;
    padding: 10px 20px;
    display: flex;
    align-items: left;
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
    width: 250px;
    background-color: #f7f7f7;
    padding: 20px;
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
