<template>
    <div id="app">
      <HeaderFile />
      <div class="main-container">
        <div class="content-wrapper">
          <PASidebar :activeSection="activeSection" :setActiveSection="setActiveSection" />
          
          <main class="content">
            <div v-if="activeSection === 'IDEComp'">
              <W1PPA1 />
            </div>
            <div v-if="activeSection === 'IDEComp1'">
              <W1PPA2 />
            </div>
            <div v-if="activeSection === 'IDEComp2'">
              <W1PPA3 />
            </div>
            <div v-if="activeSection === 'IDEComp20'">
              <W2PPA1 />
            </div>
            <div v-if="activeSection === 'IDEComp21'">
              <W2PPA2 />
            </div>
            <div v-if="activeSection === 'IDEComp22'">
              <W2PPA3 />
            </div>
            <div v-if="activeSection === 'IDEComp3'">
              <W3PPA1 />
            </div>
            <div v-if="activeSection === 'IDEComp31'">
              <W3PPA2 />
            </div>
            <div v-if="activeSection === 'IDEComp32'">
              <W3PPA3 />
            </div>
            <div v-if="activeSection === 'IDEComp4'">
              <W4PPA1 />
            </div>
            <div v-if="activeSection === 'IDEComp41'">
              <W4PPA2 />
            </div>
            <div v-if="activeSection === 'IDEComp42'">
              <W4PPA3 />
            </div>
          </main>
        </div>
      </div> 
    </div>
  </template>
  
  
  <script>
  import HeaderFile from './HeaderFile.vue';
  import PASidebar from './PASidebar.vue';
  import W1PPA1 from './PPA/W1PPA1.vue';
  import W1PPA2 from './PPA/W1PPA2.vue';
  import W1PPA3 from './PPA/W1PPA3.vue';
  import W2PPA1 from './PPA/W2PPA1.vue';
  import W2PPA2 from './PPA/W2PPA2.vue';
  import W2PPA3 from './PPA/W2PPA3.vue';
  import W3PPA1 from './PPA/W3PPA1.vue';
  import W3PPA2 from './PPA/W3PPA2.vue';
  import W3PPA3 from './PPA/W3PPA3.vue';
  import W4PPA1 from './PPA/W4PPA1.vue';
  import W4PPA2 from './PPA/W4PPA2.vue';
  import W4PPA3 from './PPA/W4PPA3.vue';
  
  
  
  export default {
  name: "PracticeAssignment",
  components: {
    HeaderFile,
    W1PPA1,
    W1PPA2,
    W1PPA3,
    W2PPA1,
    W2PPA2,
    W2PPA3,
    W3PPA1,
    W3PPA2,
    W3PPA3,
    W4PPA1,
    W4PPA2,
    W4PPA3,
    PASidebar
  },
  data() {
    return {
      activeSection: 'IDEComp',
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