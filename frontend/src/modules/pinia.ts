import { createPinia } from 'pinia'
import { Router } from 'vue-router'
import { type UserModule } from '~/types'

declare module 'pinia' {
  export interface PiniaCustomProperties {
      router: Router
  }
}

// Setup Pinia
// https://pinia.vuejs.org/
export const install: UserModule = ({ isClient, initialState, app }) => {
  const pinia = createPinia()
  app.use(pinia)
  // Refer to
  // https://github.com/antfu/vite-ssg/blob/main/README.md#state-serialization
  // for other serialization strategies.
  if (isClient)
    pinia.state.value = (initialState.pinia) || {}
  else
    initialState.pinia = pinia.state.value

}
