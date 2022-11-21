import Notifications from '@kyvg/vue3-notification'
import { type UserModule } from '~/types'

export const install: UserModule = ({ app }) => {
  app.use(Notifications)
}
