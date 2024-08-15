<template>
    <div id="app">
        <Header />
      <!-- <header class="header">
        <img
          src="https://seek.onlinedegree.iitm.ac.in/assets/img/logos/iitm-logo@3x.png"
          alt="IIT Madras Logo"
          class="logo"
        />
        <h1>September 2024: Introduction to Programming in Python</h1>
        <div class="user-info">21f1002870@ds.study.iitm.ac.in →</div>
      </header> -->
      <div class="main-container">
        <div class="content-wrapper">
          <aside class="course-sidebar">
            <!-- Intro -->
            <div class="sidebar-item" :class="{ open: isOpen('courseIntroduction') }">
              <h2 @click="toggleSection('courseIntroduction')">
                Course Introduction
                <span class="toggle-icon">{{
                  isOpen("courseIntroduction") ? "▼" : "▶"
                }}</span>
              </h2>
              <ul ref="courseIntroduction" class="collapse-content">
                <li>
                  <a href="#" @click.prevent="setActiveSection('aboutCourse')" class="{ active: isActiveSection('aboutCourse') }">About the Course</a>
                </li>
                <li>
                  <a href="#" @click.prevent="setActiveSection('learningStrategy')" class="{ active: isActiveSection('learningStrategy') }">Learning Strategy</a>
                </li>
                <li>
                  <a href="#" @click.prevent="setActiveSection('submitAssignment')" class="{ active: isActiveSection('submitAssignment') }">How to submit a programming assignment</a>
                </li>
                <li>
                  <a href="#" @click.prevent="setActiveSection('generalInstructions')" class="{ active: isActiveSection('generalInstructions') }">General Instructions</a>
                </li>
              </ul>
            </div>
         
          <!-- Week 1 -->
          <div class="sidebar-item" :class="{ open: isOpen('week1') }">
            <h2 @click="toggleSection('week1')">
              Week 1
              <span class="toggle-icon">{{
                isOpen("week1") ? "▼" : "▶"
              }}</span>
            </h2>
            <ul ref="week1" class="collapse-content">
                <li>
                    <a href="#" @click.prevent="setActiveSection('W1L1Content')" :class="{ active: isActiveSection('W1L1Content') }">L1.1: Introduction</a>
                    <a href="#" @click.prevent="setActiveSection('W1L2Content')" :class="{ active: isActiveSection('W1L2Content') }">L1.2: Introduction to Replit</a>
                    <a href="#" @click.prevent="setActiveSection('W1L3Content')" :class="{ active: isActiveSection('W1L3Content') }">L1.3: More on Replit, print, and Common Mistakes</a>
                    <a href="#" @click.prevent="setActiveSection('W1L4Content')" :class="{ active: isActiveSection('W1L4Content') }">L1.4: A Quick Introduction to Variables</a>
                    <a href="#" @click.prevent="setActiveSection('W1L5Content')" :class="{ active: isActiveSection('W1L5Content') }">L1.5: Variables and Input Statement</a>
                </li>
            </ul>
          </div>

          <!-- Week 2 -->
          <div class="sidebar-item" :class="{ open: isOpen('week2') }">
            <h2 @click="toggleSection('week2')">
              Week 2
              <span class="toggle-icon">{{
                isOpen("week2") ? "▼" : "▶"
              }}</span>
            </h2>
            <ul ref="week2" class="collapse-content">
              <li>
                <a href="#" @click.prevent="setActiveSection('W1L1Content')" :class="{ active: isActiveSection('W1L1Content') }">L1.1: Introduction</a>
                <a href="#" @click.prevent="setActiveSection('W1L2Content')" :class="{ active: isActiveSection('W1L2Content') }">L1.2: Introduction to Replit</a>
                <a href="#" @click.prevent="setActiveSection('W1L3Content')" :class="{ active: isActiveSection('W1L3Content') }">L1.3: More on Replit, print, and Common Mistakes</a>
                <a href="#" @click.prevent="setActiveSection('W1L4Content')" :class="{ active: isActiveSection('W1L4Content') }">L1.4: A Quick Introduction to Variables</a>
                <a href="#" @click.prevent="setActiveSection('W1L5Content')" :class="{ active: isActiveSection('W1L5Content') }">L1.5: Variables and Input Statement</a>
              </li>
            </ul>
          </div>
        </aside>

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
          <div v-if="activeSection === 'W1L2Content'">
            <lecture2Content />
          </div>
          <div v-if="activeSection === 'W1L3Content'">
            <lecture3Content />
          </div>
          <div v-if="activeSection === 'W1L4Content'">
            <lecture4Content />
          </div>
          <div v-if="activeSection === 'W1L5Content'">
            <lecture5Content />
          </div>
        </main>
      </div>
    </div>
  </div>
</template>
  

<script>
import Header from './Header.vue';
import CourseSidebar from './CourseSidebar.vue';
import CourseIntroduction from './Week0/CourseIntroduction.vue';
import W1L1Content from './Week1/W1L1Content.vue';

export default {
  name: "CoursePage",
  components: {
    Header,
    CourseSidebar,
    CourseIntroduction,
    W1L1Content,
  },
  data() {
    // return {
    //   openSections: {
    //     courseIntroduction: true,
    //     Week1:false,
    //   },
    //   activeSection: 'aboutCourse',
    // };
    return {
      activeSection: 'aboutCourse',
    };
  },
  methods: {
    // toggleSection(section) {
    //   this.openSections[section] = !this.isOpen(section);
    //   this.$nextTick(() => {
    //     this.animateCollapse(section);
    //   });
    // },
    // isOpen(section) {
    //   return this.openSections[section];
    // },
    // animateCollapse(section) {
    //   const content = this.$refs[section];
    //   if (content) {
    //     if (this.isOpen(section)) {
    //       content.style.maxHeight = content.scrollHeight + "px";
    //     } else {
    //       content.style.maxHeight = null;
    //     }
    //   }
    // },
    setActiveSection(section) {
      this.activeSection = section;
    },
    // isActiveSection(section) {
    //   return this.activeSection === section;
    // },
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
