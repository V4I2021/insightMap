<template>
    <div id="chart-box" ref="test">
        <div id="chart-text">
            {{ insight["insight_name"] }}
        </div>
        <div ref="chart" id="chart"/>
    </div>
</template>

<script>
import * as d3 from "d3";

export default {
    name: "ChartBox",
    props: {
        insight: {}
    },
    methods: {
        drawChart() {
            // todo: sentence
            const numberFormatter = d3.format("~s");
            // const longNameFormatter = this.longNameFormatter;
            const item = this.insight;

            let myChart = this.$echarts.getInstanceByDom(this.$refs["chart"]);
            if (myChart == null) {
                myChart = this.$echarts.init(this.$refs["chart"]);
            }

            const grid =
                    {
                        top: "30px",
                        left: "40px",
                        right: "10px",
                        bottom: "35px"
                    };
            // {
            //     top: "30px",
            //     left: "70px",
            //     right: "30px",
            //     bottom: "60px"
            // };

            const xAxisConfig = {
                nameLocation: "center",
                nameTextStyle: {
                    padding: [5, 0, 0, 0],
                    fontSize: 11,
                    // padding: [15, 0, 0, 0],
                    // fontSize: 17,
                }
            };

            const yAxisConfig = {
                nameLocation: "end",
                nameTextStyle: {
                    rotate: "90",
                    padding: [0, 0, -5, 0],
                    fontSize: 11,
                },
                // nameLocation: "center",
                // nameTextStyle: {
                //     padding: [0, 0, 25, 0],
                //     fontSize: 17,
                // },
            };

            if (item["insight_name"] === "Top1") {
                myChart.setOption(
                        {
                            grid: grid,
                            xAxis: {
                                name: item["breakdown"],
                                ...xAxisConfig,
                                type: "category",
                                data: item["breakdown_value"],
                            },
                            yAxis: {
                                name: item["measure"],
                                ...yAxisConfig,
                                type: "value",
                                splitNumber: 5,
                                axisLabel: {
                                    formatter: function (value) {
                                        return numberFormatter(value);
                                    }
                                },
                            },
                            series: [
                                {
                                    data: item["measure_value"],
                                    type: "bar",
                                    showBackground: true,
                                    backgroundStyle: {
                                        color: "rgba(180, 180, 180, 0.2)"
                                    },
                                }
                            ]
                        },
                        true
                );
            } else if (item["insight_name"] === "Trend") {
                myChart.setOption(
                        {
                            grid: grid,
                            xAxis: {
                                name: item["breakdown"],
                                ...xAxisConfig,
                                type: "category",
                                data: item["breakdown_value"],
                                axisLabel: {
                                    interval: 9,
                                }
                            },
                            yAxis: {
                                name: item["measure"],
                                ...yAxisConfig,
                                type: "value",
                                axisLabel: {
                                    formatter: function (value) {
                                        return numberFormatter(value);
                                    }
                                },
                            },
                            series: [
                                {
                                    data: item["measure_value"],
                                    type: "line",
                                    smooth: true,
                                    showSymbol: false,
                                    itemStyle: {
                                        normal: {
                                            color: "#a2d3f5",
                                            lineStyle: {
                                                color: "#1d77b9",
                                            },
                                        },
                                    }
                                }
                            ]
                        },
                        true
                );
            } else if (item["insight_name"] === "Correlation") {
                myChart.setOption(
                        {
                            grid: grid,
                            legend: {
                                right: "10", // "20",
                                data: item["breakdown_value"]
                            },
                            xAxis: {
                                name: item["time_col"],
                                ...xAxisConfig,
                                type: "category",
                                splitNumber: 3,
                                data: item["time_col_value"],
                                axisLabel: {
                                    interval: 9,
                                }
                            },
                            yAxis: {
                                name: item["measure"],
                                ...yAxisConfig,
                                type: "value",
                                splitNumber: 5,
                                axisLabel: {
                                    formatter: function (value) {
                                        return numberFormatter(value);
                                    }
                                },
                            },
                            series: [
                                {
                                    name: item["breakdown_value"][0],
                                    data: item["measure_value"][0],
                                    type: "line",
                                    smooth: true,
                                    showSymbol: false,
                                },
                                {
                                    name: item["breakdown_value"][1],
                                    data: item["measure_value"][1],
                                    type: "line",
                                    smooth: true,
                                    showSymbol: false,
                                }
                            ]
                        },
                        true
                );
            } else if (item["insight_name"] === "Outlier" || item["insight_name"] === "Change Point") {
                myChart.setOption(
                        {
                            grid: grid,
                            xAxis: {
                                name: item["breakdown"],
                                ...xAxisConfig,
                                type: "category",
                                data: item["breakdown_value"],
                                axisLabel: {
                                    interval: 9,
                                }
                            },
                            yAxis: {
                                name: item["measure"],
                                ...yAxisConfig,
                                type: "value",
                                splitNumber: 5,
                                axisLabel: {
                                    formatter: function (value) {
                                        return numberFormatter(value);
                                    }
                                },
                            },
                            series: [
                                {
                                    data: item["measure_value"],
                                    type: "line",
                                    smooth: true,
                                    showSymbol: false,
                                    itemStyle: {
                                        normal: {
                                            color: "#a2d3f5",
                                            lineStyle: {
                                                color: "#1d77b9",
                                            },
                                        },
                                    },
                                    markPoint: {
                                        symbol: "circle",
                                        symbolSize: 10, // 30
                                        data: [
                                            {
                                                name: item["insight_name"],
                                                xAxis: item["x"],
                                                yAxis: item["y"],
                                                itemStyle: {
                                                    color: "#ee6666",
                                                }
                                            }
                                        ]
                                    },
                                }
                            ]
                        },
                        true
                );
            } else if (item["insight_name"] === "Attribution") {
                let data = [];
                item["breakdown_value"].forEach((val, i) => {
                    data.push({"value": item["measure_value"][i], "name": val});
                });

                myChart.setOption(
                        {
                            series: [
                                {
                                    name: "Access From",
                                    type: "pie",
                                    radius: ["50%", "90%"],
                                    itemStyle: {
                                        borderRadius: 10,
                                        borderColor: "#fff",
                                        borderWidth: 2
                                    },
                                    label: {
                                        show: false,
                                        position: "center"
                                    },
                                    emphasis: {
                                        label: {
                                            show: true,
                                            fontSize: "18", // 40
                                            fontWeight: "bold"
                                        }
                                    },
                                    labelLine: {
                                        show: false
                                    },
                                    data: data,
                                }
                            ]
                        },
                        true
                );
            } else if (item["insight_name"] === "Cross Measure Correlation") {
                const cnt = item["x_value"].length;
                const minX = item["x_value"][0], maxX = item["x_value"][cnt - 1],
                        maxY = Math.max(item["line_y_value"][1], item["y_value"][cnt - 1]);

                let data = [];
                item["x_value"].forEach((val, i) => {
                    data.push([val, item["y_value"][i]]);
                });

                myChart.setOption(
                        {
                            tooltip: {
                                formatter: "{c}"
                            },
                            grid: grid,
                            xAxis: {
                                name: item["measures"][0],
                                ...xAxisConfig,
                                splitNumber: 3,
                                axisLabel: {
                                    formatter: function (value) {
                                        return numberFormatter(value);
                                    }
                                },
                            },
                            yAxis: {
                                name: item["measures"][1],
                                ...yAxisConfig,
                                max: maxY,
                                splitNumber: 5,
                                axisLabel: {
                                    formatter: function (value) {
                                        return numberFormatter(value);
                                    }
                                },
                            },
                            series: [
                                {
                                    type: "scatter",
                                    data: data,
                                    markLine: {
                                        animation: false,
                                        lineStyle: {
                                            type: "solid"
                                        },
                                        data: [[
                                            {
                                                coord: [minX, item["line_y_value"][0]],
                                                symbol: "none"
                                            },
                                            {
                                                coord: [maxX, item["line_y_value"][1]],
                                                symbol: "none"
                                            }
                                        ]]
                                    }
                                }
                            ]
                        },
                        true
                );
            } else if (item["insight_name"] === "Clustering") {
                let groups = {};

                item["x_value"].forEach((val, i) => {
                    const label = item["label"][i];
                    if (!(label in groups)) {
                        groups[label] = [];
                    }
                    groups[label].push([val, item["y_value"][i]]);
                });

                let series = [];
                Object.keys(groups).forEach((key, i) => {
                    const config = {
                        data: groups[key],
                        type: "scatter",
                        emphasis: {
                            focus: "series"
                        },
                    };

                    if (key === "-1") {
                        series.push({
                            name: "noise",
                            itemStyle: {
                                color: "grey"
                            },
                            ...config,
                        });
                    } else {
                        series.push({
                            name: `group${i}`,
                            ...config
                        });
                    }
                });

                myChart.setOption(
                        {
                            tooltip: {
                                formatter: "{c}"
                            },
                            legend: {
                                right: "10", // "20",
                                data: ["noise"]
                            },
                            grid: grid,
                            xAxis: {
                                name: item["measures"][0],
                                ...xAxisConfig,
                                splitNumber: 3,
                                axisLabel: {
                                    formatter: function (value) {
                                        return numberFormatter(value);
                                    }
                                },
                            },
                            yAxis: {
                                name: item["measures"][1],
                                ...yAxisConfig,
                                splitNumber: 5,
                                axisLabel: {
                                    formatter: function (value) {
                                        return numberFormatter(value);
                                    }
                                },
                            },
                            series: series
                        },
                        true
                );
            }
        },
        longNameFormatter(size, value) {
            if (value.indexOf(" ") !== -1) {
                return value.substring(0, value.indexOf(" "));
            } else if (value.length > size) {
                return value.substring(0, size - 3) + "...";
            } else {
                return value;
            }
        }
    }
};
</script>

<style scoped>
#chart-box {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
}

#chart-text {
    font-weight: bold;
    font-size: 11px;
    margin: 3px 0 0 3px;
    /*font-size: 20px;*/
    /*margin: 10px 0 0 10px;*/
}

#chart {
    flex: auto;
}
</style>
