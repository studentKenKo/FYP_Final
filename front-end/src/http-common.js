import axios from 'axios'

export default axios.create({
  baseURL: 'http://localhost:5431/',
  headers: {
    'Content-type': 'application/json',
    'Content-Length': '<calculated when request is sent>'
  }
})