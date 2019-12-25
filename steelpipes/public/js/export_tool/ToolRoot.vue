<template>
  <div>
    <DemoChart/>
  </div>
</template>

<script>
import ButtonCounter from "./components/ButtonCounter.vue";
import DemoChart from "./components/DemoChart.vue"
export default {
  name: "ToolRoot",
  data: function() {
    return {
      some_data: "sample data"
    };
  },
  components: {
    ButtonCounter,
    DemoChart
  }
};
</script>
