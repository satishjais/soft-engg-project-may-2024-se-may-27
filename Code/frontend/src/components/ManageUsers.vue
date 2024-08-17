<template>
  <div class="manage-users-container">
    <div class="manage-users-card">
      <h1>Manage Users</h1>

      <br>
      <!-- List of Users -->
      <div v-if="users.length">
        <h2>All Users</h2>
        <ul>
          <li v-for="user in users" :key="user.user_id">
            <strong>{{ user.name }}</strong>
            <br>
            <small>Email: {{ user.email }}</small>
            <br>
            <small>Username: {{ user.username }}</small>
            <br>
            <small>Mobile: {{ user.mob }}</small>
            <br>
            <small>Date Joined: {{ formatDate(user.joined_date) }}</small>
            <br>
            <small>Role: {{ user.role }}</small>
            <br>
            <button style="margin-top: 1%;" @click="deleteUser(user.user_id)">Delete</button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No users available.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ManageUsers",
  data() {
    return {
      users: [], // Array to hold the list of users
    };
  },
  async created() {
    await this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await fetch("http://127.0.0.1:2000/user", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.users = data.users || [];
        } else {
          alert(data.error || "Failed to fetch users");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while fetching users.");
      }
    },
    async deleteUser(userId) {
      try {
        const response = await fetch(`http://127.0.0.1:2000/user/${userId}`, {
          method: "DELETE",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert("User deleted successfully!");
          await this.fetchUsers(); // Refresh the list after deletion
        } else {
          alert(data.error || "Failed to delete user");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while deleting the user.");
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
.manage-users-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-bottom: 50px; /* Full height of the viewport */
  background-color: #f0f0f0;
}

.manage-users-card {
  background-color: white;
  margin-top: 40px;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
  text-align: center;
}

h1 {
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background-color: #f5f5f5;
  margin-bottom: 15px;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

button {
  padding: 10px;
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
