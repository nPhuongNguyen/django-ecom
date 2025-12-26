const TOKEN_KEY = 'access_token'
class AuthStorage{
    static getToken() {
        // return localStorage.getItem(TOKEN_KEY)
        return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBodW9uZzA5MDl0dEBnbWFpbC5jb20ifQ.UAVPbncqo0vCklQNXyi5jv8BNVjDggbDZgk6poa667c'
    }
    setToken(token) {
        localStorage.setItem(TOKEN_KEY, token)
    }

    removeToken() {
        localStorage.removeItem(TOKEN_KEY)
    }

    hasToken() {
        return !!localStorage.getItem(TOKEN_KEY)
    }
}

