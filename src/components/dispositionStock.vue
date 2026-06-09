<template>
  <div class="container">
    <h2>處置股票清單</h2>

    <p v-if="lastUpdated">
      更新時間：{{ lastUpdated }} ｜ 共 {{ count }} 筆
    </p>

    <table border="1" cellpadding="6">
      <thead>
        <tr>
          <th>市場</th>
          <th>代碼</th>
          <th>名稱</th>
          <th>開始</th>
          <th>結束</th>
          <th>撮合</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="item in list" :key="item.code">
          <td>{{ item.market }}</td>
          <td>{{ item.code }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.start_date }}</td>
          <td>{{ item.end_date }}</td>
          <td>{{ getMatchTime(item) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const list = ref([])
const lastUpdated = ref('')
const count = ref(0)

onMounted(async () => {
  const res = await fetch('/data/disposition.json')
  const data = await res.json()

  list.value = data.disposition_list
  lastUpdated.value = data.last_updated
  count.value = data.disposition_count
})

/**
 * 解析撮合時間
 */
function getMatchTime(item) {
  const text = item.details || ''

  if (text.includes('每五分鐘')) return '5分鐘'
  if (text.includes('每二十分鐘')) return '20分鐘'
  if (text.includes('每六十分鐘')) return '60分鐘'
  
  // fallback（有些寫在 measures）
  if (item.measures?.includes('5分鐘')) return '5分鐘'

  return '一般撮合'
}

</script>

<style scoped>
.container {
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: #f3f3f3;
}
</style>