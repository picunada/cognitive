import {Auth} from "@/api/auth/index";
import session from "@/api/session";

export const AuthModule = {
    namespaced: true,

    state() {
        return {
            credentials: {
                token: localStorage.getItem('token') || null
            },
        }
    },

    mutations: {
        setToken(state, token) {
            state.credentials.token = token
            localStorage.setItem('token', token)
        },

        deleteToken(state) {
            state.credentials.token = null;
            localStorage.removeItem('token')
        }
    },

    actions: {
        onLogin({commit}, user) {
            Auth.login(user.email, user.password).then((res) => {
                commit('setToken', res.data.access_token)
                session.defaults.headers['Authorization'] = `Bearer ${res.data.access_token}`
            })
        },
        onLogout({commit}) {
            commit('deleteToken')
            delete session.defaults.headers['Authorization']
        }
    }
}