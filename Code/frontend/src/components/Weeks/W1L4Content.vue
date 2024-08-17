<template>
  <h1>{{ dynamicName }}</h1>
  <div class="video-chat">
    <div class="video-container" v-if="isValidVideoLink(lecture.lecture_link)">
      <iframe 
          width="853" 
          height="480" 
          :src="formatVideoLink(lecture.lecture_link)" 
          :title="lecture.lecture_title" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          referrerpolicy="strict-origin-when-cross-origin"
          allowfullscreen>
      </iframe>
    </div>
    <VChat />
  </div>
  <p>{{ lecture.lecture_description }}</p>
  <small>Date: {{ formatDate(lecture.lecture_date) }}</small>
</template>

<script>
import VChat from './VChat.vue'
export default {
  components: {
    VChat,
  },
  data() {
    return {
      lecture: {}, // Object to hold the lecture details
    };
  },
  async created() {
    await this.fetchLecture();
  },
  computed: {
    dynamicName() {
      return `W${this.lecture.week_number}L${this.lecture.lecture_number}Content: ${this.lecture.lecture_title}`;
    },
  },
  methods: {
    async fetchLecture() {
      try {
        const response = await fetch("http://127.0.0.1:2000/study/lectures", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        const data = await response.json();
        console.log(data)
        if (response.ok && data.lectures.length) {
          // Assuming you want to display the first lecture for now
          this.lecture = data.lectures[3];
        } else {
          alert(data.error || "Failed to fetch lecture details");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while fetching lecture details.");
      }
    },
    isValidVideoLink(link) {
        const regex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
        console.log(link)
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
