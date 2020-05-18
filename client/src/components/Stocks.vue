<template>
    <div class="stocks">
        <div class="chart">
            <line-chart :chart-data="chartData" :options="options"></line-chart>
        </div>
    </div>
</template>

<script>
import LineChart from './Chart.vue'

export default {
    name: 'Stocks',
    components: {
        LineChart
    },
    props: {
        stocks: {
            type: Array,
        }
    },
    data() {
        return {
            days: 30,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: false,
                },
                tooltips: {
                    mode: 'index',
                    intersect: false
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    xAxes: [
                        {
                            display: true,
                            type: 'time',
                            time: {
                                tooltipFormat: 'LL'
                            },
                            scaleLabel: {
                                display: false,
                            }
                        }
                    ],
                    yAxes: [
                        {
                            type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                            display: true,
                            ticks: {
                            },
                            position: 'left',
                            id: 'y-axis-1',
                            scaleLabel: {
                                display: false,
                                labelString: 'Price'
                            }
                        },
                        {
                            type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                            display: true,
                            ticks: {
                            },
                            position: 'right',
                            id: 'y-axis-2',
                            scaleLabel: {
                                display: false,
                                labelString: 'Demand'
                            },

                            // grid line settings
                            gridLines: {
                                drawOnChartArea: false // only want the grid lines for one axis to show up
                            }
                        }
                    ]
                }
            }
        }
    },
    computed: {
        chartData() {
            if (this.stocks.length == 0) {
                return { labels: [], datasets: [] }
            }

            let l = this.stocks.length
            let d = 24 * 3600
            let first_ts = this.stocks[0].date
            let first_price = this.stocks[0].price
            let first_demand = this.stocks[0].demand

            let random_data = Array.from({
                length: Math.max(0, this.days - l)
            }).map((_, i) => ({
                price: Math.floor(Math.random() * first_price/2) + first_price*0.1,
                demand: Math.floor(Math.random() * first_demand/2) + first_demand*0.1,
                date: first_ts - (i + 1) * d
            }))

            let all_data = this.stocks.concat(random_data).sort((a,b) => a.date<b.date)

            return {
                labels: all_data.map(d => new Date(d.date * 1000)),
                datasets: [
                    {
                        fill: false,
                        label: 'Price',
                        backgroundColor: '#f2711c',
                        borderColor: '#f2711c',
                        data: all_data.map(d => d.price),
                        yAxisID: 'y-axis-1'
                    },
                    {
                        type: 'bar',
                        label: 'Demand',
                        backgroundColor: '#f7e497',
                        data: all_data.map(d => d.demand),
                        yAxisID: 'y-axis-2'
                    }
                ]
            }
        }
    }
}
</script>

<style scoped>
/* .chart {
    width: 1000px;
} */
</style>
