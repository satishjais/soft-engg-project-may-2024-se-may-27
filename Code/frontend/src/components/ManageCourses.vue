<template>
    <div class="manage-courses">
      <h1>Manage Courses</h1>
  
      <!-- List of Courses -->
      <div v-if="courses.length">
        <h2>All Courses</h2>
        <ul>
          <li v-for="course in courses" :key="course.course_id">
            <strong>{{ course.course_name }}</strong>
            <p>{{ course.course_description }}</p>
            <small>Start Date: {{ formatDate(course.start_date) }}</small>
            <br>
            <small>End Date: {{ formatDate(course.end_date) }}</small>
            <button @click="deleteCourse(course.course_id)">Delete</button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No courses available.</p>
      </div>
  
      <!-- Add Course Form -->
      <h2>Add a New Course</h2>
      <form @submit.prevent="addCourse">
        <div>
          <label for="courseName">Course Name:</label>
          <input type="text" id="courseName" v-model="newCourse.course_name" required />
        </div>
  
        <div>
          <label for="courseDescription">Course Description:</label>
          <textarea id="courseDescription" v-model="newCourse.course_description" required></textarea>
        </div>
  
        <div>
          <label for="startDate">Start Date:</label>
          <input type="date" id="startDate" v-model="newCourse.start_date" required />
        </div>
  
        <div>
          <label for="endDate">End Date:</label>
          <input type="date" id="endDate" v-model="newCourse.end_date" required />
        </div>
  
        <button type="submit">Add Course</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: "ManageCourse",
    data() {
      return {
        courses: [], // Array to hold the list of courses
        newCourse: {
          course_name: "",
          course_description: "",
          start_date: "",
          end_date: "",
        },
      };
    },
    async created() {
      await this.fetchCourses();
    },
    methods: {
      async fetchCourses() {
        try {
          const response = await fetch("http://127.0.0.1:2000/study", {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            },
          });
          const data = await response.json();
          if (response.ok) {
            this.courses = data.study || [];
          } else {
            alert(data.error || "Failed to fetch courses");
          }
        } catch (error) {
          console.error("Error:", error);
          alert("An error occurred while fetching courses.");
        }
      },
      async addCourse() {
        try {
          const response = await fetch("http://127.0.0.1:2000/study", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            },
            body: JSON.stringify(this.newCourse),
          });
          const data = await response.json();
          if (response.ok) {
            alert("Course added successfully!");
            this.newCourse = {
              course_name: "",
              course_description: "",
              start_date: "",
              end_date: "",
            };
            await this.fetchCourses(); // Refresh the list after adding a new course
          } else {
            alert(data.error || "Failed to add course");
          }
        } catch (error) {
          console.error("Error:", error);
          alert("An error occurred while adding the course.");
        }
      },
      async deleteCourse(courseId) {
        try {
          const response = await fetch(`http://127.0.0.1:2000/study/${courseId}`, {
            method: "DELETE",
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            },
          });
          const data = await response.json();
          if (response.ok) {
            alert("Course deleted successfully!");
            await this.fetchCourses(); // Refresh the list after deletion
          } else {
            alert(data.error || "Failed to delete course");
          }
        } catch (error) {
          console.error("Error:", error);
          alert("An error occurred while deleting the course.");
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
  .manage-courses {
    padding: 20px;
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
    padding: 10px;
    border-radius: 5px;
  }
  
  form {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
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
  