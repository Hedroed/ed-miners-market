<template>
    <div>
        <h3 class="ui center aligned attached header">Top 10 galaxie prices</h3>
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
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in topPrices" :key="item.market.id">
                        <td class="clipboard" v-clipboard:copy="item.market.system">
                            <span>{{ item.market.system }}</span>
                            <i title="Click to copy" class="copy outline icon" aria-hidden="true"></i>
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
                            <span>{{ moment.unix(item.date).fromNow() }}</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import _ from 'lodash/collection'

export default {
    name: 'PriceList',
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
            }
        }
    },
    computed: {
        topPrices() {
            const local = this.prices.map(d => {
                const realPrice = this.computeRealPrice(d.price, d.demand)
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
        isFleetCarrier(id) {
            return id > 3700000000
        }
    }
}
</script>

<style scoped>
.clipboard {
    cursor: pointer;
}
.icon {
    float: right;
}
.responsive {
    overflow-y: auto;
    padding: 0 1px;
    border: 1px solid #d4d4d5;
    margin: 0 -1px;
    border-radius: 0 0 0.28571429rem 0.28571429rem;
    border-top: 0;
}
.borderless {
    border: 0 !important;
}
.prices-table th.sortable:hover {
    color: #2185d0;
    cursor: pointer;
}
</style>
