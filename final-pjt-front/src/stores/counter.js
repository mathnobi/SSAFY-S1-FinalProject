import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCounterStore = defineStore('counter', () => {
  const API_URL = 'http://localhost:8000'
  // 예금 데이터  
  const deposits = ref([])  
  const getDepositList = function () {
    axios({
      method: 'get',
      url: `${API_URL}/deposits/deposit-products/`,
    })
    .then((res) => {
      deposits.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
  }

  // 적금 데이터
  const savings = ref([])
  const getSavingsList = function () {
    axios({
      method: 'get',
      url: `${API_URL}/deposits/savings-products/`,
    })
    .then((res) => {
      savings.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
  }
  // 환율 데이터
  const exchange = ref([])
  const getExchangeList = function () {
    axios({
      method: 'get',
      url: `${API_URL}/exchange/`,
    })
    .then((res) => {
      exchange.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
  }

  const calcExchange = function () {
    console.log('calcExchange')
  }

  // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
  const articles = ref([])
  const token = localStorage.getItem('access_token')
  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/articles/`,
      headers: token 
        ? { Authorization: `Token ${token}` } 
        : {},
    })
      .then((res) => {
        articles.value = res.data
      })
      .catch((err) => {
        if (err.response && err.response.status === 401) {
          // 401 에러 처리 (미인증 상태)
          console.log('인증이 필요합니다.')
          articles.value = [] // 빈 배열로 초기화
        } else {
          console.log(err)
        }
      })
  }

  return { API_URL, getDepositList, deposits, getSavingsList, savings, getExchangeList, exchange, calcExchange, articles, getArticles }
}, { persist: true })
