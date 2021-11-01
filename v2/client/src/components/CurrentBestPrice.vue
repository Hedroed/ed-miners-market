<template>
    <div class="price-stats">
        <h2 class="ui top attached header">Best current price</h2>
        <div class="ui attached segment">
            <div class="ui small statistic">
                <div class="value">
                    <i class="small dollar sign icon" aria-hidden="true"></i> {{ prettyNumber(price.price) }}
                </div>
                <div class="label">Best Price</div>
            </div>
        </div>
        <div class="ui attached segment">
            <div :class="demandClasses()">
                <div class="value">
                    <i class="small dolly icon" aria-hidden="true"></i> {{ prettyNumber(price.demand) }}
                </div>
                <div class="label">Demand</div>
            </div>
        </div>
        <div class="ui attached segment">
            <h4>System / Station</h4>
            <div class="ui vertical orange buttons">
                <button aria-label="Copy System name" class="ui button" v-clipboard:copy="price.market.system"><i class="copy icon" aria-hidden="true"></i>{{ price.market.system }}</button>
                <button aria-label="Station name" class="ui disabled button">{{ price.market.station }}</button>
            </div>
        </div>
        <div class="ui bottom attached segment">
            <a class="ui orange basic button" target="_blank" rel="noopener noreferrer" :href="price.commodity.inaraLink">
                <i class="external alternate icon" aria-hidden="true"></i>
                Inara page
            </a>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CurrentBestPrice',
    props: {
        price: {
            type: Object,
            default: function () {
                return {
                    price: 0,
                    demand: 0,
                    market: {
                        system: '---',
                        station: '---'
                    },
                    commodity: {
                        inaraLink: ''
                    }
                }
            }
        }
    },
    methods: {
        demandClasses() {
            let classes = ['ui', 'small', 'statistic']
            if (this.price.demand == 0) return classes
            let color = undefined
            if (this.price.demand <= 200) color = 'red'
            else if (this.price.demand <= 1000) color = 'orange'
            return [ ...classes, color ]
        },
        prettyNumber(n) {
            if (n) return Math.floor(n).toLocaleString()
            else return '0'
        }
    }
}
</script>

<style scoped>
.price-stats {
    text-align: center;
    padding-top: 20px;
}
</style>
