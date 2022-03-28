import router from "@/router";
import store from "@/store/index"

export const link = async (path, name, params = {}, query = {}) => {
    console.log(params,query)
    store.commit('changeChooseNavbar', name)
    await router.push({path, params, query})
}