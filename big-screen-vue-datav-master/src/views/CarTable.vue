<template>
  <div id="carTable" class="bg-color-black">
    <div class="d-flex pt-2 pl-2">
      <span>
        <icon name="align-left" class="text-icon"></icon>
      </span>
      <span class="fs-xl text mx-2">车型列表</span>
    </div>
    <div class="d-flex jc-center body-box">
      <dv-scroll-board
        class="dv-scr-board"
        :config="config"
      />
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      config: {
        header: ['编号', '车型', '品牌', '价格(万)'],
        data: [],
        rowNum: 7,
        headerHeight: 35,
        headerBGC: '#0f1325',
        oddRowBGC: '#0f1325',
        evenRowBGC: '#171c33',
        index: false,
        columnWidth: [60, 120, 100, 80],
        align: ['center', 'left', 'left', 'center']
      }
    }
  },
  async mounted () {
    const res = await this.$http.get('myApp/cars/')
    this.config = { ...this.config, data: res.data.data }
  }
}
</script>

<style lang="scss" scoped>
$box-height: 410px;
$box-width: 360px;
#carTable {
  padding: 16px;
  height: $box-height;
  width: $box-width;
  border-radius: 5px;
  .bg-color-black {
    height: $box-height - 30px;
    border-radius: 10px;
  }
  .text {
    color: #c3cbde;
  }
  .body-box {
    border-radius: 10px;
    overflow: hidden;
    .dv-scr-board {
      width: 320px;
      height: 340px;
    }
  }
}
</style>