import axios from 'axios'

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    timeout: 20000,
    withCredentials: true
})

export const post = (url,data,config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }) => {
    return new Promise((resolve, reject) => {
        instance.post(url, data, config).then(response => {
            resolve(response.data)
        }, err => {
            reject(err)
        })
    })
}

export const get = (url, params={}) => {
    return new Promise((resolve, reject) => {
        instance.get(url,{params}).then(response => {
            resolve(response.data)
        }, err => {
            reject(err)
        })
    })
}