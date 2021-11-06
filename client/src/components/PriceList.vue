<template>
    <div>
        <div class="ui attached segment">
            <h3 class="ui center aligned header">Top 10 galaxie prices</h3>
        </div>
        <div class="responsive">
            <table
                class="prices-table borderless ui selectable unstackable celled striped bottom attached table"
                aria-label="Top 10 best prices in the galaxie"
            >
                <thead>
                    <tr>
                        <th scope="col">Market System</th>
                        <th scope="col">Market Station</th>
                        <th scope="col" class="sortable" @click="clickSort('price')">
                            Sell Price
                            <i :class="sortIconClasses('price')" aria-hidden="true"></i>
                        </th>
                        <th scope="col" class="sortable" @click="clickSort('demand')">
                            Demand
                            <i :class="sortIconClasses('demand')" aria-hidden="true"></i>
                        </th>
                        <th scope="col" class="sortable" @click="clickSort('realPrice')">Real Price
                            <i :class="sortIconClasses('realPrice')" aria-hidden="true"></i>
                        </th>
                        <th scope="col" class="sortable" @click="clickSort('realProfit')">Sell Profit
                            <i :class="sortIconClasses('realProfit')" aria-hidden="true"></i>
                        </th>
                        <th scope="col">Last Update</th>
                        <th scope="col">Reports</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in topPrices" :key="item.market.id">
                        <td>
                            <span><a class="system-link" :href="`https://inara.cz/market/?ps1=${item.market.system}&ps2=Alcor`" target="_blank" noreferer noopener>{{ item.market.system }}</a></span>
                            <CopyButton :value="item.market.system"/>
                        </td>
                        <td>
                            <span :title="item.market.id">{{ item.market.station }}</span>
                            <img v-if="isFleetCarrier(item.market.id)" title="FleetCarrier" class="copy outline icon" aria-hidden="true" src="../assets/fc-icon.png">
                        </td>
                        <td>
                            <span>{{ prettyNumber(item.price) }}</span>
                        </td>
                        <td>
                            <span>{{ prettyNumber(item.demand) }}</span>
                        </td>
                        <td>
                            <span>{{ prettyNumber(item.realPrice) }}</span>
                        </td>
                        <td>
                            <span>{{ prettyNumber(item.realProfit) }}</span>
                        </td>
                        <td>
                            <span :class="updateDateColor(item.date)" >{{ moment.unix(item.date).fromNow() }}</span>
                        </td>
                        <td>
                            <span >{{ prettyNumber(item.reports) }}</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import _ from 'lodash/collection'
import moment from 'moment'
import CopyButton from './CopyButton.vue'

import {isFleetCarrier} from '../utils'

export default {
    name: 'PriceList',
    components: {
        CopyButton,
    },
    props: {
        prices: {
            type: Array
        },
        cargo: {
            type: Number
        }
    },
    data() {
        return {
            sortOrder: {
                sortField: 'price',
                direction: 'desc'
            },
            copied: true,
        }
    },
    computed: {
        topPrices() {
            const local = this.prices.map(d => {
                let realPrice = d.price
                if(!isFleetCarrier(d.market.id)) {
                    realPrice = this.computeRealPrice(d.price, d.demand)
                }
                return {
                    ...d,
                    realPrice,
                    realProfit: this.cargo * realPrice
                }
            })

            if (this.sortOrder == undefined) return local

            return _.orderBy(
                local,
                this.sortOrder.sortField,
                this.sortOrder.direction
            )
        }
    },
    methods: {
        computeRealPrice(price, demand) {
            if(this.cargo) {
                return (
                    price *
                    Math.max(
                        0.3,
                        1 - Math.max(0, this.cargo / demand - 0.036) * 1.08
                    )
                )
            } else {
                return price
            }
        },
        clickSort(fieldName) {
            if (
                this.sortOrder == undefined ||
                this.sortOrder.sortField !== fieldName
            ) {
                this.sortOrder = {
                    sortField: fieldName,
                    direction: 'desc'
                }
            } else {
                this.sortOrder = {
                    sortField: fieldName,
                    direction:
                        this.sortOrder.direction === 'desc' ? 'asc' : 'desc'
                }
            }
        },
        sortIconClasses(fieldName) {
            if (
                this.sortOrder == undefined ||
                this.sortOrder.sortField !== fieldName
            ) {
                return ['icon', 'grey', 'sort', 'icon']
            } else {
                return [
                    'icon',
                    'blue',
                    'chevron',
                    this.sortOrder.direction === 'desc' ? 'up' : 'down',
                    'icon'
                ]
            }
        },
        prettyNumber(n) {
            if (n) return Math.floor(n).toLocaleString()
            else return '0'
        },
        updateDateColor(timestamp) {
            const diff = moment().diff(moment.unix(timestamp), 'seconds')
            if(diff < 3600) {
                return "date-good"
            } else if(diff < 86400) {
                return "date-average"
            } else {
                return "date-old"
            }
        },
        isFleetCarrier(id) {
            return isFleetCarrier(id)
        }
    }
}
</script>

<style scoped>
.icon {
    float: right;
}
.responsive {
    overflow-y: auto;
    padding: 0 1px;
    border: 1px solid #d4d4d5;
    margin: 0 -1px;
    border-top: 0;
}
.borderless {
    border: 0 !important;
}
.prices-table th.sortable:hover {
    color: #2185d0;
    cursor: pointer;
}

.date-good {
    color: #151;
}
.date-average {
    color: rgb(136, 100, 27);
}
.date-old {
    color: #611;
}

.system-link {
    color: inherit;
}

.system-link:hover {
    text-decoration: underline;
}

</style>
