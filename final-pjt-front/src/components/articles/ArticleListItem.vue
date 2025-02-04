<template>
  <RouterLink :to="{ name: 'DetailView', params: { id: article.post_id } }" class="link">
    <p class="value"> {{ article.title }}</p>
    <hr>
  </RouterLink>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  article: Object
})
</script>

<style scoped>
.link {
  text-decoration: none; /* RouterLink의 밑줄 제거 */
}

.value {
  color: black; /* 글자 색을 검정으로 */
}

hr {
  border: 0; /* 기존 border 제거 */
  border-top: 1px solid gray; /* 선의 두께는 1px, 색상은 밝은 회색 */
  margin: 10px 0; /* 위아래 여백 추가 */
}
</style>
