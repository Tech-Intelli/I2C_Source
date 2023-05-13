import React from 'react'
import "./card.css";

import image from "./image.jpeg";
import logo from "./logo.jpg";

const Card = () => {
  return (
    <div className="card-page">
        <div className="top">
            <div className="userDetails">
                <div className="profile_img">
                    <img src ={logo} class = "cover"/>
                </div>
                <h3>User_Name<br/><span>India</span></h3>
            </div>
            <div>
                <i class="fa-solid fa-ellipsis-vertical dot"></i>
            </div>
        </div>
        <div className="imgBx">
            <img src={image} alt="" className='cover'/>
        </div>
        <div className='actionBtns'>
            <div className="left">
                <i class="fa-regular fa-heart"></i>
                <i class="fa-regular fa-comment"></i>
                <i class="fa-solid fa-share"></i>
            </div>
            <div className="right">
            <i class="fa-regular fa-bookmark"></i>
            </div>
        </div>
        <h4 className='likes'>3,684 likes</h4>
        <h4 className='message'>Newly generated Caption<span>#cards #html # css</span></h4>

    </div>
  )
}

export default Card