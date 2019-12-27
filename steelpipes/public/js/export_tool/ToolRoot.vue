<template>
  <div>
    <FrappeChart/>
  </div>
</template>

<script>
import FrappeChart from "./components/FrappeChart.vue"
export default {
  name: "ToolRoot",
  data: function() {
    return {
      some_data: "sample data"
    };
  },
  components: {
    FrappeChart
  }
};
</script>
