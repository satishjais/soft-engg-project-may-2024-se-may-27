<template>
  <div class="manage-lectures-container">
    <div class="manage-lectures-card">
      <h1>Manage Lectures</h1>

      <!-- Add Lecture Form -->
      <h2>Add a New Lecture</h2>
      <form @submit.prevent="addLecture">
        <div>
          <label for="lectureTitle">Lecture Title:</label>
          <input type="text" id="lectureTitle" v-model="newLecture.lecture_title" required />
        </div>
        <div>
          <label for="lectureWeek">Week Number:</label>
          <input type="number" id="lectureWeek" v-model="newLecture.week_number" required />
        </div>
        <div>
          <label for="lectureLecture">Lecture Number:</label>
          <input type="number" id="lectureLecture" v-model="newLecture.lecture_number" required />
        </div>
        <div>
          <label for="lectureLink">Lecture Link:</label>
          <input type="url" id="lectureLink" v-model="newLecture.lecture_link" required />
        </div>
        <div>
          <label for="lectureDate">Lecture Date:</label>
          <input type="date" id="lectureDate" v-model="newLecture.lecture_date" required />
        </div>
        <div>
          <label for="lectureDescription">Description:</label>
          <textarea id="lectureDescription" v-model="newLecture.lecture_description" required></textarea>
        </div>
        <button type="submit">Add Lecture</button>
      </form>

      <br>

      <!-- List of Lectures -->
      <div v-if="lectures.length">
        <h2>All Lectures</h2>
        <ul>
          <li v-for="lecture in lectures" :key="lecture.lecture_id">
            <div v-if="isValidVideoLink(lecture.lecture_link)">
              <iframe
                :src="formatVideoLink(lecture.lecture_link)"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                width="560"
                height="315"
              ></iframe>
            </div>
            <br>
            <strong>{{ lecture.lecture_title }}</strong>
            <p>{{ lecture.description }}</p>
            <small>Date: {{ formatDate(lecture.lecture_date) }}</small>
            <br>
            <button style="margin-top: 1%;" @click="deleteLecture(lecture.lecture_id)">Delete</button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No lectures available.</p>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "ManageLectures",
  data() {
    return {
      lectures: [], // Array to hold the list of lectures
      newLecture: {
        lecture_title: "",
        lecture_link: "",
        lecture_date: "",
        lecture_description: "",
        week_number: "",
        lecture_number: "",
      },
    };
  },
  async created() {
    await this.fetchLectures();
  },
  methods: {
    async fetchLectures() {
      try {
        const response = await fetch("http://127.0.0.1:2000/study/lectures", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.lectures = data.lectures || [];
        } else {
          alert(data.error || "Failed to fetch lectures");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while fetching lectures.");
      }
    },
    async addLecture() {
      try {
        const response = await fetch("http://127.0.0.1:2000/study/lectures", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify(this.newLecture),
        });
        const data = await response.json();
        if (response.ok) {
          alert("Lecture added successfully!");
          this.newLecture = {
            lecture_title: "",
            lecture_link: "",
            lecture_date: "",
            lecture_description: "",
          };
          await this.fetchLectures(); // Refresh the list after adding a new lecture
        } else {
          alert(data.error || "Failed to add lecture");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while adding the lecture.");
      }
    },
    async deleteLecture(lectureId) {
      try {
        const response = await fetch(`http://127.0.0.1:2000/study/lectures/${lectureId}`, {
          method: "DELETE",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert("Lecture deleted successfully!");
          await this.fetchLectures(); // Refresh the list after deletion
        } else {
          alert(data.error || "Failed to delete lecture");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while deleting the lecture.");
      }
    },
    isValidVideoLink(link) {
      const regex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
      return regex.test(link);
    },
    formatVideoLink(link) {
      const videoId = link.split("v=")[1] || link.split("/").pop();
      return `https://www.youtube.com/embed/${videoId}`;
    },
    formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString(undefined, options);
    },
  },
};
</script>

<style scoped>
.manage-lectures-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-bottom: 50px; /* Full height of the viewport */
  background-color: #f0f0f0;
}

.manage-lectures-card {
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

iframe {
  margin-top: 10px;
  border-radius: 5px;
}

form {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

label {
  font-weight: bold;
}

input,
textarea {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
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
