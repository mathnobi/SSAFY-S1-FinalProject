<template>
  <div>
    <hr>
    <ArticleListItem 
      v-for="article in store.articles"
      :key="article.post_id"
      :article="article"
    />
  </div>
</template>

<script setup>
import ArticleListItem from '@/components/articles/ArticleListItem.vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
</script>

<style scoped>
  hr {
    border: 0; /* 기존 border 제거 */
    border-top: 1px solid gray; /* 선의 두께는 1px, 색상은 밝은 회색 */
  }
</style>
