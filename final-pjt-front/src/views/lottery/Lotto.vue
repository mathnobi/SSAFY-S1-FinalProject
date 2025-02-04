<template>
  <div>
    <h1>🎰로또 번호 추출기🎰</h1>
    <button class="lottery-btn" @click="getLottery">💰행운 번호 받기💰</button>
    
    <div class="lottery-stats">
      <span>추출 횟수: {{ lotteryHistory.length }}회</span>
    </div>

    <!-- 최신 로또 번호 (가장 위에 표시) -->
    <ul v-if="currentNumbers.length > 0" class="current-numbers">
      <li v-for="number in currentNumbers" :key="number" class="current">
        {{ number }}
      </li>
    </ul>

    <!-- 로또 번호 히스토리 (최신 번호 아래에 표시) -->
    <div class="history-container">
      <div v-for="(numbers, index) in lotteryHistory" :key="index" class="history-item">
        <span class="history-count">{{ lotteryHistory.length - index }}회차: </span>
        <ul>
          <li v-for="number in numbers" :key="number">
            {{ number }}
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div class="link-margin">
    <a href="https://dhlottery.co.kr/common.do?method=main" class="link">💰</a>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 현재 로또 번호를 저장할 반응형 배열
const currentNumbers = ref([])

// 로또 번호 히스토리를 저장할 반응형 배열
const lotteryHistory = ref([])

// 로또 번호를 생성하는 함수
const getNumbers = () => {
  // 1부터 45까지의 배열 생성
  const numbers = Array.from({length: 45}, (_, i) => i + 1)
  
  // 배열에서 랜덤으로 6개 번호 추출
  const shuffled = numbers.sort(() => 0.5 - Math.random())
  return shuffled.slice(0, 6).sort((a, b) => a - b)
}

// 로또 번호를 추출하고 화면에 표시하는 함수
const getLottery = () => {
  // 새로운 로또 번호 생성
  const newNumbers = getNumbers()
  
  // 현재 번호를 히스토리에 추가
  currentNumbers.value = newNumbers
  lotteryHistory.value.unshift(newNumbers)
}
</script>

<style scoped>
h1 {
  border-radius: 5px;
}

.lottery-btn {
  background-color: #f6c552;
  padding: 10px 20px;
  border-radius: 5px;
  font-weight: bold;
  font-size: 16px;
}

.lottery-stats {

  font-size: 16px;
  font-weight: bold;

  padding: 10px 0;
  border-radius: 5px;
}

.current-numbers {
  display: flex;
  list-style-type: none;
  padding: 10px;
  gap: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
}

.current-numbers li {
  background-color: #495057;
  color: white;
  padding: 10px;
  border-radius: 5px;
  font-size: 18px;
  font-weight: bold;

  width: 40px;  /* 가로 크기 */
  height: 40px; /* 세로 크기 */
  display: flex; /* 내용 정렬을 위한 flexbox */
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  box-sizing: border-box; /* padding을 포함한 크기 계산 */
}


.history-container {
  overflow-y: auto;
}

.history-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;

  padding: 5px;
  border-radius: 5px;
}

.history-item ul {
  display: flex;
  list-style-type: none;
  padding: 0;
  margin: 0;
  gap: 10px;
}

.history-item li {
  background-color: #adb5bd;
  padding: 5px;
  border-radius: 3px;

  width: 35px;  /* 가로 크기 */
  height: 35px; /* 세로 크기 */
  display: flex; /* 내용 정렬을 위한 flexbox */
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  box-sizing: border-box; /* padding을 포함한 크기 계산 */
}

.history-count {
  margin-right: 10px;
  font-weight: bold;
}

.link {
  text-decoration: none;
  color: black;
  padding: 7px;
  /* background-color: #f1f3f5; */
  font-size: 1.5rem;
  border-radius: 5px;
}

.link-margin {
  margin-top: 10px;
}
</style>