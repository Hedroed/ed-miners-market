<template>
    <div>
        <h3 class="ui center aligned attached header">Top 10 galaxie prices</h3>
        <vuetable
            ref="vuetable"
            :api-mode="false"
            :data-manager="dataManager"
            :fields="fields"
            :css="css.table"
            class="responsive"
        >
            <div
                slot="system-slot"
                slot-scope="props"
                class="clipboard"
                v-clipboard:copy="props.rowData.market.system"
            >
                <span title="Click to copy">{{ props.rowData.market.system }}</span>
                <i class="clip-icon copy outline icon"></i>
            </div>
            <div slot="station-slot" slot-scope="props">
                <span>{{ props.rowData.market.station }}</span>
            </div>
            <div slot="date-slot" slot-scope="props">
                <span>{{ moment.unix(props.rowData.date).fromNow() }}</span>
            </div>
            <div slot="price-slot" slot-scope="props">
                <span>{{ props.rowData.price | number('0,0') }}</span>
            </div>
            <div slot="demand-slot" slot-scope="props">
                <span>{{ props.rowData.demand | number('0,0') }}</span>
            </div>
            <div slot="realprice-slot" slot-scope="props">
                <span>{{ computeRealPrice(props.rowData.price, props.rowData.demand) | number('0,0') }}</span>
            </div>
            <div slot="profit-slot" slot-scope="props">
                <span>{{ computeRealProfit(props.rowData.price, props.rowData.demand) | number('0,0') }}</span>
            </div>
        </vuetable>
    </div>
</template>

<script>
import Vuetable from 'vuetable-2'
import VuetableCss from './VuetableCss.js'

import _ from 'lodash/collection'

export default {
    name: 'PriceList',
    components: {
        Vuetable
    },
    props: {
        prices: {
            type: Array,
        },
        cargo: {
            type: Number
        }
    },
    data() {
        return {
            css: VuetableCss,
            fields: [
                'market.id',
                {
                    name: 'system-slot',
                    title: 'Market System'
                },
                {
                    name: 'station-slot',
                    title: 'Market Station'
                },
                {
                    name: 'price-slot',
                    title: 'Sell Price',
                    sortField: 'price'
                },
                {
                    name: 'demand-slot',
                    title: 'Demand',
                    sortField: 'demand'
                },
                {
                    name: 'realprice-slot',
                    title: 'Real Price'
                },
                {
                    name: 'profit-slot',
                    title: 'Sell Profite'
                },
                {
                    name: 'date-slot',
                    title: 'Last Update'
                }
            ]
        }
    },
    watch: {
        topPrices() {
            this.$refs.vuetable.refresh()
        }
    },
    computed: {
        topPrices() {
            return this.prices.map((d, i) => ({ ...d, id: i }))
        } 
    },
    methods: {
        dataManager(sortOrder, pagination) {
            if (this.topPrices == undefined || this.topPrices.length == 0) {
                return {
                    pagination: pagination,
                    data: []
                }
            }

            let local = this.topPrices
            // sortOrder can be empty, so we have to check for that as well
            if (sortOrder.length > 0) {
                local = _.orderBy(
                    local,
                    sortOrder[0].sortField,
                    sortOrder[0].direction
                )
            }

            return {
                pagination: pagination,
                data: local
            }
        },
        computeRealPrice(price, demand) {
            return price * Math.max(0.3, 1-(Math.max(0, (this.cargo / demand)-0.036)) * 1.08)
        },
        computeRealProfit(price, demand) {
            return this.cargo * this.computeRealPrice(price, demand)
        }
    }
}
</script>

<style scoped>
.clipboard {
    cursor: pointer;
}
.clip-icon {
    float: right;
}
.responsive {
    /* width: 100%; */
    /* box-sizing: border-box; */
    overflow-y: auto;
    padding: 0 1px;
}
</style>
