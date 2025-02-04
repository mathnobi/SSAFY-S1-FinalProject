<template>
  <tr v-if="savings">
    <td>{{ savings.kor_co_nm }}</td>
    <td>{{ savings.fin_prdt_nm }}</td>
    <td v-if="!selectedTerm || selectedTerm === 3">{{ getRateByTerm(3) }}</td>
    <td v-if="!selectedTerm || selectedTerm === 6">{{ getRateByTerm(6) }}</td>
    <td v-if="!selectedTerm || selectedTerm === 12">{{ getRateByTerm(12) }}</td>
    <td v-if="!selectedTerm || selectedTerm === 24">{{ getRateByTerm(24) }}</td>
    <td>
      <RouterLink 
        :to="{ 
          name: 'SavingsDetail', 
          params: { id: savings.fin_prdt_cd }
        }"
        class="text-blue-600 hover:text-blue-800 link"
      >
        상세 조회
      </RouterLink>
    </td>
  </tr>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'

const props = defineProps({
  savings: {
    type: Object,
    required: true,
    default: () => ({})
  },
  selectedTerm: {
    type: [Number, String],
    default: ''
  }
})

const store = useCounterStore()
const options = ref([])
const loading = ref(true)
const error = ref(null)

const getRateByTerm = (term) => {
  if (!options.value?.length) return '-'
  
  const option = options.value.find(opt => Number(opt.save_trm) === Number(term))
  if (!option) return '-'
  
  return option.intr_rate ? `${option.intr_rate}%` : '-'
}

const fetchOptions = async () => {
  if (!props.savings?.fin_prdt_cd) return
  
  try {
    loading.value = true
    const response = await axios({
      method: 'get',
      url: `${store.API_URL}/deposits/savings-products-options/${props.savings.fin_prdt_cd}`,
    })
    options.value = response.data || []
  } catch (err) {
    console.error('금리 정보 조회 실패:', err)
    error.value = err
    options.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchOptions()
})
</script>

<style scoped>
/* RouterLink의 밑줄 제거 */
.link {
  text-decoration: none;
  color: black;
}
</style>