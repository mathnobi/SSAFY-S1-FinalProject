<template>
  <div class="container">
    <div class="header">
      <h2>게시판 리스트</h2>
      <RouterLink v-if="isLoggedIn" :to="{ name: 'CreateView' }" class="link">
        <p class="link-text">글쓰기</p>
      </RouterLink>
    </div>
    <div v-if="ArticleList">
      <ArticleList />
    </div>
  </div>
</template>

<script setup>
import ArticleList from '@/components/articles/ArticleList.vue'
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'

const isLoggedIn = ref(!!localStorage.getItem('access_token'));
const store = useCounterStore()

onMounted(() => {
  // mount 되기 전에 store에 있는 전체 게시글 요청 함수를 호출
  store.getArticles()
})
</script>

<style scoped>
.container {
  font-family: Arial, sans-serif;
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
  border-radius: 8px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h2 {
  color: #333;
  font-size: 2rem;
  margin: 0;
}

.link {
  text-decoration: none;
}

.link-text {
  color: black;
  font-size: 1.3rem;
  font-weight: bold;
  cursor: pointer;
}

.link-text:hover {
  color: rgb(118, 116, 124);
}

.ArticleList {
  padding: 20px;
  border-radius: 6px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

</style>
