import { type UserModule } from '~/types'

export const install: UserModule = ({ isClient, router }) => {
  if (isClient) {
    router.beforeEach(async (to, from) => {
      const auth = useAuthStore()
      const roles = to.meta.roles as [string]
      //              Page role guard
      if (to.meta.roles) {
        return await auth.fetchUser().then(() => {
          if (!roles.includes(auth.user?.role as string))
            return { path: '/' }
        },
        )
      }
    })
  }
}
