individual_pipe_sold_options = {
  data: {
    labels: ["3/4", "1", "1 1/2", "2", "2 1/2", "3", "4", "5","6","7","8","10","12"],
    datasets: [{ values: [18, 40, 30, 35, 8, 52, 17, 4, 55, 23, 10, 33, 45] }]
  },
  type: "bar",
  // height: 350,
  colors: ["blue"],
  isNavigable: true,
  tooltipOptions: {
    formatTooltipX: d => (d + "").toUpperCase(),
    formatTooltipY: d => d + " TONS"
  }
};

individual_pipe_sold_options2 = {
  data: {
    labels: ["3/4", "1", "1 1/2", "2", "2 1/2", "3", "4", "5","6","7","8","10","12"],
    datasets: [{ values: [18, 40, 30, 35, -8, 5, 27, 4, 55, 23, 20, 13, 35] }]
  },
  type: "bar",
  // height: 350,
  colors: ["blue"],
  isNavigable: true,
  tooltipOptions: {
    formatTooltipX: d => (d + "").toUpperCase(),
    formatTooltipY: d => d + " TONS"
  }
};

export var individual_pipe_sold_options;
export var individual_pipe_sold_options2;
