<template>
  <div class="profile-container">
    <div class="profile-form">
      <h1 class="profile-title">유저 프로필</h1>
      
      <div v-if="profile">
        <div class="input-group">
          <label for="username">이름</label>
          <span>{{ profile.username }}</span>
        </div>

        <div class="input-group">
          <label for="email">Email</label>
          <span>{{ profile.email }}</span>
        </div>

        <div class="input-group">
          <label for="age">나이</label>
          <span v-if="!isEditMode">{{ profile.age }}</span>
          <input v-else v-model="profile.age" type="number" class="input-field" />
        </div>

        <div class="input-group">
          <label for="gender">성별</label>
          <span v-if="!isEditMode">{{ profile.gender }}</span>
          <select v-else v-model="profile.gender" class="input-field">
            <option value="남">남</option>
            <option value="여">여</option>
          </select>
        </div>

        <div class="input-group">
          <label for="salary">연봉</label>
          <span v-if="!isEditMode">{{ profile.salary }}</span>
          <input v-else v-model="profile.salary" type="number" class="input-field" />
        </div>

        <div class="input-group">
          <label for="wealth">자산</label>
          <span v-if="!isEditMode">{{ profile.wealth }}</span>
          <input v-else v-model="profile.wealth" type="number" class="input-field" />
        </div>

        <div class="input-group">
          <label for="debt">빚</label>
          <span v-if="!isEditMode">{{ profile.debt }}</span>
          <input v-else v-model="profile.debt" type="number" class="input-field" />
        </div>

        <div class="input-group">
          <label for="tendency">성향</label>
          <span v-if="!isEditMode">{{ profile.tendency }}</span>
          <select v-else v-model="profile.tendency" class="input-field" required>
            <option value="1">고위험 고수익</option>
            <option value="2">중위험 중수익</option>
            <option value="3">저위험 저수익</option>
          </select>
        </div>

        <!-- 예금 상품들을 표로 출력 -->
        <h3>가입한 상품들</h3>
        <table v-if="parsedProducts.length > 0" class="product-table">
          <thead>
            <tr>
              <th>상품 번호</th>
              <th>은행명</th>
              <th>상품명</th>
              <th>저축금리</th>
              <th>최고우대금리</th>
              <th>저축기간 (개월)</th>
              <th v-if="isEditMode">삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(product, index) in parsedProducts" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ product.bank_name }}</td>
              <td>{{ product.product_name }}</td>
              <td>{{ product.intr_rate }}%</td>
              <td>{{ product.intr_rate2 }}%</td>
              <td>{{ product.save_trm }}개월</td>
              <td v-if="isEditMode"><button @click="deleteProduct(index)" class="edit-button">삭제</button></td>
            </tr>
          </tbody>
        </table>
        <p v-else>가입한 상품이 없습니다.</p>

        <button @click="toggleEditMode" class="edit-button">{{ isEditMode ? '저장' : '수정' }}</button>
      </div>
    </div>
  </div>
</template>

  
  <script setup>
  import axios from 'axios';
  import { ref, onMounted, computed } from 'vue';
  import { useRouter } from 'vue-router';
  import { useCounterStore } from '@/stores/counter';
  
  const store = useCounterStore();
  const router = useRouter(); 
  const token = localStorage.getItem('access_token');
  const profile = ref(null);
  const isEditMode = ref(false); // 수정 모드 상태
  const props = defineProps(['profile'])
  
  // 프로필 데이터를 로드하는 함수
  onMounted(() => {
    axios
      .get(`${store.API_URL}/accounts/profile/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      })
      .then((res) => {
        profile.value = res.data;
      })
      .catch((err) => {
        console.error('프로필 조회 오류:', err);
      });
  });

  const parsedProducts = computed(() => {
  if (profile.value && profile.value.products) {
    try {
      return JSON.parse(profile.value.products || '[]');
    } catch (e) {
      console.error('JSON 파싱 에러:', e);
      return [];
    }
  } else {
    return [];
    }
  });

  // 상품 삭제 함수
const deleteProduct = async (index) => {
  try {
    // 상품 목록에서 삭제할 상품 제거
    const updatedProducts = [...parsedProducts.value];
    updatedProducts.splice(index, 1);  // index에 해당하는 상품을 삭제

    // 서버에 삭제된 목록 저장
    const updateResponse = await axios.put(
      `${store.API_URL}/accounts/profile/`,
      {
        products: JSON.stringify(updatedProducts),  // 수정된 상품 목록
      },
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );

    // 상품 삭제 후 프로필 업데이트
    profile.value = updateResponse.data;
    alert('상품이 삭제되었습니다.');

  } catch (err) {
    console.error('상품 삭제 오류:', err);
    alert('상품 삭제에 실패했습니다.');
  }
};

  // 수정 모드 토글 함수
  const toggleEditMode = () => {
    if (isEditMode.value) {
      // 저장 클릭 시 프로필 업데이트
      axios
        .put(`${store.API_URL}/accounts/profile/`, {
          age: profile.value.age,
          gender: profile.value.gender,
          salary: profile.value.salary,
          wealth: profile.value.wealth,
          debt: profile.value.debt,
          tendency: profile.value.tendency,
          products: profile.value.products,
        }, {
          headers: {
            Authorization: `Token ${token}`,
          },
        })
        .then((res) => {
          profile.value = res.data;
          router.push('/profile/');  // 페이지 이동
          // console.log(profile.value.products)
        })
        .catch((err) => {
          console.error('프로필 업데이트 오류:', err);
        });
    }

  
  
    // 수정 모드 전환
    isEditMode.value = !isEditMode.value;
  };
  </script>
  
  <style scoped>
  /* 전체 페이지 스타일 */
  html, body {
    height: 100%;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: flex-start; /* 화면의 상단으로 위치하도록 설정 */
  }

  /* 유저 프로필을 감싸는 컨테이너 스타일 */
  .profile-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    height: 100%;
    width: 100%;
    padding-top: 50px; /* 화면 상단에서 50px 아래로 위치 */
  }

  /* 프로필 폼 스타일 */
  .profile-form {
    display: flex;
    flex-direction: column;
    gap: 20px; /* 각 항목 간 여백 */
    width: 500px;
    padding: 25px;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  /* 프로필 제목 스타일 */
  .profile-title {
    font-size: 1.8rem;
    color: #2c3e50;
    margin-bottom: 20px;
    font-weight: bold;
  }

  /* 각 입력 항목 스타일 */
  .input-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
    text-align: left;
  }

  .input-group label {
    font-size: 1.2rem;
    color: #2c3e50;
    margin-top: 15px;
    font-weight: bold;
  }

  /* 입력 필드 스타일 */
  .input-field, .input-group select {
    padding: 12px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: 100%;
    box-sizing: border-box;
  }

  /* 프로필 수정 버튼 스타일 */
  .edit-button {
    padding: 12px;
    background-color: gray;
    color: white;
    font-size: 1.1rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .edit-button:hover {
    background-color: gray;
  }

  /* 상품 목록 테이블 스타일 */
  .product-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }

  .product-table th, .product-table td {
    padding: 12px;
    text-align: center;
    border: 1px solid #ddd;
  }

  .product-table th {
    background-color: #f8f8f8;
    font-weight: bold;
  }

  /* 모바일 화면에서 폼과 입력 필드 크기 조정 */
  @media (max-width: 768px) {
    .profile-form {
      width: 100%;
      padding: 15px;
    }

    .input-field, .edit-button {
      font-size: 1.2rem;
    }

    .product-table th, .product-table td {
      font-size: 0.9rem;
      padding: 8px;
    }
  }

  </style>
  