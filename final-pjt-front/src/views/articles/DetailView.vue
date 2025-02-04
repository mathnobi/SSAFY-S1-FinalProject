<template>
  <div class="container">
    <h1 v-if="article">{{ article.post_id }}번 게시글</h1>
    <div v-if="article" class="article-details">
      <p>제목: {{ article.title }}</p>
      <p>내용: {{ article.content }}</p>
      <p>작성일: {{ article.created_at }}</p>
      <p>수정일: {{ article.updated_at }}</p>

      <button v-if="isAuthor" @click="editArticle" class="button edit">게시글 수정</button>
      <button v-if="isAuthor" @click="deleteArticle" class="button delete">삭제</button>

      <hr>

      <h2>댓글</h2>
      <div v-if="comments.length">
        <div v-for="comment in comments" :key="comment.id" class="comment">
          <div class="comment-info">
            <p>{{ comment.user_id }}번 유저 - {{ comment.content }}</p>
            
            <div v-if="editingCommentId === comment.comment_id" class="comment-edit">
              <input v-model="editedContent" type="text" class="comment-input">
              <div class="button-group">
                <button @click="saveComment(comment)" class="button save">저장</button>
                <button @click="cancelEdit" class="button cancel">취소</button>
              </div>
            </div>
            
            <div v-else class="comment-actions">
              <button 
                v-if="comment.user_id === loggedInUserId" 
                @click="startEdit(comment)" 
                class="button edit"
              >
                댓글 수정
              </button>
              <button v-if="comment.user_id === loggedInUserId" @click="deleteComment(comment)" class="button delete">삭제</button>
            </div>
          </div>

          <hr>
        </div>
      </div>
      
      <textarea v-if="loggedInUserId" v-model="newComment" placeholder="댓글을 입력하세요..." class="comment-input"></textarea>
      <button v-if="loggedInUserId" @click="addComment" class="button add">댓글 작성</button>      
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

const article = ref(null)
const token = localStorage.getItem('access_token')
const isAuthor = ref(false)
let loggedInUserId = ref(null);

const comments = ref([])
const newComment = ref('')

// 댓글 목록 조회
const loadComments = () => {
  const config = token 
    ? { headers: { Authorization: `Token ${token}` } }
    : {};

  axios
    .get(`${store.API_URL}/articles/${route.params.id}/comments/`, config)
    .then((res) => {
      comments.value = res.data
    })
    .catch((err) => {
      console.error(err)
    });
};

// 게시글 상세 조회
onMounted(() => {
  // 로그인한 사용자 정보 조회 (토큰 있을 때만)
  const getUserInfo = () => {
    return token 
      ? axios.get(`${store.API_URL}/dj-rest-auth/user/`, {
          headers: { Authorization: `Token ${token}` }
        })
      : Promise.resolve({ data: { pk: null } });
  };

  // 게시글 조회 설정
  const getArticleConfig = token 
    ? { headers: { Authorization: `Token ${token}` } }
    : {};

  // 비동기 처리
  getUserInfo()
    .then((res) => {
      loggedInUserId.value = res.data.pk || null;

      return axios.get(
        `${store.API_URL}/articles/${route.params.id}/`, 
        getArticleConfig
      );
    })
    .then((res) => {
      article.value = res.data;
      
      // 로그인한 사용자가 있을 때만 작성자 체크
      if (loggedInUserId.value && article.value.user_id === loggedInUserId.value) {
        isAuthor.value = true;
      }
      
      loadComments();
    })
    .catch((err) => {
      console.error(err);
    });
});
// 게시글 수정
const editArticle = () => {
  // 수정 화면으로 이동 (게시글 수정 페이지로 리다이렉트)
  router.push({ name: 'ArticleEditView', params: { id: article.value.post_id } });
};

// 게시글 삭제
const deleteArticle = () => {
  if (confirm('정말로 게시글을 삭제하시겠습니까?')) {
    axios
      .delete(`${store.API_URL}/articles/${route.params.id}/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      })
      .then(() => {
        alert('게시글이 삭제되었습니다.');
        router.push({ name: 'ArticleView' }); // 게시글 목록 페이지로 리다이렉트
      })
      .catch((err) => {
        console.error('삭제 오류:', err);
        alert('본인의 게시글만 삭제가 가능합니다.');
      });
  }
};

// 댓글 작성
const addComment = () => {
  axios
    .post(`${store.API_URL}/articles/${route.params.id}/comments/`, {
      content: newComment.value,
    }, {
      headers: { 
        Authorization: `Token ${token}`, 
      },
    })
    .then((res) => {
      newComment.value = ''
      loadComments();
    })
    .catch((err) => {
      console.error(err)
    });
};

// 댓글 수정
const editingCommentId = ref(null); // 현재 수정 중인 댓글 ID
const editedContent = ref(''); // 수정 중인 댓글 내용

// 수정 모드 시작
const startEdit = (comment) => {
  editingCommentId.value = comment.comment_id
  editedContent.value = comment.content
}

// 수정 취소
const cancelEdit = () => {
  editingCommentId.value = null
  editedContent.value = ''
}

// 댓글 수정 저장
const saveComment = (comment) => {
  axios
    .put(
      `${store.API_URL}/articles/${route.params.id}/comments/${comment.comment_id}/`,
      {
        content: editedContent.value,
      },
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    )
    .then((res) => {
      // 성공적으로 수정된 경우
      const commentIndex = comments.value.findIndex(
        (c) => c.comment_id === comment.comment_id
      )
      if (commentIndex !== -1) {
        comments.value[commentIndex].content = editedContent.value
      }
      editingCommentId.value = null
      editedContent.value = ''
    })
    .catch((err) => {
      console.error('댓글 수정 실패:', err)
      // 에러 처리 로직 추가
    })
}

// 댓글 삭제
const deleteComment = (comment) => {
  axios
    .delete(`${store.API_URL}/articles/${route.params.id}/comments/${comment.comment_id}/`, {
      headers: { Authorization: `Token ${token}` },
    })
    .then((res) => {
      loadComments();
    })
    .catch((err) => {
      console.error(err)
    });
};

</script>

<style scoped>
.container {
  font-family: Arial, sans-serif;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  color: black;
  text-align: left;
}

.article-details p {
  color: #333;
  font-size: 1.1rem;
  margin-bottom: 10px;
}

hr {
  border: 0;
  border-top: 2px solid gray;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  opacity: 0.8;
}

.button.edit {
  background-color: gray;
  color: white;
  font-size: 1rem;
}

.button.delete {
  background-color: gray;
  color: white;
  font-size: 1rem;
}

.button.add {
  background-color: gray;
  color: white;
  font-size: 1rem;
  margin-top: 10px;
}

.comment-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid black;
  border-radius: 4px;
  font-size: 1rem;
}

.comment-edit .button-group {
  display: flex;
  gap: 10px;
}

.button {
  margin-right: 8px;
}

textarea.comment-input {
  height: 80px;
  resize: none;
  background-color: #ffffff;
}

h2 {
  color: black;
  margin-bottom: 15px;
}

.comment {
  background-color: white;
  border-radius: 6px;
}

.comment-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-actions {
  display: flex;
  gap: 10px;
  margin-left: 10px;
}
</style>
