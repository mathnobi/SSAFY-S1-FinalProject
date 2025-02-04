<template>
  <div class="image-container">
    <img :src="imageUrl" alt="홈 이미지">
  </div>
</template>

<script setup>
import { ref } from 'vue'
import img1 from '@/assets/index.jpg'

// 이미지 URL 참조
const imageUrl = ref(img1)
</script>

<style scoped>
.image-container {
  display: flex;
  justify-content: center; /* 수평 중앙 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
  width: 100%; /* 전체 너비 차지 */
  margin-top: 250px;
}

img {
  max-width: 50%; /* 반응형 이미지 */
  height: auto;
}
</style>