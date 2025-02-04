<template>
  <section class="container">
    <!-- 프로필 영역 -->
    <div class="top-area">
      <div class="profile-area">
        <span>금융상품 추천 챗봇</span>
      </div>
    </div>
    
    <!-- 채팅 영역 -->
    <div class="chat-area">
      <div
        v-for="(message, index) in chatMessages"
        :key="index"
        :class="['chat', message.type === 'send' ? 'send-chat' : 'receive-chat']"
      >
        {{ message.content }}
      </div>
    </div>
    
    <!-- 채팅창 하단 영역 -->
    <div class="bottom-area">
      <input
        class="chat-input"
        type="text"
        placeholder="원하시는 금융상품 조건을 입력해주세요..."
        v-model="userMessage"
        @keyup.enter="handleSubmit"
      />
    </div>
  </section>
</template>

<script>
import { useGptStore } from "@/stores/gpt";
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const gptStore = useGptStore();
    const userMessage = ref("");
    const financialProducts = ref([]);

    // 금융상품 데이터 가져오기
    const fetchFinancialProducts = async () => {
      try {
        const [depositResponse, savingsResponse] = await Promise.all([
          axios.get("http://localhost:8000/deposits/deposit-products/"),
          axios.get("http://localhost:8000/deposits/savings-products/"),
        ]);

        const deposits = depositResponse.data || [];
        const savings = savingsResponse.data || [];

        financialProducts.value = [
          ...deposits.map(product => ({
            name: product.fin_prdt_nm,
            bank: product.kor_co_nm,
            description: product.etc_note,
            joinRestriction: product.join_deny === 1
              ? "제한없음"
              : product.join_deny === 2
              ? "서민전용"
              : "일부 제한",
            joinTarget: product.join_member,
            joinMethod: product.join_way,
            specialCondition: product.spcl_cnd || "없음",
            type: "예금",
          })),
          ...savings.map(product => ({
            name: product.fin_prdt_nm,
            bank: product.kor_co_nm,
            description: product.etc_note,
            joinRestriction: product.join_deny === 1
              ? "제한없음"
              : product.join_deny === 2
              ? "서민전용"
              : "일부 제한",
            joinTarget: product.join_member,
            joinMethod: product.join_way,
            specialCondition: product.spcl_cnd || "없음",
            type: "적금",
          })),
        ];
      } catch (error) {
        console.error('금융상품 데이터 가져오기 실패:', error);
        gptStore.addChat('receive', '죄송합니다. 금융상품 데이터를 가져오는데 실패했습니다.');
      }
    };

    // 사용자 메시지 분석 및 상품 추천
    const analyzeUserMessage = (message) => {
      const keywords = {
        예금: ['예금', '입출금', '예치'],
        적금: ['적금', '저축', '매월'],
        서민: ['서민', '저소득', '취약계층'],
        학생: ['학생', '대학생', '청년'],
      };

      let recommendedProducts = [...financialProducts.value];

      // 상품 종류 필터링
      if (message.includes('예금')) {
        recommendedProducts = recommendedProducts.filter(p => p.type === '예금');
      } else if (message.includes('적금')) {
        recommendedProducts = recommendedProducts.filter(p => p.type === '적금');
      }

      // 가입 대상 필터링
      if (message.includes('서민')) {
        recommendedProducts = recommendedProducts.filter(p => 
          p.joinRestriction === '서민전용' || p.joinTarget.includes('서민')
        );
      }

      // 상위 3개 상품 추천
      return recommendedProducts.slice(0, 3);
    };

    // 챗봇 응답 생성
    const generateResponse = (products) => {
      if (products.length === 0) {
        return '죄송합니다. 조건에 맞는 상품을 찾지 못했습니다.';
      }

      let response = '다음과 같은 상품들을 추천드립니다:\n\n';
      products.forEach((product, index) => {
        response += `${index + 1}. ${product.name} (${product.bank})\n`;
        response += `   - 상품 유형: ${product.type}\n`;
        response += `   - 가입 대상: ${product.joinTarget}\n`;
        response += `   - 우대 조건: ${product.specialCondition}\n\n`;
      });

      return response;
    };

    // 메시지 제출 처리
    const handleSubmit = async () => {
      if (!userMessage.value) return;

      // 상품 추천 로직 실행
      const recommendedProducts = analyzeUserMessage(userMessage.value);
      const response = generateResponse(recommendedProducts);

      // GPT 응답과 상품 추천을 결합
      await gptStore.sendChat(userMessage.value);
      gptStore.addChat('receive', response);

      userMessage.value = "";
    };

    // 컴포넌트 마운트 시 금융상품 데이터 가져오기
    onMounted(() => {
      fetchFinancialProducts();
      gptStore.addChat('receive', '안녕하세요! 원하시는 금융상품 조건을 말씀해주세요. (예: "청년을 위한 예금 추천해줘")');
    });

    return {
      userMessage,
      chatMessages: computed(() => gptStore.chatMessages),
      handleSubmit,
    };
  },
};
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 600px;
  height: 80vh;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
  background-color: #f9f0f9; /* 연보라색 톤의 배경 */
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.top-area {
  padding: 1rem;
  background-color: rgb(155, 154, 154); /* 부드러운 핑크색 */
  color: rgb(40, 40, 40); /* 다크 그레이 텍스트 */
  /* border-bottom: 1px solid black; 약간의 회색-핑크 톤의 경계선 */
}

.profile-area {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.profile-area span {
  font-size: 1.2rem;
  font-weight: 600;
  color: rgb(40, 40, 40); /* 다크 그레이 */
}

.chat-area {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  background-color: rgb(226, 225, 225); /* 연보라색 배경 */
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chat {
  max-width: 70%;
  padding: 0.8rem 1rem;
  border-radius: 12px;
  white-space: pre-line;
  line-height: 1.4;
}

.send-chat {
  align-self: flex-end;
  background-color: darkgray; 
  font-style: white;
  color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.receive-chat {
  align-self: flex-start;
  background-color: whitesmoke; /* 연보라색 */
  color: rgb(40, 40, 40); /* 다크 그레이 */
  border-radius: 8px;
  font-size: large;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.bottom-area {
  padding: 1rem;
  background-color: lightgray;
  border-top: 1px solid lightgray; /* 회색-핑크 톤의 경계선 */
}

.chat-input {
  width: 94%;
  padding: 0.8rem 1rem;
  border: 2px solid black; /* 핑크색 */
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s, background-color 0.2s;
  background-color: white;
}

.chat-input:focus {
  border-color: gray; /* 연한 핑크 */
  background-color: white; /* 연보라색 배경 */
}

/* Scrollbar Styling */
.chat-area::-webkit-scrollbar {
  width: 8px;
}

.chat-area::-webkit-scrollbar-track {
  background: lightgray; /* 연한 회색 */
}

.chat-area::-webkit-scrollbar-thumb {
  background: gray;
  border-radius: 4px;
}

/* .chat-area::-webkit-scrollbar-thumb:hover {
  background: #ec9ce5;
} */

</style>
