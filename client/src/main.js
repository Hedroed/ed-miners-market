import Vue from 'vue'
import VueApollo from 'vue-apollo'
import ApolloClient from 'apollo-boost'
import moment from 'moment'
import VueClipboard from 'vue-clipboard2'

import 'semantic-ui-css/components/reset.min.css'
import 'semantic-ui-css/components/site.min.css'
import 'semantic-ui-css/components/button.min.css'
import 'semantic-ui-css/components/container.min.css'
import 'semantic-ui-css/components/segment.min.css'
import 'semantic-ui-css/components/table.min.css'
import 'semantic-ui-css/components/menu.min.css'
import 'semantic-ui-css/components/header.min.css'
import 'semantic-ui-css/components/grid.min.css'
import 'semantic-ui-css/components/icon.min.css'
import 'semantic-ui-css/components/message.min.css'
import 'semantic-ui-css/components/statistic.min.css'
import 'semantic-ui-css/components/input.min.css'
import 'semantic-ui-css/components/divider.min.css'

import App from './App.vue'


Vue.use(VueClipboard)
Vue.use(VueApollo)

Vue.config.productionTip = false
Vue.prototype.moment = moment


const apolloClient = new ApolloClient({
    uri: 'https://edmm.space/graphql/'
})

const apolloProvider = new VueApollo({
    defaultClient: apolloClient,
})
  

new Vue({
    render: h => h(App),
    apolloProvider,
}).$mount('#app')
