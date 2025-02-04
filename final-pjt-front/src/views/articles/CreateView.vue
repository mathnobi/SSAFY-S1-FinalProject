<template>
  <div class="form-container">
    <h1 class="form-title">게시글 작성</h1>
    <form @submit.prevent="createArticle" class="article-form">
      <div class="form-group">
        <label for="title" class="form-label">제목 : </label>
        <input type="text" id="title" v-model.trim="title" class="input-field" placeholder="제목을 입력하세요">
      </div>
      <div class="form-group">
        <label for="content" class="form-label">내용 : </label>
        <textarea id="content" v-model.trim="content" class="textarea-field" placeholder="내용을 입력하세요"></textarea>
      </div>
      <input type="submit" class="submit-button" value="작성 완료">
    </form>
  </div>
</template>

  
  <script setup>
  import { ref } from 'vue'
  import { useCounterStore } from '@/stores/counter'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  
  const title = ref('')
  const content = ref('')
  const store = useCounterStore()
  const router = useRouter()
    
  const createArticle = function () {
    const token = localStorage.getItem('access_token')

    axios({
        method: 'post',
        url: `${store.API_URL}/articles/`,
        data: {
            title: title.value,
            content: content.value
        },
        headers: {
            Authorization: `Token ${token}`
        }
    })
        .then((res) => {
            // console.log('게시글 작성 성공:', res.data)
            router.push({ name: 'ArticleView' }) 
        })
        .catch((err) => {
            console.log('에러 상세:', err.response)
            if (err.response?.status === 405) {
                console.log('허용되지 않은 메서드입니다.')
            } else {
                alert('게시글 작성 중 오류가 발생했습니다.')
            }
        })
}
  
  </script>
  
  <style scoped>
  /* 전체 페이지 스타일 */
  html, body {
    height: 100%;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: flex-start; /* 화면의 상단으로 위치하도록 변경 */
    font-family: Arial, sans-serif;
  }

  /* 폼을 감싸는 컨테이너 스타일 */
  .form-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    padding: 50px 20px;
  }

  /* 제목 스타일 */
  .form-title {
    font-size: 2rem;
    color: #2c3e50;
    font-weight: bold;
    margin-bottom: 20px;
  }

  /* 폼 스타일 */
  .article-form {
    display: flex;
    flex-direction: column;
    gap: 20px; /* 각 항목 간 여백 */
    width: 100%;
    max-width: 600px;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  /* 입력 필드 스타일 */
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .form-label {
    font-size: 1.1rem;
    color: #333;
  }

  .input-field, .textarea-field {
    padding: 12px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: 100%;
  }

  .textarea-field {
    height: 150px;
    resize: vertical;
  }

  /* 제출 버튼 스타일 */
  .submit-button {
    padding: 12px;
    background-color: gray;
    color: white;
    font-size: 1.1rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    width: 100%;
  }

  .submit-button:hover {
    background-color: rgb(118, 116, 124);
  }
  </style>