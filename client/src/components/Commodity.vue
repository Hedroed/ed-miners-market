<template>
    <div class="main">
        <div class="spinner" v-show="$apollo.loading">
            <EDSpinner/>
        </div>
        <div class="ui segments">
            <div class="ui segment">
                <h2 class="ui center aligned header">{{name}}</h2>
            </div>
            <div class="ui segment">
                <div class="ui mobile reversed stackable grid">
                    <div class="twelve wide column">
                        <Stocks v-if="!$apollo.loading" :stocks="data.stocks.prices" />
                        <!-- <button class="mini ui basic button reload-icon" @click="$apollo.queries.data.refetch()">
                            <i class="redo alternate icon"></i>
                            Refresh
                        </button> -->
                        <div class="ui buttons">
                            <button class="ui orange basic button" @click="$apollo.queries.data.refetch()">
                                <i class="redo alternate icon"></i>
                                Refresh
                            </button>
                            <button :class="['ui', 'basic', 'button', {'orange': filterFleetcarrier, 'grey': !filterFleetcarrier}]" @click="filterFleetcarrier = !filterFleetcarrier">
                                <i v-if="filterFleetcarrier" class="check icon"></i>
                                <i v-else class="times icon"></i>
                                Filter FleetCarrier
                            </button>
                            <button :class="['ui', 'basic', 'button', {'orange': filterOld, 'grey': !filterOld}]" @click="filterOld = !filterOld">
                                <i v-if="filterOld" class="check icon"></i>
                                <i v-else class="times icon"></i>
                                Only recent (&lt; 3h)
                            </button>
                        </div>
                    </div>
                    <div class="four wide column">
                        <CurrentBestPrice :inaraLink="data.prices.inaraLink" :price="data.prices.prices[0]"/>
                    </div>
                </div>
            </div>
            <!-- <div class="ui horizontal compact segments">
                <div class="ui segment">
                    <h4 class="ui header">Filters:</h4>
                </div>
                <div class="ui segment">
                    <button class="ui toggle button">
                        <input type="checkbox" name="fleetcarrier" v-model="filterFleetcarrier" true-value="yes" false-value="no">
                        <label>Filter FleetCarrier</label>
                    </div>
                </div>
                <div class="ui segment">
                    <div class="ui toggle checkbox" title="filter older than 2 hours">
                        <input type="checkbox" name="old" v-model="filterOld" true-value="yes" false-value="no">
                        <label>Only recent (&lt; 3h)</label>
                    </div>
                </div>
            </div> -->
            <PriceList :prices="data.prices.prices" :cargo="cargo" />
            <AlertVeryLow v-if="isVeryLowDemand"/>
            <AlertLow v-else-if="isLowDemand"/>
        </div>
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
            skip: true,
            market_id: null,
            filterFleetcarrier: false,
            filterOld: false,
        }
    },
    apollo: {
        data: {
            // gql query
            query: gql`
                query commodityData($id: ID!, $hours: Int!, $mid: ID, $filter_carrier: Boolean!) {
                    commodityPrices(commodity_id: $id, market_id: $mid, hours: $hours, filter_carrier: $filter_carrier) {
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
                    commodityPricesChart(commodity_id: $id, market_id: $mid, hours: 72, filter_carrier: $filter_carrier) {
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
                    hours: this.filterOld ? 3 : 72,
                    mid: this.market_id,
                    filter_carrier: this.filterFleetcarrier
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
        },
    },
    mounted() {
        window.appp = this.$apollo
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
/* .reload-icon {
    margin-top: 10px;
} */
</style>