<template>
    <div id="app">
        <header>
            <div class="ui fluid container">
                <div class="ui large stackable text inverted menu">
                    <div class="item">
                        <img src="./assets/logo.png" />
                    </div>
                    <div class="item">
                        <h1>ED Dealers</h1>
                    </div>
                    <div class="item">
                        <div class="ui icon input">
                            <input v-model.trim="search" type="text" placeholder="Commodity Search..." @focus="$event.target.select()" />
                            <i class="search link icon"></i>
                        </div>
                    </div>
                    <div class="item">
                        <div class="ui icon input">
                            <input v-model.number="cargo" type="number" placeholder="Your cargo" @focus="$event.target.select()" min="0" />
                            <i class="boxes link icon"></i>
                        </div>
                    </div>
                    <div class="right menu">
                        <a class="ui item">About</a>
                        <a class="item">
                            <i class="github icon"></i> Github
                        </a>
                    </div>
                </div>
            </div>
        </header>
        <main class="ui container">
            <Commodity
                :name="item.name"
                :id="item.id"
                :cargo="+cargo"
                v-for="item in commodities"
                :key="item.id"
                v-show="item.name.toLowerCase().includes(search.toLowerCase())"
            />
        </main>
    </div>
</template>

<script>
import Commodity from './components/Commodity.vue'

export default {
    name: 'App',
    components: {
        Commodity
    },
    data() {
        return {
            search: '',
            cargo: 0,
            commodities: [
                {
                    name: 'Low Temperature Diamond',
                    id: 144
                },
                {
                    name: 'Painite',
                    id: 84
                }
            ]
        }
    },
    methods: {
        clear() {
            this.search = ''
        }
    }
}
</script>

<style>
header {
    background-color: black;
    background-image: url('./assets/header_bg.png');
    background-position: 90% center;
    background-repeat: no-repeat;
    padding: 1px 50px;
}
main {
    padding-top: 20px;
}
</style>
