<template>
    <div class="manage-lectures">
      <h1>Manage Lectures</h1>
  
      <!-- Display all lectures grouped by course -->
      <div v-if="lectures.length > 0">
        <div v-for="(lecturesList, index) in lectures" :key="index">
          <h2>{{ lecturesList[0]?.course_name }}</h2>
          <ul>
            <li v-for="lecture in lecturesList" :key="lecture.lecture_id">
              <strong>{{ lecture.lecture_title }}</strong><br>
              Link: <a :href="lecture.lecture_link" target="_blank">{{ lecture.lecture_link }}</a><br>
              Date: {{ formatDate(lecture.lecture_date) }}<br>
              Description: {{ lecture.description }}
            </li>
          </ul>
        </div>
      </div>
      <div v-else>
        <p>No lectures found.</p>
      </div>
  
      <!-- Form to add a new lecture -->
      <h2>Add New Lecture</h2>
      <form @submit.prevent="addLecture">
        <div>
          <label for="course">Select Course:</label>
          <select v-model="newLecture.CourseID" required>
            <option v-for="course in courses" :key="course.CourseID" :value="course.CourseID">
              {{ course.CourseName }}
            </option>
          </select>
        </div>
        <div>
          <label for="title">Lecture Title:</label>
          <input v-model="newLecture.lecture_title" type="text" required />
        </div>
        <div>
          <label for="link">Lecture Link:</label>
          <input v-model="newLecture.lecture_link" type="text" required />
        </div>
        <div>
          <label for="date">Lecture Date:</label>
          <input v-model="newLecture.lecture_date" type="date" required />
        </div>
        <div>
          <label for="description">Description:</label>
          <textarea v-model="newLecture.lecture_description"></textarea>
        </div>
        <button type="submit">Add Lecture</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ManageLectures',
    data() {
      return {
        lectures: [], // Array of arrays, each containing lectures for a specific course
        courses: [],
        newLecture: {
          course_id: null,
          lecture_title: '',
          lecture_link: '',
          lecture_date: '',
          lecture_description: ''
        }
      };
    },
    async created() {
      await this.fetchLectures();
    },
    methods: {
      async fetchLectures() {
        try {
          const response = await axios.get('http://127.0.0.1:2000/study/lectures', {
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            },
          });
          if (response.status === 200) {
            const data = response.data;
            this.lectures = this.groupLecturesByCourse(data.lectures);
            this.courses = data.courses.map(course => ({
              CourseID: course.CourseID,
              CourseName: course.CourseName
            }));
          } else {
            this.lectures = [];
            this.courses = [];
          }
        } catch (error) {
          console.error('Error fetching lectures:', error);
        }
      },
      groupLecturesByCourse(lectures) {
        return lectures.reduce((acc, lecture) => {
          const courseIndex = acc.findIndex(group => group[0].course_id === lecture.course_id);
          if (courseIndex === -1) {
            acc.push([lecture]);
          } else {
            acc[courseIndex].push(lecture);
          }
          return acc;
        }, []);
      },
      async addLecture() {
        try {
          const lectureData = {
            course_id: this.newLecture.course_id,
            lecture_title: this.newLecture.lecture_title,
            lecture_link: this.newLecture.lecture_link,
            lecture_date: this.newLecture.lecture_date,
            lecture_description: this.newLecture.lecture_description
          };
  
          const response = await axios.post('http://127.0.0.1:2000/study/lectures', lectureData, {
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            },
          });
  
          if (response.status === 201) {
            alert('Lecture added successfully!');
            this.newLecture = { course_id: null, lecture_title: '', lecture_link: '', lecture_date: '', lecture_description: '' };
            await this.fetchLectures();
          } else {
            alert('Error adding lecture:', response.data.error);
          }
        } catch (error) {
          console.error('Error adding lecture:', error);
        }
      },
      formatDate(date) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(date).toLocaleDateString(undefined, options);
      }
    }
  };
  </script>
  
  <style scoped>
  .manage-lectures {
    padding: 20px;
  }
  
  h1 {
    margin-bottom: 20px;
  }
  
  h2 {
    margin-top: 20px;
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
  textarea,
  select {
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
  