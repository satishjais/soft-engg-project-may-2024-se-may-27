<template>
    <aside class="course-sidebar">
      <!-- Intro -->
      <!-- <div class="sidebar-item" :class="{ open: isOpen('courseIntroduction') }">
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
      </div> -->
    
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
              <a href="#" @click.prevent="setActiveSection('IDEComp')" :class="{ active: isActiveSection('IDEComp') }">PPA 1.1 - Non Graded</a>
              <a href="#" @click.prevent="setActiveSection('IDEComp1')" :class="{ active: isActiveSection('IDEComp1') }">PPA 1.2 - Non Graded</a>
              <a href="#" @click.prevent="setActiveSection('IDEComp2')" :class="{ active: isActiveSection('IDEComp2') }">PPA 1.3 - Non Graded</a>
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
              <a href="#" @click.prevent="setActiveSection('IDEComp20')" :class="{ active: isActiveSection('IDEComp20') }">PPA 2.1 - Non Graded</a>
              <a href="#" @click.prevent="setActiveSection('IDEComp21')" :class="{ active: isActiveSection('IDEComp21') }">PPA 2.2 - Non Graded</a>
              <a href="#" @click.prevent="setActiveSection('IDEComp22')" :class="{ active: isActiveSection('IDEComp22') }">PPA 2.3 - Non Graded</a>
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
              <a href="#" @click.prevent="setActiveSection('IDEComp3')" :class="{ active: isActiveSection('IDEComp3') }">PPA 3.1 - Non Graded</a>
              <a href="#" @click.prevent="setActiveSection('IDEComp31')" :class="{ active: isActiveSection('IDEComp31') }">PPA 3.2 - Non Graded</a>
              <a href="#" @click.prevent="setActiveSection('IDEComp32')" :class="{ active: isActiveSection('IDEComp32') }">PPA 3.3 - Non Graded</a>
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
              <a href="#" @click.prevent="setActiveSection('IDEComp4')" :class="{ active: isActiveSection('IDEComp4') }">PPA 4.1 - Non Graded</a>
              <a href="#" @click.prevent="setActiveSection('IDEComp41')" :class="{ active: isActiveSection('IDEComp41') }">PPA 4.2 - Non Graded</a>
              <a href="#" @click.prevent="setActiveSection('IDEComp42')" :class="{ active: isActiveSection('IDEComp42') }">PPA 4.3 - Non Graded</a>
          </li>
        </ul>
      </div>

      <!-- Course Content -->
      <div class="sidebar-item" :class="{ open: isOpen('Study Content') }">
        <h2 @click="toggleSection('Study Content')">
          Study
          <span class="toggle-icon">{{
            isOpen("Study Content") ? "▼" : "▶"
          }}</span>
        </h2>
        <ul ref="Study Content" class="collapse-content">
          <li>
            <router-link to="/dashboard">Course Content</router-link>
          </li>
        </ul>
      </div>
    </aside>
  </template>
  
  <script>
  export default {
    name: "PASidebar",
    props: ["activeSection", "setActiveSection"],
    data() {
      return {
        openSections: {
          courseIntroduction: false,
          week1: true,
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

  