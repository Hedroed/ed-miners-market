<template>
    <div class="main">
        <div class="spinner" v-show="$apollo.loading">
            <EDSpinner/>
        </div>
        <h2 class="ui top center aligned attached header">{{name}}</h2>
        <div class="ui attached segment">
            <div class="ui mobile reversed stackable grid">
                <div class="twelve wide column">
                    <Stocks v-if="!$apollo.loading" :stocks="data.stocks.prices" />
                    <button class="mini ui basic button reload-icon" @click="$apollo.queries.data.refetch()">
                        <i class="redo alternate icon"></i>
                        Refresh
                    </button>
                </div>
                <div class="four wide column">
                    <CurrentBestPrice :inaraLink="data.prices.inaraLink" :price="data.prices.prices[0]"/>
                </div>
            </div>
        </div>
        <AlertVeryLow v-if="isVeryLowDemand"/>
        <AlertLow v-else-if="isLowDemand"/>
        <PriceList :prices="data.prices.prices" :cargo="cargo" />
        <div class="ui section divider"></div>
    </div>
</template>

<script>
import gql from 'graphql-tag'

import Stocks from './Stocks.vue'
import PriceList from './PriceList.vue'
import CurrentBestPrice from './CurrentBestPrice.vue'
import AlertLow from './alerts/AlertLow.vue'
import AlertVeryLow from './alerts/AlertVeryLow.vue'
import EDSpinner from './EDSpinner.vue'

import {isFleetCarrier} from '../utils'

export default {
    name: 'Commodity',
    props: ['name', 'id', 'cargo'],
    components: {
        Stocks,
        PriceList,
        CurrentBestPrice,
        AlertLow,
        AlertVeryLow,
        EDSpinner,
    },
    data() {
        return {
            data: {prices: {inaraLink: null, prices: []}, stocks: {prices: []}},
            hours: 72,
            skip: true,
            market_id: null,
        }
    },
    apollo: {
        data: {
            // gql query
            query: gql`
                query commodityData($id: ID!, $hours: Int!, $mid: ID) {
                    commodityPrices(commodity_id: $id, market_id: $mid) {
                        inaraLink
                        prices {
                            price
                            demand
                            date
                            reports
                            market {
                                system
                                station
                                id
                            }
                        }
                    }
                    commodityPricesChart(commodity_id: $id, market_id: $mid, limit: $hours) {
                        prices {
                            price
                            demand
                            date
                        }
                    }
                }
            `,
            // Static parameters
            variables() {
                return {
                    id: this.id,
                    hours: this.hours,
                    mid: this.market_id,
                }
            },
            update: data => {
                return {
                    prices: data.commodityPrices,
                    stocks: data.commodityPricesChart
                }
            },
            skip() {
                return this.skip
            },
        }
    },
    computed: {
        isLowDemand() {
            if (this.data.prices.prices.length < 1) return false
            return this.data.prices.prices[0].demand <= 1000 && !isFleetCarrier(this.data.prices.prices[0].market.id)
        },
        isVeryLowDemand() {
            if (this.data.prices.prices.length < 1) return false
            return this.data.prices.prices[0].demand <= 200 && !isFleetCarrier(this.data.prices.prices[0].market.id)
        }
    },
    mounted() {
        this.observer = new IntersectionObserver(entries => {
            const el = entries[0];
            if (el.isIntersecting) {
                this.skip = false;
                this.observer.unobserve(this.$el);
            }
        });

        this.observer.observe(this.$el);
    },
}
</script>

<style scoped>
.main {
    position: relative;
}
.spinner {
    z-index: 999;
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
}
.reload-icon {
    margin-top: 10px;
}
</style>