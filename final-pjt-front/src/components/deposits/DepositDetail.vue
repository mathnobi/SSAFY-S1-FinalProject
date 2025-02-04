<template>
  <div>
    <h1>예적금 데이터 상세</h1>
    <!-- 부모 데이터 출력 -->
    <div v-if="deposit">
      <p>금융 회사 : {{ deposit.kor_co_nm }}</p>
      <p>금융 상품명 : {{ deposit.fin_prdt_nm }}</p>
      <!-- <p>금융 상품 소개 : {{ deposit.etc_note }}</p> -->
      <p>가입 제한 : {{ deposit.join_deny }}</p>
      <p>가입 대상 : {{ deposit.join_member }}</p>
      <p>가입 방법 : {{ deposit.join_way }}</p>
      <p>우대 조건 : {{ deposit.spcl_cnd }}</p>
      <hr>
    </div>
    
    <!-- 자식 데이터 출력 -->
    <div v-if="depositOptions" v-for="(option, index) in depositOptions" :key="option.id">
      <p>{{ index + 1 }}번 째 상품입니다.</p>
      <!-- <p>금융상품코드 : {{ option.fin_prdt_cd }}</p>
      <p>저축금리유형명 : {{ option.intr_rate_type_nm }}</p> -->
      <p>저축기간 : {{ option.save_trm }}</p>
      <p>저축금리 : {{ option.intr_rate }}</p>
      <p>최고우대금리 : {{ option.intr_rate2 }}</p>
      
      <td>
        <button @click="saveProduct(option)">저장</button>
      </td>
      <hr>
    </div>

    <div>
      <p>가입 제한 안내</p>
      <p>1:제한없음, 2:서민전용, 3: 일부 제한</p>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const props = defineProps(['deposit'])
const route = useRoute()
const store = useCounterStore()
const deposit = ref(null)
const depositOptions = ref(null)
const token = localStorage.getItem('access_token')

// 상품 저장 함수
const saveProduct = async (option) => {
  try {
    // 먼저 현재 사용자 정보를 가져옴
    const userResponse = await axios({
      method: 'get',
      url: `${store.API_URL}/accounts/profile/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })

    // 현재 저장된 상품 목록 파싱
    let currentProducts = []
    try {
      currentProducts = JSON.parse(userResponse.data.products || '[]')
    } catch (e) {
      currentProducts = []
    }
    
    // 새로운 상품 정보
    const newProduct = {
      bank_name: deposit.value.kor_co_nm,
      product_name: deposit.value.fin_prdt_nm,
      save_trm: option.save_trm,        // 저축 기간
      intr_rate: option.intr_rate,      // 저축 금리
      intr_rate2: option.intr_rate2     // 최고 우대 금리
    }

    // 중복 체크
    const isDuplicate = currentProducts.some(
      product => 
        product.bank_name === newProduct.bank_name && 
        product.product_name === newProduct.product_name
    )

    if (!isDuplicate) {
      // 새 상품 추가
      currentProducts.push(newProduct)

      // 업데이트된 상품 목록 저장
      const updateResponse = await axios({
        method: 'put',
        url: `${store.API_URL}/accounts/profile/`,
        headers: {
          Authorization: `Token ${token}`
        },
        data: { 
          products: JSON.stringify(currentProducts)  // Sending the updated products data in the body
        }
      })

      if (updateResponse.status === 200) {
        alert('상품이 저장되었습니다.')
      }
    } else {
      alert('이미 저장된 상품입니다.')
    }
  } catch (err) {
    console.error(err)
    alert('상품 저장에 실패했습니다.')
  }
}

onMounted(async () => {
  try {
    // 상품 기본 정보 가져오기
    const depositResponse = await axios({
      method: 'get',
      url: `${store.API_URL}/deposits/deposit-products/${route.params.id}`,
    })
    deposit.value = depositResponse.data

    // 상품 옵션 정보 가져오기
    const optionsResponse = await axios({
      method: 'get',
      url: `${store.API_URL}/deposits/deposit-products-options/${route.params.id}`,
    })
    depositOptions.value = optionsResponse.data
  } catch (err) {
    console.log(err)
  }
})
</script>

<style scoped>
</style>