import { createApp, defineComponent } from 'vue';
import dispositionStockList from './data/data.json'
import investorConferenceList from './data/data_meetings.json'
import stockIndexList from './data/data_global.json'

const dispositionStock = defineComponent({
  template: `<div class="container">
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
        <tr v-for="item in sortedList" :key="item.code">
          <td>{{ item.market }}</td>
          <td>{{ item.code }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.start_date }}</td>
          <td>{{ item.end_date }}</td>
          <td>{{ getMatchTime(item) }}</td>
        </tr>
      </tbody>
    </table>
  </div>`,
  data() {
    return {
      list : dispositionStockList.disposition_list,
	  lastUpdated : dispositionStockList.last_updated, 
	  count : dispositionStockList.disposition_count
    }
  },
  methods: {
    getMatchTime(item) {
      onst text = item.details || ''

	  if (text.includes('每五分鐘')) return '5分鐘'
	  if (text.includes('每二十分鐘')) return '20分鐘'
	  if (text.includes('每六十分鐘')) return '60分鐘'
	  
	  // fallback（有些寫在 measures）
	  if (item.measures?.includes('5分鐘')) return '5分鐘'

	  return '一般撮合'
    },
  },
  computed: {
	  sortedList() {
		const latestMap = new Map();

		this.list.forEach(item => {
		  const existing = latestMap.get(item.code);
		  const itemDate = new Date(item.end_date);

		  if (!existing) {
			latestMap.set(item.code, item);
		  } else {
			const existingDate = new Date(existing.end_date);
			if (itemDate > existingDate) {
			  latestMap.set(item.code, item);
			}
		  }
		});

		return Array.from(latestMap.values()).sort(
		  (a, b) => new Date(a.end_date) - new Date(b.end_date)
		);
	  }
	}
});


createApp(dispositionStock).mount('#dispositionStock');



const investorConference = defineComponent({
  template: `<div class="container">
    <h2>法說會列表</h2>

    <p v-if="lastUpdated">
      更新時間：{{ lastUpdated }} ｜ 共 {{ count }} 筆
    </p>

    <table border="1" cellpadding="2">
      <thead>
        <tr>
          <th>日期</th>
          <th>公司</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="item in list" :key="item.公司">
          <td>{{ item.日期 }}</td>
          <td>{{ item.公司 }}</td>
        </tr>
      </tbody>
    </table>
  </div>`,
  data() {
    return {
      list : investorConferenceList.company_list,
	  lastUpdated : dispositionStockList.last_updated,
    }
  },
});


createApp(investorConference).mount('#investorConference');



const stockIndex = defineComponent({
  template: `<div class="container">
    <h2>指數</h2>

    <p v-if="lastUpdated">
      更新時間：{{ lastUpdated }} ｜ 共 {{ count }} 筆
    </p>

    <tr v-for="item in list" :key="item.item_name">
      <td>{{ item.item_name }}</td>
      <td>{{ item.current_price }}</td>
      <td>{{ item.price_change }}</td>
      <td>{{ item.price_change_percent }}</td>
      <td>{{ item.status_signal }}</td>
      <td>{{ item.last_trade_time }}</td>
    </tr>
  </div>`,
  data() {
    return {
      list : stockIndexList.market_indices, 
	  lastUpdated : stockIndexList.last_updated
    }
  },
  
});


createApp(stockIndex).mount('#stockIndex');
