<template>
  <div>
    <div>
      <span>
        <button v-on:click="gchart" class="btn btn-primary border">
          Generate Chart
        </button></span
      >
      <span id="fortest"
        >Button clicked
        <span class="badge badge-success">{{ time }}</span> time(s)</span
      >
      <a>
        <button v-on:click="changedata" class="btn btn-danger border">
          Change Data
        </button>
      </a>
    </div>

    <div id="totalPipeSold"></div>
    <div id="individualPipeSold"></div>
  </div>
</template>

<script>
import { total_pipe_sold_options } from "../chart_configs/total_pipes_sold.js";
import { individual_pipe_sold_options } from "../chart_configs/individual_pipe_sold.js";
import { individual_pipe_sold_options2 } from "../chart_configs/individual_pipe_sold.js";

export default {
  data: function() {
    return {
      time: 0,
      switch: true,
      fromchart: true,
      total_pipe_sold_chart: null,
      total_pipe_sold: total_pipe_sold_options,
      individual_pipe_sold: null,
      individual_pipe_sold: individual_pipe_sold_options,
      individual_pipe_sold2: individual_pipe_sold_options2
    };
  },
  methods: {
    gchart: function() {
      if (this.time == 0) {
        // Total pipe sold chart
        this.total_pipe_sold_chart = new frappe.Chart(
          "#totalPipeSold",
          this.total_pipe_sold
        );
        this.total_pipe_sold_chart.parent.addEventListener("data-select", e => {
          console.log(
            "Index: " +
              e.index +
              " | Label: " +
              e.label +
              " | Value: " +
              e.values[0]
          );
          //changing data set:
          console.log("from total sold addEvent", this.fromchart);
          this.fromchart = !this.fromchart;
        });
        // Individual Pipe Sold Chart
        this.individual_pipe_sold_chart = new frappe.Chart(
          "#individualPipeSold",
          this.individual_pipe_sold
        );
        this.individual_pipe_sold_chart.parent.addEventListener(
          "data-select",
          e => {
            console.log(
              "Index: " +
                e.index +
                " | Label: " +
                e.label +
                " | Value: " +
                e.values[0] +
                " | time: " +
                this.time
            );
          }
        );
      }
      this.time += 1;
      console.log("Button clicked");
    },
    changedata: function() {
      console.log(this.fromchart, "from changedata");
    }
  },
  mounted() {}
};
</script>
