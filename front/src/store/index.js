import {createStore} from "vuex";
import {AuthModule} from "@/api/auth/store";

export default createStore({
    modules: {
        auth: AuthModule
    }
})