<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md">
      <div class="col-12 col-sm-6 col-md-4" v-for="(asset, index) in assets" :key="index">
        <div style="border: 1px solid gray" class="q-pa-md cursor-pointer">
          <div class="text-h6">{{asset.symbol}}</div>
          <div class="q-mt-md">총 구매액: {{ numberWithCommas(asset.buy_amount.toFixed(0)) }}₩</div>
          <div class="q-mt-md">현재 자산가치: {{ numberWithCommas(asset.current_amount.toFixed(0)) }}₩</div>
          <div class="text-h6" :class="`text-${asset.current_amount > asset.buy_amount ? 'green' : 'red' }`">{{ (asset.current_amount  * 100 / asset.buy_amount - 100).toFixed(3) }} %</div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import {ref} from "vue";
import {api} from "boot/axios";
import {useRoute} from "vue-router";
import {Loading} from "quasar";

export default {
  name: "PlayerPage",
  setup() {
    const route = useRoute()
    function numberWithCommas(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
    const assets = ref([])
    function getAssets() {
      Loading.show()
      api.get(`/total_asset?query_s=groupBySymbol&player_id=${route.params.player}`).then((res) => {
        assets.value = res.data.data
      }).finally(() => {
        Loading.hide()
      })
    }
    getAssets()
    return {
      numberWithCommas,
      assets
    }
  }
}
</script>

<style scoped>

</style>
