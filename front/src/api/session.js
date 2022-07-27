import axios from 'axios';


const session = axios.create({
});

if (localStorage.getItem('token')) {
    session.defaults.headers.common.Authorization = `Bearer ${localStorage.getItem('token')}`;
} else {
    session.defaults.headers.common.Authorization = null;
}

session.interceptors.response.use((response) => {
    return response;
}, (err) => {
    if (err.response.status === 401 && localStorage.getItem('token')) {
        localStorage.removeItem('token');
    }
    throw err;
});

session.defaults.baseURL = 'https://localhost:8000/';

export default session;
