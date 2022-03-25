import router from "@/router";
import store from "@/store/index"

export const link = async (path, name) => {
    store.commit('changeChooseNavbar', name)
    await router.push(path)
}