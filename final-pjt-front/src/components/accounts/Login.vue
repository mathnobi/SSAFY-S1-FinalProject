<template>
  <div class="login-container">
    <form @submit.prevent="login" class="login-form">
      <h2 class="login-title">로그인</h2>
      <input v-model="email" type="email" placeholder="이메일" required class="input-field" />
      <input v-model="password" type="password" placeholder="비밀번호" required class="input-field" />
      <button type="submit" class="submit-button">로그인</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://localhost:8000/dj-rest-auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          if (data.key) {
            localStorage.setItem('access_token', data.key);
            alert('로그인 성공');
            this.$emit('loginSuccess');
            this.$router.push('/');
          } else {
            console.error('토큰이 응답에 없습니다:', data);
            alert('로그인 응답에 토큰이 없습니다');
          }
        } else {
          console.error('로그인 실패:', data);
          alert(data.detail || '로그인 실패');
        }
      } catch (error) {
        console.error("로그인 오류:", error);
        alert("로그인 중 오류가 발생했습니다.");
      }
    },
  },
};
</script>

<style scoped>
/* 전체 페이지 스타일 */
html, body {
  height: 100%;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 화면의 상단으로 위치하도록 변경 */
}

/* 로그인 폼을 감싸는 컨테이너 스타일 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 로그인 폼을 상단으로 위치 */
  height: 100%;
  width: 100%;
  padding-top: 100px; /* 폼을 화면 위에서 100px 정도 아래로 위치시킴 */
}

/* 로그인 폼 스타일 */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px; /* 각 항목 간 여백 */
  width: 400px;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center; /* 로그인 제목을 중앙 정렬 */
}

/* 로그인 제목 스타일 */
.login-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 15px;
  font-weight: bold;
}

/* 입력 필드 스타일 */
.input-field {
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 95%;
}

/* 로그인 버튼 스타일 */
.submit-button {
  padding: 10px;
  background-color: gray;
  color: white;
  font-size: 1.1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: rgb(118, 116, 124);
}
</style>
