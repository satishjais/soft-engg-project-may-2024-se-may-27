<template>
  <div class="dashboard">
    <h1>Welcome, {{ user.name }}</h1>
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
  name: 'DashboardPage',
  data() {
    return {
      user: {},
      announcements: [],
      deadlines: [],
    };
  },
  async created() {
    await this.fetchDashboardData();
  },
  methods: {
    async fetchDashboardData() {
      const token = localStorage.getItem('access_token');
      try {
        const response = await fetch('http://127.0.0.1:2000/dashboard', {
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
        } else {
          alert(data.error || 'Failed to fetch dashboard data');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while fetching dashboard data.');
      }
    },
  },
};
</script>
