import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createAuth0 } from '@auth0/auth0-vue'
import { createMetaManager } from 'vue-meta'

// bootstrap
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'

const app = createApp(App)

// Register Auth0 for authentication passwordless
app.use(
  createAuth0({
    domain: 'philipp-lein.eu.auth0.com',
    clientId: 'lOR7Yu0DcbsWRTaziSeA40CRduRs0fL9',
    authorizationParams: {
      audience: 'https://philipp-lein.eu.auth0.com/api/v2/',
      redirect_uri: window.location.origin
    },
    cacheLocation: 'localstorage',
    useRefreshTokens: true
  })
)

// Register meta for meta information of views
app.use(createMetaManager())

app.use(router).mount('#app')
