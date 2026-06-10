const { createApp, defineComponent } = Vue;

const files = [
  './data/data.json',
  './data/data_meetings.json',
  './data/data_global.json'
];

Promise.all(files.map(f => fetch(f).then(r => r.json())))
  .then(([dispositionStockList, investorConferenceList, stockIndexList]) => {

    // =========================
    // 處置股票
    // =========================
    const dispositionStock = defineComponent({
      template: `
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
      </div>
      `,
      data() {
        return {
          list: dispositionStockList.disposition_list || [],
          lastUpdated: dispositionStockList.last_updated,
          count: dispositionStockList.disposition_count
        };
      },
      methods: {
        getMatchTime(item) {
          const text = item.details || '';

          if (text.includes('每五分鐘')) return '5分鐘';
          if (text.includes('每二十分鐘')) return '20分鐘';
          if (text.includes('每六十分鐘')) return '60分鐘';

          if (item.measures?.includes('5分鐘')) return '5分鐘';

          return '一般撮合';
        }
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

    // =========================
    // 法說會
    // =========================
    const investorConference = defineComponent({
      template: `
      <div class="container">
        <h2>法說會列表</h2>

        <p v-if="lastUpdated">
          更新時間：{{ lastUpdated }}
        </p>

        <table border="1" cellpadding="6">
          <thead>
            <tr>
              <th>日期</th>
              <th>公司</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="item in list" :key="item.公司 + item.日期">
              <td>{{ item.日期 }}</td>
              <td>{{ item.公司 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      `,
      data() {
        return {
          list: investorConferenceList.company_list || [],
          lastUpdated: investorConferenceList.last_updated
        };
      }
    });

    createApp(investorConference).mount('#investorConference');

    // =========================
    // 指數
    // =========================
    const stockIndex = defineComponent({
      template: `
      <div class="container">
        <h2>指數</h2>

        <p v-if="lastUpdated">
          更新時間：{{ lastUpdated }}
        </p>

        <table border="1" cellpadding="6">
          <thead>
            <tr>
              <th>名稱</th>
              <th>價格</th>
              <th>漲跌</th>
              <th>漲跌幅</th>
              <th>訊號</th>
              <th>時間</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="item in list" :key="item.item_name">
              <td>{{ item.item_name }}</td>
              <td>{{ item.current_price }}</td>
              <td>{{ item.price_change }}</td>
              <td>{{ item.price_change_percent }}</td>
              <td>{{ item.status_signal }}</td>
              <td>{{ item.last_trade_time }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      `,
      data() {
        return {
          list: stockIndexList.market_indices || [],
          lastUpdated: stockIndexList.last_updated
        };
      }
    });

    createApp(stockIndex).mount('#stockIndex');

  });