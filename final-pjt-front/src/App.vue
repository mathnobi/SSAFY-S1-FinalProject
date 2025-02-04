<template>
  <div class="main-container">
    <h1 class="site-title">
      <RouterLink to="/">금리 비교 사이트</RouterLink>
    </h1>

    <!-- 현재 페이지를 표시할 div -->
    <div class="auth-links">
      <!-- 현재 페이지를 표시하는 텍스트 -->
      <!-- <p class="current-page">현재 보고 있는 페이지는 '{{ currentPage }}' 입니다.</p> -->

      <!-- 로그인/회원가입/로그아웃 버튼 -->
      <div class="auth-buttons">
        <RouterLink v-if="!isLoggedIn" to="/login">로그인</RouterLink>
        <RouterLink v-if="!isLoggedIn" to="/signup">회원가입</RouterLink>
        <RouterLink v-if="isLoggedIn" to="/profile">프로필</RouterLink>
        <form v-if="isLoggedIn" @submit.prevent="logout" class="logout-form">
          <input type="submit" value="로그아웃">
        </form>
      </div>
    </div>

    <header class="header-container" style="font-size: 1.3rem;">
      <nav class="nav-container">
        <div class="nav-links-left">
          <RouterLink to="/deposit">예금금리비교</RouterLink>
          <RouterLink to="/savings">적금금리비교</RouterLink>
          <RouterLink to="/exchange">환율비교</RouterLink>
          <RouterLink to="/bankmap">은행 위치</RouterLink>
          <RouterLink to="/chatboat">챗봇</RouterLink>
          <RouterLink to="/articles">자유게시판</RouterLink>
          <RouterLink to="/lottery">로또 번호 추출기</RouterLink>
        </div>
      </nav>
    </header>
    <RouterView @loginSuccess="updateLoginStatus" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink, RouterView, useRouter, useRoute } from 'vue-router'

const isLoggedIn = ref(!!localStorage.getItem('access_token'));
const router = useRouter();
const route = useRoute(); // 현재 경로 추적

const logout = () => {
  localStorage.removeItem('access_token');
  isLoggedIn.value = false;
  router.push('/');
};

const updateLoginStatus = () => {
  isLoggedIn.value = true;
};

// 현재 페이지 이름을 추적하는 computed property
const currentPage = computed(() => {
  const routeName = route.name;
  // console.log(routeName)
  if (routeName === 'DepositShow') return '예금금리비교';
  if (routeName === 'SavingsShow') return '적금금리비교';
  if (routeName === 'Exchange') return '환율비교';
  if (routeName === 'Bankmap') return '은행 위치';
  if (routeName === 'ChatBoat') return '챗봇';
  if (routeName === 'ProfileView') return '프로필';
  if (routeName === 'Login') return '로그인';
  if (routeName === 'Signup') return '회원가입';
  if (routeName === 'ArticleView') return '자유게시판';
  if (routeName === 'Lotto') return '로또 당첨 가자!';
  return '홈'; // 기본값
});
</script>

<style scoped>
/* 사이트 제목 스타일 */
.site-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0 0 0 0; /* 하단 마진을 0으로 설정 */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', 'Helvetica', sans-serif;
}

/* 로그인/회원가입/로그아웃 버튼 스타일 */
.auth-links {
  display: flex;
  justify-content: space-between; /* 두 영역을 양쪽 끝으로 분리 */
  align-items: center; /* 세로 중앙 정렬 */
  padding: 0px 20px;
  /* border-bottom: 2px solid black; */
  position: relative;
}

.current-page {
  font-size: 1.2rem;
  font-weight: bold;
  /* color: #ff4081; */
  text-align: center; /* 가운데 정렬 */
  flex-grow: 1; /* p 태그가 중앙에 고정되도록 */
  margin: 0;
  position: absolute; /* 절대 위치 지정 */
  left: 50%; /* 왼쪽에서 50% */
  transform: translateX(-50%); /* 정확히 중앙에 위치시키기 위한 수평 이동 */
}

.auth-buttons {
  display: flex;
  gap: 15px;
  justify-content: flex-end; /* 오른쪽 끝에 배치 */
  margin-left: auto; /* 오른쪽으로 밀기 위한 마진 설정 */
}

.auth-links a {
  font-weight: bold;
  padding: 8px 15px;
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
  text-decoration: none;
  color: black;
}

.logout-form input[type="submit"] {
  background-color: white;
  color: black;
  font-size: 1rem;
  padding: 8px 15px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

/* 헤더 스타일 */
.header-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: lightgrey;
  padding: 15px 20px;
  border-top: 2px solid black;
  border-bottom : 2px solid black;
}

.nav-container {
  display: flex;
  justify-content: center;
  width: 100%;
}

.nav-links-left {
  display: flex;
  gap: 6rem; /* 항목 간 간격을 더 넓게 설정 */
  flex-wrap: wrap;
}

a {
  text-decoration: none;
  color: black;
  font-weight: bold;
  padding: 8px 15px;
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* 금리 비교 사이트 컨테이너 */
.main-container {
  margin: 30px 250px 10px 250px;
}
</style>