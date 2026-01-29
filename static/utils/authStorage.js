class AuthStorage{
    static getToken(token_name) {
        return localStorage.getItem(token_name)
    }

    static setToken(token_name, token_data) {
        localStorage.setItem(token_name, token_data)
    }

    static removeToken(token_name) {
        localStorage.removeItem(token_name)
    }

    static hasToken(token_name) {
        return !!localStorage.getItem(token_name)
    }
}

