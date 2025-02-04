<template>
  <div class="map-container">
    <h1>은행 위치</h1>
    <div class="search-container">
      <input 
        v-model="locationKeyword" 
        placeholder="지역을 입력하세요 (예: 서울역)"
        @keyup.enter="handleSearch"
      />
      <input 
        v-model="bankKeyword" 
        placeholder="은행을 입력하세요 (예: 신한은행)"
        @keyup.enter="handleSearch"
      />
      <button @click="handleSearch">검색</button>
    </div>
    <div ref="mapContainer" style="width: 100%; height: 500px;"></div>
    
    <!-- 검색 결과 목록 -->
    <div id="menu_wrap">
      <ul id="placesList">
        <li v-for="(place, index) in searchResults" :key="index" class="item"
            @mouseover="handleListItemHover(place)"
            @mouseout="closeInfoWindow">
          <div class="info">
            <h5>{{ place.place_name }}</h5>
            <span>{{ place.road_address_name || place.address_name }}</span>
            <span class="tel">{{ place.phone }}</span>
          </div>
        </li>
      </ul>
      <div id="pagination">
        <a v-for="pageNum in totalPages" 
           :key="pageNum" 
           :class="{ on: currentPage === pageNum }"
           @click="changePage(pageNum)">
          {{ pageNum }}
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// 카카오맵 api 밑에다 넣기. 이거 env 파일 해야 할텐데 아직 거기까지 못알아봄.
const VITE_KAKAO_MAP_KEY = '728dbcc6159260d5c184352fde9af4e3';
const mapContainer = ref(null);
const locationKeyword = ref('');
const bankKeyword = ref('');
const map = ref(null);
const markers = ref([]);
const infowindow = ref(null);
const searchResults = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);

// 카카오맵 로드
const loadKakaoMap = () => {
  const script = document.createElement('script');
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${VITE_KAKAO_MAP_KEY}&libraries=services&autoload=false`;
  document.head.appendChild(script);
  
  script.onload = () => {
    window.kakao.maps.load(() => {
      console.log('Kakao maps library loaded');
      createMap();
    });
  };
};

// 맵 생성
const createMap = () => {
  if (!mapContainer.value) return;
  
  const options = {
    center: new window.kakao.maps.LatLng(37.552987, 126.972591),
    level: 3,
  };
  
  map.value = new window.kakao.maps.Map(mapContainer.value, options);
  infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1 });
};

// 마커 생성
const addMarker = (position, idx) => {
  const imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png';
  const imageSize = new window.kakao.maps.Size(36, 37);
  const imgOptions = {
    spriteSize: new window.kakao.maps.Size(36, 691),
    spriteOrigin: new window.kakao.maps.Point(0, (idx * 46) + 10),
    offset: new window.kakao.maps.Point(13, 37)
  };
  
  const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions);
  const marker = new window.kakao.maps.Marker({
    position: position,
    image: markerImage
  });
  
  marker.setMap(map.value);
  markers.value.push(marker);
  return marker;
};

// 마커 제거
const removeMarkers = () => {
  markers.value.forEach(marker => marker.setMap(null));
  markers.value = [];
};

// 검색 실행
const handleSearch = () => {
  if (!locationKeyword.value || !bankKeyword.value) {
    alert('지역과 은행명을 모두 입력해주세요!');
    return;
  }
  
  const ps = new window.kakao.maps.services.Places();
  const searchKeyword = `${locationKeyword.value} ${bankKeyword.value}`;
  
  ps.keywordSearch(searchKeyword, (data, status, pagination) => {
    if (status === window.kakao.maps.services.Status.OK) {
      searchResults.value = data;
      totalPages.value = pagination.last;
      currentPage.value = pagination.current;
      
      // 검색 결과 표시
      displayPlaces(data);
    } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
      alert('검색 결과가 존재하지 않습니다.');
      searchResults.value = [];
    } else if (status === window.kakao.maps.services.Status.ERROR) {
      alert('검색 중 오류가 발생했습니다.');
      searchResults.value = [];
    }
  });
};

// 검색 결과 표시
const displayPlaces = (places) => {
  removeMarkers();
  const bounds = new window.kakao.maps.LatLngBounds();
  
  places.forEach((place, idx) => {
    const placePosition = new window.kakao.maps.LatLng(place.y, place.x);
    const marker = addMarker(placePosition, idx);
    
    bounds.extend(placePosition);
    
    // 마커에 이벤트 리스너 추가
    window.kakao.maps.event.addListener(marker, 'mouseover', () => {
      displayInfowindow(marker, place.place_name);
    });
    
    window.kakao.maps.event.addListener(marker, 'mouseout', () => {
      infowindow.value.close();
    });
  });
  
  map.value.setBounds(bounds);
};

// 인포윈도우 표시
const displayInfowindow = (marker, title) => {
  const content = `<div style="padding:5px;z-index:1;">${title}</div>`;
  infowindow.value.setContent(content);
  infowindow.value.open(map.value, marker);
};

// 인포윈도우 닫기
const closeInfoWindow = () => {
  infowindow.value?.close();
};

// 목록 항목 호버 처리
const handleListItemHover = (place) => {
  const marker = markers.value[searchResults.value.indexOf(place)];
  displayInfowindow(marker, place.place_name);
};

// 페이지 변경
const changePage = (pageNum) => {
  const ps = new window.kakao.maps.services.Places();
  const searchKeyword = `${locationKeyword.value} ${bankKeyword.value}`;
  
  ps.keywordSearch(searchKeyword, (data, status, pagination) => {
    if (status === window.kakao.maps.services.Status.OK) {
      searchResults.value = data;
      currentPage.value = pageNum;
      displayPlaces(data);
    }
  }, { page: pageNum });
};

onMounted(() => {
  if (!window.kakao || !window.kakao.maps) {
    loadKakaoMap();
  } else {
    createMap();
  }
});
</script>

<style scoped>
.map-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-container {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.search-container input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex: 1;
}

.search-container button {
  padding: 8px 16px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

#menu_wrap {
  margin-top: 20px;
  padding: 20px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

#placesList {
  list-style: none;
  padding: 0;
}

.item {
  padding: 10px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.item:hover {
  background-color: #f5f5f5;
}

.info h5 {
  margin: 0 0 5px 0;
  font-size: 16px;
}

.info span {
  display: block;
  font-size: 14px;
  color: #666;
}

.tel {
  color: #009688;
}

#pagination {
  margin-top: 20px;
  text-align: center;
}

#pagination a {
  display: inline-block;
  margin: 0 5px;
  padding: 5px 10px;
  border-radius: 4px;
  color: #333;
  text-decoration: none;
  cursor: pointer;
}

#pagination a.on {
  background-color: #2196F3;
  color: white;
}
</style>