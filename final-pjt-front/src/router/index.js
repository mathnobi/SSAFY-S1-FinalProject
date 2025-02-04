import { createRouter, createWebHistory } from 'vue-router'
import DepositShow from '@/views/deposits/DepositShow.vue'
import DepositDetail from '@/components/deposits/DepositDetail.vue'
import SavingsShow from '@/views/savings/SavingsShow.vue'
import SavingsDetail from '@/components/savings/SavingsDetail.vue'
import Home from '@/views/Home.vue'
import Exchange from '@/views/exchange/Exchange.vue'  
import Bankmap from '@/views/bankmap/Bankmap.vue'
import Signup from '@/components/accounts/Signup.vue'
import Login from '@/components/accounts/Login.vue'
import ArticleView from '@/views/articles/ArticleView.vue'
import CreateView from '@/views/articles/CreateView.vue'
import DetailView from '@/views/articles/DetailView.vue'
import ArticleEditView from '@/views/articles/ArticleEditView.vue'
import ChatBoat from '@/views/chatboat/ChatBoat.vue'
import ProfileView from '@/views/accounts/ProfileView.vue'
import Lotto from '@/views/lottery/Lotto.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 홈 페이지
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    // 예금 데이터 목록 - 전체 데이터 조회
    {
      path: '/deposit',
      name: 'DepositShow',
      component: DepositShow,
    },
    // 예금 데이터 목록 - 상품명 상세 조회
    {
      path: '/deposit/:id',
      name: 'DepositDetail',
      component: DepositDetail,
    },
    // 적금 데이터 목록 - 전체 데이터 조회
    {
      path: '/savings',
      name: 'SavingsShow',
      component: SavingsShow,
    },
    // 적금 데이터 목록 - 상품명 상세 조회
    {
      path: '/savings/:id',
      name: 'SavingsDetail',
      component: SavingsDetail,
    },
    // 환율 데이터 목록 - 전체 데이터 조회
    {
      path: '/exchange',
      name: 'Exchange',
      component: Exchange,
    },
    // 은행 위치 보여주기
    {
      path: '/bankmap',
      name: 'Bankmap',
      component: Bankmap,
    },
    // 회원가입
    {
      path: '/signup',
      name: 'Signup',
      component: Signup,
    },
    // 로그인
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    // 게시판
    {
      path: '/articles',
      name: 'ArticleView',
      component: ArticleView,
    },
    // 게시글 작성
    {
      path: '/articles/create',
      name: 'CreateView',
      component: CreateView,
    },
    // 게시글 상세 조회
    {
      path: '/articles/:id',
      name: 'DetailView',
      component: DetailView,
    },
    // 게시글 수정
    {
      path: '/articles/:id/edit',
      name: 'ArticleEditView',
      component: ArticleEditView,
    },
    // 챗봇
    {
      path: '/chatboat',
      name: 'ChatBoat',
      component: ChatBoat,
    },
    // 프로필 조회
    {
      path: '/profile',
      name: 'ProfileView',
      component: ProfileView,
    },
    // 로또 번호 추출기
    {
      path: '/lottery',
      name: 'Lotto',
      component: Lotto,
    },
  ],
})

export default router
