<template>
  <div class="signup-container">
    <form @submit.prevent="submitSignup" class="signup-form">
      <h2 class="signup-title">회원가입</h2>
      <div class="input-group">
        <label for="username">사용자 이름</label>
        <input type="text" id="username" v-model="username" required class="input-field" />
      </div>
      <div class="input-group">
        <label for="email">이메일</label>
        <input type="email" id="email" v-model="email" required class="input-field" />
      </div>
      <div class="input-group">
        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model="password1" required class="input-field" />
      </div>
      <div class="input-group">
        <label for="password2">비밀번호 확인</label>
        <input type="password" id="password2" v-model="password2" required class="input-field" />
      </div>
      <div class="input-group">
        <label for="age">나이</label>
        <input type="number" id="age" v-model="age" required class="input-field" />
      </div>
      <div class="input-group">
        <label for="gender">성별</label>
        <select id="gender" v-model="gender" required class="input-field">
          <option value="남">남</option>
          <option value="여">여</option>
        </select>
      </div>
      <div class="input-group">
        <label for="salary">연봉</label>
        <input type="number" id="salary" v-model="salary" required class="input-field" />
      </div>
      <div class="input-group">
        <label for="wealth">자산</label>
        <input type="number" id="wealth" v-model="wealth" required class="input-field" />
      </div>
      <div class="input-group">
        <label for="debt">부채</label>
        <input type="number" id="debt" v-model="debt" required class="input-field" />
      </div>
      <div class="input-group">
        <label for="tendency">투자성향</label>
        <select id="tendency" v-model="tendency" required class="input-field">
          <option value="1">고위험 고수익</option>
          <option value="2">중위험 중수익</option>
          <option value="3">저위험 저수익</option>
        </select>
      </div>
      <button type="submit" class="submit-button">회원가입</button>
    </form>
  </div>
</template>


<script>
export default {
  data() {
    return {
      username: '',
      password1: '',
      password2: '',
      email: '',
      age: 26,         // 기본값 설정
      gender: '남',     // 기본값 설정
      salary: 0,       // 기본값 설정
      wealth: 0,       // 기본값 설정
      debt: 0,         // 기본값 설정
      tendency: 1,     // 기본값 설정
    };
  },
  methods: {
    validateForm() {
      if (!this.username || !this.email || !this.password1 || !this.password2) {
        alert("필수 항목을 모두 입력해주세요.");
        return false;
      }
      if (this.password1 !== this.password2) {
        alert("비밀번호가 일치하지 않습니다.");
        return false;
      }
      if (this.tendency < 1 || this.tendency > 3) {
        alert("투자성향은 1~3 사이의 값이어야 합니다.");
        return false;
      }
      return true;
    },
    async submitSignup() {
      if (!this.validateForm()) return;

      const payload = {
        username: this.username,
        email: this.email,
        password1: this.password1,
        password2: this.password2,
        age: parseInt(this.age),
        gender: this.gender,
        salary: parseInt(this.salary),
        wealth: parseInt(this.wealth),
        debt: parseInt(this.debt),
        tendency: parseInt(this.tendency),
      };

      try {
        const response = await fetch('http://localhost:8000/dj-rest-auth/registration/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        });

        if (response.ok) {
          const data = await response.json();
          alert('회원가입이 완료되었습니다.');
          this.$router.push('/');
        } else {
          const errorData = await response.json();
          const errorMessage = Object.entries(errorData)
            .map(([key, value]) => `${key}: ${value}`)
            .join('\n');
          alert(errorMessage || '회원가입 실패');
        }
      } catch (error) {
        console.error("회원가입 오류:", error);
        alert("회원가입 중 오류가 발생했습니다.");
      }
    }
  }
};
</script>

<style scoped>
/* 전체 페이지 스타일 */
html, body {
  height: 100%;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 화면의 상단으로 위치하도록 설정 */
}

/* 회원가입 폼을 감싸는 컨테이너 스타일 */
.signup-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  height: 100%;
  width: 100%;
  padding-top: 50px; /* 폼을 화면 위에서 50px 정도 아래로 위치시킴 */
}

/* 회원가입 폼 스타일 */
.signup-form {
  display: flex;
  flex-direction: column;
  gap: 20px; /* 각 항목 간 여백 */
  width: 400px;
  padding: 25px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* 회원가입 제목 스타일 */
.signup-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 20px;
  font-weight: bold;
}

/* 각 입력 항목 스타일 */
.input-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
  text-align: left;
}

.input-group label {
  font-size: 1rem;
  color: #2c3e50;
}

/* 입력 필드 스타일 */
.input-field {
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  box-sizing: border-box;
}

/* 회원가입 버튼 스타일 */
.submit-button {
  padding: 12px;
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