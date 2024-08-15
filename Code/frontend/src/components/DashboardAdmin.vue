<template>
    <div class="dashboard">
      <h1>Welcome, {{ user.name }}</h1>
  
      <div class="stats">
        <div class="stat">
          <h2>Total Users</h2>
          <p>{{ totalUsers }}</p>
        </div>
        <div class="stat">
          <h2>Total Courses</h2>
          <p>{{ totalCourses }}</p>
        </div>
        <div class="stat">
          <h2>Total Assignments</h2>
          <p>{{ totalAssignments }}</p>
        </div>
        <div class="stat">
          <h2>Total Lectures</h2>
          <p>{{ totalLectures }}</p>
        </div>
        <div class="stat">
          <h2>Total Announcements</h2>
          <p>{{ totalAnnouncements }}</p>
        </div>
        <div class="stat">
          <h2>Total Course Documents</h2>
          <p>{{ totalDocs }}</p>
        </div>
      </div>
  
      <div class="manage-buttons">
        <button @click="navigateTo('ManageCourse')">Manage Courses</button>
        <button @click="navigateTo('manage-assignments')">Manage Assignments</button>
        <button @click="navigateTo('ManageLectures')">Manage Lectures</button>
        <button @click="navigateTo('manage-announcements')">Manage Announcements</button>
        <button @click="navigateTo('manage-docs')">Manage Course Docs</button>
      </div>
  
      <div v-if="announcements.length">
        <h2>Announcements</h2>
        <ul>
          <li v-for="announcement in announcements" :key="announcement.announcement_id">
            <strong>{{ announcement.title }}</strong>
            <p>{{ announcement.content }}</p>
            <small>{{ announcement.created_at }}</small>
          </li>
        </ul>
      </div>
  
      <div v-if="deadlines.length">
        <h2>Deadlines</h2>
        <ul>
          <li v-for="(date, title) in deadlines" :key="title">
            <strong>{{ title }}</strong>
            <p>Due Date: {{ date }}</p>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AdminDash',
    data() {
      return {
        user: {},
        announcements: [],
        deadlines: [],
        totalUsers: 0,
        totalCourses: 0,
        totalAssignments: 0,
        totalLectures: 0,
        totalAnnouncements: 0,
        totalDocs: 0,
      };
    },
    async created() {
      await this.fetchDashboardData();
    },
    methods: {
      async fetchDashboardData() {
        const token = localStorage.getItem('access_token');
        try {
          const response = await fetch('http://127.0.0.1:2000/dashboard/admin', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });
  
          const data = await response.json();
          if (response.ok) {
            this.user = data.dashboard.user;
            this.announcements = data.dashboard.announcements;
            this.deadlines = data.dashboard.deadlines;
            this.totalUsers = data.dashboard.total_users;
            this.totalCourses = data.dashboard.total_courses;
            this.totalAssignments = data.dashboard.total_assignments;
            this.totalLectures = data.dashboard.total_lectures;
            this.totalAnnouncements = data.dashboard.total_announcements;
            this.totalDocs = data.dashboard.total_docs;
          } else {
            alert(data.error || 'Failed to fetch dashboard data');
          }
        } catch (error) {
          console.error('Error:', error);
          alert('An error occurred while fetching dashboard data.');
        }
      },
      navigateTo(route) {
        this.$router.push({ name: route });
      },
    },
  };
  </script>

  <style scoped>
  .dashboard {
    padding: 20px;
  }

  .stats {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 20px;
  }
  
  .stat {
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 8px;
    flex: 1 1 calc(33.333% - 20px);
    text-align: center;
  }
  
  .manage-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  