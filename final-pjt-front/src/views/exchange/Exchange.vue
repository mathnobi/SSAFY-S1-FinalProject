<template>
  <div class="exchange-container">
    <h1>환율 알려드립니다.</h1>
    <h2>환율 계산기</h2>
    
    <ExchangeList 
      :exchanges="counterStore.exchange" 
      @exchange-selected="updateSelectedExchange"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import ExchangeList from './ExchangeList.vue'

const counterStore = useCounterStore()
const selectedExchange = ref(null)

const updateSelectedExchange = (exchange) => {
  selectedExchange.value = exchange
}

onMounted(() => {
  counterStore.getExchangeList()
})
</script>

<style scoped>
.exchange-container {
  margin: 30px 550px 10px 550px;
}
</style>
