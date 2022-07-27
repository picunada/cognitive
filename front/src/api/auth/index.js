import session from "@/api/session";
import qs from "qs";


export const Auth = {
    async login(username, password) {
        return await session.post('http://localhost:8000/manager/auth',
            qs.stringify({username, password}),
            { headers: {'content-type': 'application/x-www-form-urlencoded'}})
    },
    logout() {

    }
}