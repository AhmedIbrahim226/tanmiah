const protocol = window.location.protocol
const host = window.location.host

let getAllUsers = async () => {
    try {
        const response = await axios.get(`${protocol}//${host}/api/users/`)
        return response.data
    }catch (e) {
        console.log(e)
    }
}