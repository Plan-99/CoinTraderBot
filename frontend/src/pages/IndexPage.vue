<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md">
      <div class="col-12 col-sm-6 col-md-4" v-for="player in players" :key="player.id">
        <div style="border: 1px solid gray" class="q-pa-md cursor-pointer">
          <div class="text-h6">{{ player.name }}</div>
          <div>{{ player.description }}</div>
          <div class="q-mt-md">현재 금액: {{ numberWithCommas(player.current_amount.toFixed(0)) }}</div>
          <div class="text-h6" :class="`text-${player.current_amount > player.buy_amount ? 'green' : 'red' }`">{{ (player.current_amount  * 100 / player.buy_amount - 100).toFixed(3) }} %</div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import {defineComponent, ref} from 'vue'
import {api} from "boot/axios";

export default defineComponent({
  name: 'IndexPage',
  setup() {
    const players = ref([
      { id: 1, name: 'Player 1', description: '지지선과 저항선에 의한 트레이딩', buy_amount: 0, current_amount: 0 },
      { id: 2, name: 'Player 2', description: '상승/하락 추이에 따른 트레이딩', buy_amount: 0, current_amount: 0 },
      // { id: 3, name: 'Player 3', description: '신규 소식을 기반으로 한 트레이딩', buy_amount: 0, current_amount: 0 },
    ])

    function getPlayers() {
      api.get('/total_asset?query_s=groupByPlayer').then((res) => {
        players.value.forEach((p) => {
          console.log(res.data)
          const player = res.data.data.find((e) => p.id === e.player_id)
          if (player) {
            p.buy_amount = player.buy_amount
            p.current_amount = player.current_amount
          }
        })
      })
    }

    function numberWithCommas(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    getPlayers()

    return {
      players,
      numberWithCommas
    }
  }
})
</script>
