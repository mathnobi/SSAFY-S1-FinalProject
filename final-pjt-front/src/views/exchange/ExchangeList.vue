<template>
  <div>
    <label for="krw-input">원화 : </label>
    <input 
      type="number" 
      id="krw-input" 
      v-model.number="krw" 
      placeholder="원화 금액 입력"
    >
    
    <select 
      v-model="selectedExchange" 
      @change="selectExchange"
    >
      <option value="" disabled>국가 선택</option>
      <option 
        v-for="exchange in exchanges" 
        :key="exchange.id" 
        :value="exchange"
      >
        {{ exchange.cur_nm }}
      </option>
    </select>
    
    <div v-if="selectedExchange">
      <h3>{{ selectedExchange.cur_nm }} 환율 정보</h3>
      <p v-if="selectedExchange.cur_nm !== '한국 원'">
        환율: 1 {{ selectedExchange.cur_nm }} = {{ selectedExchange.tts }}원
      </p>
      <p v-if="selectedExchange.cur_nm === '한국 원'">
        환율: 1 {{ selectedExchange.cur_nm }} = 1원
      </p>
      <p v-if="selectedExchange.cur_nm !== '한국 원'">
        변환 금액: {{ convertedAmount.toFixed(2) }} {{ selectedExchange.cur_nm }}
      </p>
      <p v-if="selectedExchange.cur_nm === '한국 원'">
        변환 금액: {{ krw }} {{ selectedExchange.cur_nm }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  exchanges: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['exchange-selected'])

const krw = ref(0)
const selectedExchange = ref(null)
const convertedAmount = ref(0)

const selectExchange = () => {
  // 선택된 환율이 "한국 원"이 아닌 경우에만 변환을 진행
  if (selectedExchange.value && krw.value && selectedExchange.value.cur_nm !== "한국 원") {
    const exchangeRate = parseFloat(selectedExchange.value.tts.replace(/,/g, ''))
    convertedAmount.value = krw.value / exchangeRate
    
    // 부모 컴포넌트에 선택된 환율 정보 전달
    emit('exchange-selected', selectedExchange.value)
  } else {
    // "한국 원"이 선택된 경우에는 변환을 하지 않음
    convertedAmount.value = null
  }
}
</script>

<style scoped>
select, input {
  margin: 10px 0;
  padding: 5px;
}

div {
  max-width: 400px;
  margin: 0 auto;
}
</style>
