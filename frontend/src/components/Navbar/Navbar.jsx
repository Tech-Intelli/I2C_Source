import React, {useState} from 'react';
import './Navbar.css';
import { Link, useNavigate } from "react-router-dom";
import axios from 'axios';


export default function Navbar(props) {
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);
  const toggleDropdown = () => {
    console.log("User was clicked");
      setShowDropdown(!showDropdown);
  };
  const handleLogout = async() => {
    await axios.post(`${process.env.REACT_APP_BACKEND_URL}/logout_user`)
    .then((res)=>{
      navigate("/");
      setShowDropdown(false);
    })
    .catch((err) => {
      console.log("Error", err);
    });
    console.log("Go to Login")
  };


  return (
    <div className="header">
          <div>
              <p>CapGenAIze</p>
          </div>
          <div className= "icons">
          <i
              className={`fa-regular fa-user ${showDropdown ? 'active' : ''}`}
              onClick={(props.flag)?toggleDropdown: ()=>{console.log("first")}}
            ></i>
              <i className="fa-solid fa-bars"></i>
          </div>
          {showDropdown && (
          <div className="dropdown-input">
            <ul>
              <li onClick={handleLogout}>Log out</li>
            </ul>
          </div>
        )}
    </div>
  )
}
