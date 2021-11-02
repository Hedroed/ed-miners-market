<template>
    <div class="reports">
        <h2 class="ui top center aligned attached header">Reports over time</h2>
        <div class="ui bottom attached segment">
            <div class="chart">
                <line-chart style="height:100px" :chart-data="chartData" :options="options"></line-chart>
            </div>
        </div>
    </div>
</template>

<script>
import gql from 'graphql-tag'
import moment from 'moment'

export default {
    name: 'Reports',
    props: ['id'],
    components: {
        LineChart: () => import('./Chart.vue')
    },
    data() {
        return {
            data: {reports: []},
            hours: 72,
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
                legend: {
                    display: false,
                },
                elements: {
                    point: {
                        radius: 0,
                        hoverRadius: 0,
                    },
                    line: {
                        cubicInterpolationMode: 'monotone',
                    },
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
                            display: false,
                            position: 'left',
                        },
                    ]
                }
            }
        }
    },
    apollo: {
        data: {
            // gql query
            query: gql`
                query commodityData($id: ID, $hours: Int!) {
                    reports(commodity_id: $id, limit: $hours) {
                        date
                        reports
                    }
                }
            `,
            // Static parameters
            variables() {
                return {
                    id: this.id,
                    hours: this.hours,
                }
            },
            update: data => {
                return {
                    reports: data.reports,
                }
            },
            skip() {
                return false
            },
        }
    },
    computed: {
        chartData() {
            if (this.data.reports.length == 0) {
                return { labels: [], datasets: [] }
            }
            const all_data = this.data.reports
                .map(d => ({...d, date: moment(d.date * 1000)}))

            return {
                labels: all_data.map(d => d.date),
                datasets: [
                    {
                        fill: false,
                        label: 'Reports',
                        backgroundColor: '#f00',
                        borderColor: '#f00',
                        data: all_data.map(d => d.reports),
                    },
                ]
            }
        }
    }
    // mounted() {
    //     this.observer = new IntersectionObserver(entries => {
    //         const el = entries[0];
    //         if (el.isIntersecting) {
    //             this.skip = false;
    //             this.observer.unobserve(this.$el);
    //         }
    //     });

    //     this.observer.observe(this.$el);
    // },
}
</script>

<style scoped>

</style>