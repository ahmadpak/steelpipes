<template>
  <div>
    <nav class="navbar navbar-light">
      <form class="form-inline">
        <button
          type="button"
          class="btn btn-default btn-sm dropdown-toggle"
          data-toggle="dropdown"
          aria-expanded="true"
        >
          <span class="hidden-xs">
            <span class="menu-btn-group-label" data-label="Select Period"
              ><span class="alt-underline">S</span>elect Period</span
            >
            <span class="caret"></span>
          </span>
          <span class="visible-xs">
            <i class="octicon octicon-triangle-down"></i>
          </span>
        </button>
        <ul class="dropdown-menu" role="Select Period">
          <li
            class="user-action"
            v-for="duration in durations"
            :key="duration.id"
          >
            <a
              class="grey-link dropdown-item"
              href="#"
              onclick="return false;"
              v-on:click="gchart"
            >
              <span class="menu-item-label" data-label="Stock Entry"
                ><span class="alt-underline"></span>{{ duration }}</span
              ></a
            >
          </li>
        </ul>
        <span
          v-on:click="changeResolution"
          class="btn btn-primary float-right"
          type="button"
        >
          Add Data Points
        </span>
        <span
          v-on:click="changeResolution"
          class="btn btn-primary float-right"
          type="button"
        >
          Remove Data Points
        </span>
      </form>
    </nav>
    <div>
      Period: <strong>{{ period }}</strong>
    </div>
    <div id="totalPipeSold"></div>
    <div id="individualPipeSold"></div>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      time: 0,
      durations: [
        "This Month",
        "This Quarter",
        "This Year",
        "Last Month",
        "Last Quarter",
        "Last Year"
      ],
      period: "Not Selected",
      resolution: 1,
      total_pipe_sold_chart: null,
      total_pipe_sold_data: null,
      individual_pipe_sold_chart: null,
      individual_pipe_sold_data: null
    };
  },
  computed: {},
  methods: {
    gchart: function(event) {
      this.period = event.toElement.innerText;
      // Calling method to fetch data
      frappe
        .call({
          method:
            "steelpipes.sp_dashboard.page.havenir_insight.havenir_insight.generate_total_pipe_labels_and_data_sets",
          args: {
            period: this.period,
            resolution: this.resolution
          }
        })
        .then(r => {
          this.total_pipe_sold_data = r.message[0];
          console.log(r.message[1])
        })
        .then(() => {
          this.total_pipe_sold_chart = new frappe.Chart("#totalPipeSold", {
            data: this.total_pipe_sold_data,
            title: "Total Pipes Sold in MT",
            type: "line",
            // height: 350,
            lineOptions: {
              dotSize: 6, // default: 4
              regionFill: 1, // default: 0
              xIsSeries: true,
              heatline: 1 // default: 0
            },
            tooltipOptions: {
              formatTooltipX: d => {
                if (d.includes("Week")) {
                  return d;
                } else {
                  return "Day " + d;
                }
              },
              formatTooltipY: d => d + " MT"
            },
            colors: ["green"],
            isNavigable: true
          });
          this.total_pipe_sold_chart.parent.addEventListener(
            "data-select",
            e => {
              console.log(
                "Index: " +
                  e.index +
                  " | Label: " +
                  e.label +
                  " | Value: " +
                  e.values[0]
              );
              //changing data set:
            }
          );
        });

      // Individual Pipe Sold Chart
      // this.individual_pipe_sold_chart = new frappe.Chart(
      //   "#individualPipeSold",
      //   this.individual_pipe_sold
      // );
      // this.individual_pipe_sold_chart.parent.addEventListener(
      //   "data-select",
      //   e => {
      //     console.log(
      //       "Index: " +
      //         e.index +
      //         " | Label: " +
      //         e.label +
      //         " | Value: " +
      //         e.values[0] +
      //         " | time: " +
      //         this.time
      //     );
      //   }
      // );
    },
    changeResolution: function(event) {
      console.log(event)
      if (
        this.resolution > 0 &&
        this.resolution < 4 &&
        this.period != "Not Selected"
      ) {
        if (event.toElement.innerText == "Add Data Points") {
          if (this.resolution == 2) {
            return;
          }
          this.resolution += 1;
        } else {
          if (this.resolution == 1) {
            return;
          }
          this.resolution -= 1;
        }
        frappe
          .call({
            method:
              "steelpipes.sp_dashboard.page.havenir_insight.havenir_insight.generate_total_pipe_labels_and_data_sets",
            args: {
              period: this.period,
              resolution: this.resolution
            }
          })
          .then(r => {
            this.total_pipe_sold_data = r.message[0];
          })
          .then(r => {
            this.total_pipe_sold_chart.update(this.total_pipe_sold_data);
          });
      }
    }
  },
  mounted() {}
};
</script>
