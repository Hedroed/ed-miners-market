<template>
    <div class="price-stats">
        <h2 class="ui top attached header">Best current price</h2>
        <div class="ui attached segment">
            <div class="ui small statistic">
                <div class="value">
                    <i class="small dollar sign icon"></i> {{ price.price | number('0,0') }}
                </div>
                <div class="label">Best Price</div>
            </div>
        </div>
        <div class="ui attached segment">
            <div class="ui small statistic">
                <div class="value">
                    <i class="small dolly icon"></i> {{ price.demand | number('0,0') }}
                </div>
                <div class="label">Demand</div>
            </div>
        </div>
        <div class="ui attached segment">
            <h4>System / Station</h4>
            <div class="ui vertical orange buttons">
                <button class="ui button" v-clipboard:copy="price.market.system"><i class="copy icon"></i>{{ price.market.system }}</button>
                <button class="ui disabled button">{{ price.market.station }}</button>
            </div>
            <!-- <a class="ui teal image large label" v-clipboard:copy="price.market.system">
                <i class="copy icon"></i>
                {{ price.market.system }}
                <div class="detail">{{ price.market.station }}</div>
            </a> -->
        </div>
        <div class="ui bottom attached segment">
            <a class="ui orange basic button" target="_blank" :href="price.commodity.inaraLink">
                <i class="external alternate icon"></i>
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
                        system: '',
                        station: ''
                    },
                    commodity: {
                        inaraLink: ''
                    }
                }
            }
        }
    },
}
</script>

<style scoped>
.price-stats {
    text-align: center;
    padding-top: 20px;
}
</style>
