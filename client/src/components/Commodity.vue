<template>
    <div>
        <h2 class="ui top center aligned attached header">{{name}}</h2>
        <div class="ui mobile reversed stackable grid attached segment">
            <div class="twelve wide column">
                <Stocks :stocks="data.stocks" />
            </div>
            <div class="four wide column">
                <CurrentBestPrice :price="data.prices[0]"/>
            </div>
        </div>
        <PriceList :prices="data.prices" :cargo="cargo" />
        <div class="ui section divider"></div>
    </div>
</template>

<script>
import gql from 'graphql-tag'

import Stocks from './Stocks.vue'
import PriceList from './PriceList.vue'
import CurrentBestPrice from './CurrentBestPrice.vue'

export default {
    name: 'Commodity',
    props: ['name', 'id', 'cargo'],
    components: {
        Stocks,
        PriceList,
        CurrentBestPrice
    },
    data() {
        return {
            data: {prices: [], stocks: []},
            days: 30,
        }
    },
    apollo: {
        data: {
            // gql query
            query: gql`
                query commodityData($id: Int!, $days: Int!) {
                    commodityPrices(commodity_id: $id) {
                        price
                        demand
                        date
                        market {
                            system
                            station
                            id
                        }
                        commodity {
                            inaraLink
                        }
                    }
                    commodityMaxPrices(commodity_id: $id, days: $days) {
                        price
                        demand
                        date
                    }
                }
            `,
            // Static parameters
            variables() {
                return {
                    id: this.id,
                    days: this.days
                }
            },
            update: data => {
                return {
                    prices: data.commodityPrices,
                    stocks: data.commodityMaxPrices
                }
            }
        }
    },
}
</script>

<style>

</style>