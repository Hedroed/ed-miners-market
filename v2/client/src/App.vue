<template>
    <div id="app">
        <header>
            <div class="ui fluid container">
                <div class="ui large stackable text inverted menu">
                    <a href="/" class="item">
                        <img src="./assets/logo.png" alt="logo" />
                    </a>
                    <a href="/" class="item">
                        <h1>ED Miners Market</h1>
                    </a>
                    <div class="item">
                        <div class="ui icon input">
                            <input v-model.trim="search" type="text" placeholder="Commodity Search..." @focus="$event.target.select()" />
                            <i class="search link icon" aria-hidden="true"></i>
                        </div>
                    </div>
                    <div class="item">
                        <div class="ui icon input">
                            <input v-model.number="cargo" type="number" placeholder="Your cargo" @focus="$event.target.select()" min="0" />
                            <i class="boxes link icon" aria-hidden="true"></i>
                        </div>
                    </div>
                    <div class="right menu">
                        <a href="/about.html" class="ui item">About</a>
                        <a href="#" class="item">
                            <i class="github icon" aria-hidden="true"></i> Github
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
            cargo: '',
            commodities: [
                {
                    name: 'Low Temperature Diamond',
                    id: 144
                },
                {
                    name: 'Void Opal',
                    id: 10250
                },
                {
                    name: 'Painite',
                    id: 84
                },
                {
                    name: 'Tritium',
                    id: 10269
                },
                {
                    name: 'Benitoite',
                    id: 10247
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
    background-image: url('./assets/header_bg.webp');
    background-position: 90% center;
    background-repeat: no-repeat;
    padding: 1px 50px;
}
</style>
