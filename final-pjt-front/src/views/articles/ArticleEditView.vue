<template>
    <div>
      <h1>게시글 수정</h1>
      <div v-if="article">
        <form @submit.prevent="updateArticle">
          <div>
            <label for="title">제목</label>
            <input
              type="text"
              id="title"
              v-model="article.title"
              placeholder="제목을 입력하세요"
              required
            />
          </div>
  
          <div>
            <label for="content">내용</label>
            <textarea
              id="content"
              v-model="article.content"
              placeholder="내용을 입력하세요"
              required
            ></textarea>
          </div>
  
          <button type="submit">수정하기</button>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import axios from 'axios';
  import { ref, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useCounterStore } from '@/stores/counter';
  
  const store = useCounterStore();
  const route = useRoute();
  const router = useRouter();
  
  const article = ref(null); // 게시글 정보
  const token = localStorage.getItem('access_token');
  
  // 게시글 상세 조회
  onMounted(() => {
    axios
      .get(`${store.API_URL}/articles/${route.params.id}/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      })
      .then((res) => {
        article.value = res.data;
      })
      .catch((err) => {
        console.error('게시글 조회 오류:', err);
        alert('게시글을 불러오는 데 실패했습니다.');
      });
  });
  
  // 게시글 수정
  const updateArticle = () => {
    axios
      .put(
        `${store.API_URL}/articles/${route.params.id}/`,
        {
          title: article.value.title,
          content: article.value.content,
        },
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      )
      .then(() => {
        alert('게시글이 수정되었습니다.');
        router.push({ name: 'DetailView', params: { id: article.value.post_id } });
      })
      .catch((err) => {
        console.error('수정 오류:', err);
        alert('게시글 수정에 실패했습니다.');
      });
  };
  </script>
  
  <style scoped>
  /* 스타일을 추가할 수 있습니다 */
  form {
    display: flex;
    flex-direction: column;
  }
  
  input,
  textarea {
    margin-bottom: 15px;
    padding: 8px;
    font-size: 14px;
    width: 100%;
  }
  
  button {
    background-color: gray;
    color: white;
    padding: 10px 15px;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: gray;
  }
  </style>
  