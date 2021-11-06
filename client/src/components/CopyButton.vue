<template>
    <div class="ui mini icon button clipboard" v-clipboard:success="onCopy" v-clipboard:copy="value" data-content="Copy to clipboard">
        <i class="copy outline icon" aria-hidden="true"></i>
        <transition name="slide-fade">
            <div v-if="copying" class="ui left pointing floating label">
                Copied
            </div>
        </transition>
    </div>
</template>

<script>
import {timeout} from '../utils'

export default {
    name: 'CopyButton',
    props: ['value'],
    data() {
        return {
            copying: false
        }
    },
    methods: {
        async onCopy() {
            this.copying = true
            await timeout(800)
            this.copying = false
        }
    }
}
</script>

<style scoped>
.clipboard {
    position: relative;
}
.clipboard .label{
    left: 65px;
    top: 2px;
}

/* Enter and leave animations can use different */
/* durations and timing functions.              */
.slide-fade-enter-active {
  transition: all .3s ease;
}
.slide-fade-leave-active {
  transition: all .8s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateX(-10px);
  opacity: 0;
}

</style>