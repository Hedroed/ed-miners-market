<template>
    <div class="main">
        <div class="spinner" v-show="$apollo.loading">
            <EDSpinner/>
        </div>
        <h2 class="ui top center aligned attached header">{{name}}</h2>
        <div class="ui attached segment">
            <div class="ui mobile reversed stackable grid">
                <div class="twelve wide column">
                    <Stocks :stocks="data.stocks" />
                </div>
                <div class="four wide column">
                    <CurrentBestPrice :price="data.prices[0]"/>
                </div>
            </div>
        </div>
        <AlertVeryLow v-if="isVeryLowDemand"/>
        <AlertLow v-else-if="isLowDemand"/>
        <PriceList :prices="data.prices" :cargo="cargo" />
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
            data: {prices: [], stocks: []},
            days: 30,
            skip: true
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
            },
            skip() {
                return this.skip
            },
        }
    },
    computed: {
        isLowDemand() {
            if (this.data.prices.length < 1) return false
            return this.data.prices[0].demand <= 1000
        },
        isVeryLowDemand() {
            if (this.data.prices.length < 1) return false
            return this.data.prices[0].demand <= 200
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
</style>