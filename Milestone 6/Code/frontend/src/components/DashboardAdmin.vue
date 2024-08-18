<template>
  <div class="dashboard-container">
    <div class="dashboard-card">
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
          <h2>Total Lectures</h2>
          <p>{{ totalLectures }}</p>
        </div>
      </div>

      <div class="manage-buttons">
        <button @click="navigateTo('ManageCourse')">Manage Course</button>
        <button @click="navigateTo('ManageLectures')">Manage Lectures</button>
        <button @click="navigateTo('ManageUsers')">Manage Users</button>
      </div>
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
      totalLectures: 0,
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
.dashboard-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Full height of the viewport */
  background-color: #f0f0f0;
}

.dashboard-card {
  background-color: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
  text-align: center;
}

.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
}

.stat {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  flex: 1 1 calc(33.333% - 20px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.manage-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
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
