<template>
    <div class="stocks">
        <div class="chart">
            <line-chart :chart-data="chartData" :options="options"></line-chart>
        </div>
    </div>
</template>

<script>
import moment from 'moment'

export default {
    name: 'Stocks',
    components: {
        LineChart: () => import('./Chart.vue')
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
                                tooltipFormat: 'LLL',
                                unit: 'hour'
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
            // const past31days = moment().subtract(31, 'days');

            const all_data = this.stocks
                .map(d => ({...d, date: moment(d.date * 1000)}))
                // .filter(d => d.date.isAfter(past31days))

            return {
                labels: all_data.map(d => d.date),
                datasets: [
                    {
                        fill: false,
                        label: 'Price',
                        backgroundColor: '#f5821f',
                        borderColor: '#f5821f',
                        data: all_data.map(d => d.price),
                        yAxisID: 'y-axis-1'
                    },
                    {
                        type: 'bar',
                        label: 'Demand',
                        backgroundColor: '#f7e99c',
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

</style>
