total_pipe_sold_options = {
  data: {
    labels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    datasets: [{ values: [18, 40, 30, 35, 8, 52, 17, -4] }]
  },
  type: "line",
  lineOptions: {
    heatline: 1,
    regionFill: 1
  },
  // height: 350,
  colors: ["green"],
  isNavigable: true,
  tooltipOptions: {
    formatTooltipX: d => (d + "").toUpperCase(),
    formatTooltipY: d => d + " TONS"
  }
};

export var total_pipe_sold_options;
