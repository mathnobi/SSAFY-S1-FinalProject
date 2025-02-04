<template>
  <tr>
    <td>{{ deposit.kor_co_nm }}</td>
    <td>{{ deposit.fin_prdt_nm }}</td>
    <td v-if="!selectedTerm || selectedTerm === 3">{{ getRateByTerm(3) }}%</td>
    <td v-if="!selectedTerm || selectedTerm === 6">{{ getRateByTerm(6) }}%</td>
    <td v-if="!selectedTerm || selectedTerm === 12">{{ getRateByTerm(12) }}%</td>
    <td v-if="!selectedTerm || selectedTerm === 24">{{ getRateByTerm(24) }}%</td>
    <td>
      <RouterLink class="link" :to="{ name: 'DepositDetail', params: { id: deposit.fin_prdt_cd }}">
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
  deposit: Object,
  selectedTerm: {
    type: [Number, String],
    default: ''
  }
})

const store = useCounterStore()
const options = ref([])

const getRateByTerm = (term) => {
  const option = options.value.find(opt => opt.save_trm === term)
  return option ? option.intr_rate : '-'
}

onMounted(async () => {
  try {
    const response = await axios({
      method: 'get',
      url: `${store.API_URL}/deposits/deposit-products-options/${props.deposit.fin_prdt_cd}`,
    })
    options.value = response.data
  } catch (err) {
    console.log(err)
    options.value = []
  }
})
</script>

<style scoped>
/* RouterLink의 밑줄 제거 */
.link {
  text-decoration: none;
  color: black;
}
</style>