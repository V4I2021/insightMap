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
            // todo: 坐标轴名，sentence
            const numberFormatter = d3.format("~s");
            // const longNameFormatter = this.longNameFormatter;
            const item = this.insight;

            let myChart = this.$echarts.getInstanceByDom(this.$refs["chart"]);
            if (myChart == null) {
                myChart = this.$echarts.init(this.$refs["chart"]);
            }

            if (item["insight_name"] === "Top1") {
                myChart.setOption(
                        {
                            grid: {
                                top: "10px",
                                left: "40px",
                                right: "10px",
                                bottom: "20px"
                            },
                            xAxis: {
                                type: "category",
                                splitNumber: 3,
                                data: item["breakdown_value"],
                                // axisLabel: {
                                //     interval: 0,
                                //     formatter: function (value) {
                                //         return longNameFormatter(7, value);
                                //     }
                                // }
                            },
                            yAxis: {
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
                            grid: {
                                top: "10px",
                                left: "40px",
                                right: "10px",
                                bottom: "20px"
                            },
                            xAxis: {
                                type: "category",
                                splitNumber: 3,
                                data: item["breakdown_value"]
                            },
                            yAxis: {
                                type: "value",
                                // min: function (value) {
                                //   return 0;
                                // },
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
                            grid: {
                                top: "10px",
                                left: "40px",
                                right: "10px",
                                bottom: "20px"
                            },
                            xAxis: {
                                type: "category",
                                splitNumber: 3,
                                data: item["breakdown_value"]
                            },
                            yAxis: {
                                type: "value",
                                // min: function (value) {
                                //   return 0;
                                // },
                                axisLabel: {
                                    formatter: function (value) {
                                        return numberFormatter(value);
                                    }
                                },
                            },
                            series: [
                                {
                                    name: "1", // todo
                                    data: item["measure_value"][0],
                                    type: "line",
                                    smooth: true,
                                    showSymbol: false,
                                },
                                {
                                    name: "2", // todo
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
                            grid: {
                                top: "10px",
                                left: "40px",
                                right: "10px",
                                bottom: "20px"
                            },
                            xAxis: {
                                type: "category",
                                splitNumber: 3,
                                data: item["breakdown_value"]
                            },
                            yAxis: {
                                type: "value",
                                // min: function (value) {
                                //   return 0;
                                // },
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
                                        symbolSize: 10,
                                        data: [
                                            {
                                                name: item["insight_name"],
                                                xAxis: item["x"],
                                                yAxis: item["y"],
                                                itemStyle: {
                                                    color: "#96ce7b",
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
                                    radius: ['50%', '90%'],
                                    itemStyle: {
                                        borderRadius: 10,
                                        borderColor: '#fff',
                                        borderWidth: 2
                                    },
                                    label: {
                                        show: false,
                                        position: "center"
                                    },
                                    emphasis: {
                                        label: {
                                            show: true,
                                            fontSize: '18',
                                            fontWeight: 'bold'
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
                        minY = item["y_value"][0], maxY = item["y_value"][cnt - 1];

                let data = [];
                item["x_value"].forEach((val, i) => {
                    data.push([val, item["y_value"][i]]);
                });

                myChart.setOption(
                        {
                            tooltip: {
                                formatter: "{c}"
                            },
                            grid: {
                                top: "10px",
                                left: "40px",
                                right: "10px",
                                bottom: "20px"
                            },
                            xAxis: {
                                min: minX,
                                max: maxX,
                                splitNumber: 3,
                                axisLabel: {
                                    formatter: function (value) {
                                        return numberFormatter(value);
                                    }
                                },
                            },
                            yAxis: {
                                min: minY,
                                max: maxY,
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
                const cnt = item["x_value"].length;
                const minX = item["x_value"][0], maxX = item["x_value"][cnt - 1],
                        minY = item["y_value"][0], maxY = item["y_value"][cnt - 1];

                let group1 = [], group2 = [];
                item["x_value"].forEach((val, i) => {
                    if (item["label"][i] === 0) {
                        group1.push([val, item["y_value"][i]]);
                    } else {
                        group2.push([val, item["y_value"][i]]);
                    }
                });

                myChart.setOption(
                        {
                            tooltip: {
                                formatter: "{c}"
                            },
                            grid: {
                                top: "10px",
                                left: "40px",
                                right: "10px",
                                bottom: "20px"
                            },
                            xAxis: {
                                min: minX,
                                max: maxX,
                                splitNumber: 3,
                                axisLabel: {
                                    formatter: function (value) {
                                        return numberFormatter(value);
                                    }
                                },
                            },
                            yAxis: {
                                min: minY,
                                max: maxY,
                                axisLabel: {
                                    formatter: function (value) {
                                        return numberFormatter(value);
                                    }
                                },
                            },
                            series: [
                                {
                                    name: "1", // todo
                                    data: group1,
                                    type: "scatter",
                                    emphasis: {
                                        focus: "series"
                                    },
                                },
                                {
                                    name: "2", // todo
                                    data: group2,
                                    type: "scatter",
                                    emphasis: {
                                        focus: "series"
                                    },
                                }
                            ]
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
    font-size: 11px;
    font-weight: bold;
    margin: 3px 0 0 3px;
}

#chart {
    flex: auto;
}

/*.chart-box-hover {*/
/*    box-shadow: 7px 7px 7px #afafaf;*/
/*    transition: all;*/
/*}*/
</style>
