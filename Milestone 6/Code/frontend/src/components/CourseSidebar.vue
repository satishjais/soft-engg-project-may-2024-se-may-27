<template>
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
            <a href="#" @click.prevent="setActiveSection('aboutCourse')" :class="{ active: isActiveSection('aboutCourse') }">About the Course</a>
          </li>
          <li>
            <a href="#" @click.prevent="setActiveSection('learningStrategy')" :class="{ active: isActiveSection('learningStrategy') }">Learning Strategy</a>
          </li>
          <li>
            <a href="#" @click.prevent="setActiveSection('submitAssignment')" :class="{ active: isActiveSection('submitAssignment') }">How to submit a programming assignment</a>
          </li>
          <li>
            <a href="#" @click.prevent="setActiveSection('generalInstructions')" :class="{ active: isActiveSection('generalInstructions') }">General Instructions</a>
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
              <a href="#" @click.prevent="setActiveSection('W1L1Content')" :class="{ active: isActiveSection('W1L1Content') }">L1.1</a>
              <a href="#" @click.prevent="setActiveSection('W1L2Content')" :class="{ active: isActiveSection('W1L2Content') }">L1.2</a>
              <a href="#" @click.prevent="setActiveSection('W1L3Content')" :class="{ active: isActiveSection('W1L3Content') }">L1.3</a>
              <a href="#" @click.prevent="setActiveSection('W1L4Content')" :class="{ active: isActiveSection('W1L4Content') }">L1.4</a>
              <a href="#" @click.prevent="setActiveSection('W1L5Content')" :class="{ active: isActiveSection('W1L5Content') }">L1.5</a>
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
            <a href="#" @click.prevent="setActiveSection('W2L1Content')" :class="{ active: isActiveSection('W2L1Content') }">L2.1</a>
            <a href="#" @click.prevent="setActiveSection('W2L2Content')" :class="{ active: isActiveSection('W2L2Content') }">L2.2</a>
            <a href="#" @click.prevent="setActiveSection('W2L3Content')" :class="{ active: isActiveSection('W2L3Content') }">L2.3</a>
            <a href="#" @click.prevent="setActiveSection('W2L4Content')" :class="{ active: isActiveSection('W2L4Content') }">L2.4</a>
            <a href="#" @click.prevent="setActiveSection('W2L5Content')" :class="{ active: isActiveSection('W2L5Content') }">L2.5</a>
          </li>
        </ul>
      </div>

      <!-- Week 3 -->
      <div class="sidebar-item" :class="{ open: isOpen('week3') }">
        <h2 @click="toggleSection('week3')">
          Week 3
          <span class="toggle-icon">{{
            isOpen("week3") ? "▼" : "▶"
          }}</span>
        </h2>
        <ul ref="week3" class="collapse-content">
          <li>
            <a href="#" @click.prevent="setActiveSection('W3L1Content')" :class="{ active: isActiveSection('W3L1Content') }">L3.1</a>
            <a href="#" @click.prevent="setActiveSection('W3L2Content')" :class="{ active: isActiveSection('W3L2Content') }">L3.2</a>
            <a href="#" @click.prevent="setActiveSection('W3L3Content')" :class="{ active: isActiveSection('W3L3Content') }">L3.3</a>
            <a href="#" @click.prevent="setActiveSection('W3L4Content')" :class="{ active: isActiveSection('W3L4Content') }">L3.4</a>
            <a href="#" @click.prevent="setActiveSection('W3L5Content')" :class="{ active: isActiveSection('W3L5Content') }">L3.5</a>
          </li>
        </ul>
      </div>

      <!-- Week 4 -->
      <div class="sidebar-item" :class="{ open: isOpen('week4') }">
        <h2 @click="toggleSection('week4')">
          Week 4
          <span class="toggle-icon">{{
            isOpen("week4") ? "▼" : "▶"
          }}</span>
        </h2>
        <ul ref="week4" class="collapse-content">
          <li>
            <a href="#" @click.prevent="setActiveSection('W4L1Content')" :class="{ active: isActiveSection('W4L1Content') }">L4.1</a>
            <a href="#" @click.prevent="setActiveSection('W4L2Content')" :class="{ active: isActiveSection('W4L2Content') }">L4.2</a>
            <a href="#" @click.prevent="setActiveSection('W4L3Content')" :class="{ active: isActiveSection('W4L3Content') }">L4.3</a>
            <a href="#" @click.prevent="setActiveSection('W4L4Content')" :class="{ active: isActiveSection('W4L4Content') }">L4.4</a>
            <a href="#" @click.prevent="setActiveSection('W4L5Content')" :class="{ active: isActiveSection('W4L5Content') }">L4.5</a>
          </li>
        </ul>
      </div>

      <!-- Practice -->
      <div class="sidebar-item" :class="{ open: isOpen('practice') }">
        <h2 @click="toggleSection('practice')">
          Practice
          <span class="toggle-icon">{{
            isOpen("practice") ? "▼" : "▶"
          }}</span>
        </h2>
        <ul ref="practice" class="collapse-content">
          <li>
            <router-link to="/dashboard/pa">Programming</router-link>
          </li>
        </ul>
      </div>
    </aside>
  </template>
  
  <script>
  export default {
    name: "CourseSidebar",
    props: ["activeSection", "setActiveSection"],
    data() {
      return {
        openSections: {
          courseIntroduction: true,
          week1: false,
          week2: false,
        },
      };
    },
    methods: {
      toggleSection(section) {
        this.openSections[section] = !this.isOpen(section);
        this.$nextTick(() => {
          this.animateCollapse(section);
        });
      },
      isOpen(section) {
        return this.openSections[section];
      },
      animateCollapse(section) {
        const content = this.$refs[section];
        if (content) {
          if (this.isOpen(section)) {
            content.style.maxHeight = content.scrollHeight + "px";
          } else {
            content.style.maxHeight = null;
          }
        }
      },
      isActiveSection(section) {
      return this.activeSection === section;
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

  