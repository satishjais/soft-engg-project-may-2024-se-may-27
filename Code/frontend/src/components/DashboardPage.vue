<template>
    <div class="dashboard">
      <div class="header">
        <h1>Welcome, {{ user.name }}</h1>
      </div>
  
      <div class="section">
        <h2>Announcements</h2>
        <div v-if="announcements.length">
          <ul>
            <li v-for="announcement in announcements" :key="announcement.announcement_id">
              <h3>{{ announcement.title }}</h3>
              <p>{{ announcement.content }}</p>
              <small>Created at: {{ formatDate(announcement.created_at) }}</small>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>No announcements available.</p>
        </div>
      </div>
  
      <div class="section">
        <h2>Deadlines</h2>
        <div v-if="deadlines.length">
          <ul>
            <li v-for="(dueDate, title) in deadlines" :key="title">
              <strong>{{ title }}</strong>: {{ formatDate(dueDate) }}
            </li>
          </ul>
        </div>
        <div v-else>
          <p>No deadlines available.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DashboardBoard',
    data() {
      return {
        user: {},
        announcements: [],
        deadlines: {},
      };
    },
    created() {
      this.fetchDashboardData();
    },
    methods: {
      async fetchDashboardData() {
        try {
          const response = await fetch('http://127.0.0.1:2000/dashboard');
          const data = await response.json();
          if (response.ok) {
            this.user = data.dashboard.user;
            this.announcements = data.dashboard.announcements;
            this.deadlines = data.dashboard.deadlines;
          } else {
            console.error('Error fetching dashboard data:', data.error);
          }
        } catch (error) {
          console.error('Fetch error:', error);
        }
      },
      formatDate(date) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(date).toLocaleDateString(undefined, options);
      },
    },
  };
  </script>
  
  <style scoped>
  .dashboard {
    padding: 20px;
  }
  
  .header {
    margin-bottom: 20px;
  }
  
  .section {
    margin-bottom: 40px;
  }
  
  h2 {
    border-bottom: 2px solid #ddd;
    padding-bottom: 10px;
    margin-bottom: 20px;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 20px;
  }
  
  small {
    display: block;
    margin-top: 5px;
    color: #666;
  }
  </style>
  