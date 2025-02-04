<template>
  <div class="deposit-container">
    <h1>예금금리 비교 페이지입니다.</h1>
    <h2>예금 데이터 목록</h2>

    <!-- 검색 필터 섹션 -->
    <div class="search-filters">
      <div class="filter-item">
        <label for="bankSelect">은행 선택:</label>
        <select id="bankSelect" v-model="selectedBank">
          <option value="">전체</option>
          <option v-for="bank in uniqueBanks" 
                  :key="bank" 
                  :value="bank">
            {{ bank }}
          </option>
        </select>
      </div>

      <div class="filter-item">
        <label for="termSelect">예치기간:</label>
        <select id="termSelect" v-model="selectedTerm">
          <option value="">전체</option>
          <option v-for="term in [3, 6, 12, 24]" 
                  :key="term" 
                  :value="term">
            {{ term }}개월
          </option>
        </select>
      </div>
    </div>

    <table class="deposit-table">
      <thead>
        <tr>
          <th>금융 회사</th>
          <th>금융 상품명</th>
          <th v-if="!selectedTerm || selectedTerm === 3">3개월</th>
          <th v-if="!selectedTerm || selectedTerm === 6">6개월</th>
          <th v-if="!selectedTerm || selectedTerm === 12">12개월</th>
          <th v-if="!selectedTerm || selectedTerm === 24">24개월</th>
          <th>상세보기</th>
        </tr>
      </thead>
      <tbody>
        <DepositList
          v-for="deposit in filteredDeposits"
          :key="deposit.id"
          :deposit="deposit"
          :selected-term="selectedTerm"
        />
      </tbody>
    </table>
  </div>
</template>

<script setup>
import DepositList from '@/components/deposits/DepositList.vue'
import { ref, computed, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'

const counterStore = useCounterStore()
const selectedBank = ref('')
const selectedTerm = ref('')

// 은행 목록 생성
const uniqueBanks = computed(() => {
  const banks = counterStore.deposits.map(deposit => deposit.kor_co_nm)
  return [...new Set(banks)].sort()
})

// 필터링된 예금 상품 목록
const filteredDeposits = computed(() => {
  let filtered = counterStore.deposits

  if (selectedBank.value) {
    filtered = filtered.filter(deposit => deposit.kor_co_nm === selectedBank.value)
  }

  return filtered
})

onMounted(() => {
  counterStore.getDepositList()
})
</script>

<style scoped>
.deposit-container {
  margin: 30px 550px 10px 550px;
}


.search-filters {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.deposit-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

.deposit-table th,
.deposit-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.deposit-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.deposit-table tr:hover {
  background-color: #f9f9f9;
}

.deposit-table a {
  color: #007bff;
  text-decoration: none;
}

.deposit-table a:hover {
  text-decoration: underline;
}
</style>