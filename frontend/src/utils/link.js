import router from "@/router";

export const link = async (path, name, params = {}, query = {}) => {
    console.log(params,query)
    await router.push({path, params, query})
}