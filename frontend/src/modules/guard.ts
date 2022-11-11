import { type UserModule } from '~/types'

export const install: UserModule = ({ isClient, router }) => {
    if (isClient) {
      router.beforeEach(async (to, from) => {
        const auth = useAuthStore()
        //             Page requires login     Prevent redirect loops       User authentication check
        if(to.meta.requiresAuth && to.path !== '/login'  && !auth.isAuthenticated) {
            console.log('Authentication required for page \'' + to.name?.toString() + '\'! Redirecting to login.')
            // Redirect user to login page
            return { path: '/login' }
        }
    })
  }
}

