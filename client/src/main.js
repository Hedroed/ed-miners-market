import Vue from 'vue'
import VueApollo from 'vue-apollo'
import Vue2Filters from 'vue2-filters'
import ApolloClient from 'apollo-boost'
import moment from 'moment'
import VueClipboard from 'vue-clipboard2'
 

import App from './App.vue'


Vue.use(VueClipboard)
Vue.use(Vue2Filters)
Vue.use(VueApollo)

Vue.config.productionTip = false
Vue.prototype.moment = moment


const apolloClient = new ApolloClient({
    // You should use an absolute URL here
    // uri: 'http://localhost:4000/graphql/'
    uri: 'http://ed-tool.nathanryd.in/graphql/'
})

const apolloProvider = new VueApollo({
    defaultClient: apolloClient,
})
  

new Vue({
    render: h => h(App),
    apolloProvider,
}).$mount('#app')
