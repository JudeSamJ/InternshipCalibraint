import './App.css'

import {BrowserRoutes as Router,Routes,Route} from 'react-router-dom'

import Home from '../pages/Home'
import Cart from '../pages/Cart'
import Login from '../pages/Login'
import Orders from '../pages/Orders'
import Signup from '../pages/Signup'

function App(){
  return (
    <Router>
      <Home>
        <Routes>
          <Route path='/' element={<Orders/>}/>
        </Routes>
      </Home>
    </Router>
  )
}
